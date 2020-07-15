import pandas as pd
from flask import request, make_response
from api.variable.get import VariableGetter
from api.variable.get import UnknownSubjectError
from api.metadata.main import VariableMetadataResource


class VariableGetterAll:
    vg = VariableGetter()
    vmr = VariableMetadataResource()

    def get(self, dataset):
        request_variables = request.args.getlist('variable') or []
        include_cols = request.args.getlist('include') or []
        exclude_cols = request.args.getlist('exclude') or []

        limit = 20
        if request.args.get('limit') is not None:
            try:
                limit = int(request.args.get('limit'))
            except:
                pass

        try:
            regions = self.vg.get_query_region_ids()
        except UnknownSubjectError as ex:
            return ex.get_error_dict(), 404

        if len(request_variables) > 0:
            variables = request_variables
        else:
            variables = [x['variable_id'] for x in self.vmr.get(dataset)[0]][:limit]

        df_list = []
        for variable in variables:
            _ = self.vg.get_direct(dataset, variable, include_cols, exclude_cols, -1, regions, return_df=True)

            if _ is not None:
                _ = self.reshape_canonical_data(_)
                df_list.append(_)
        df = pd.concat(df_list)
        df.drop(columns=['value', 'value_unit', 'variable_id', 'variable'], inplace=True)
        csv = df.to_csv(index=False)
        output = make_response(csv)
        output.headers['Content-Disposition'] = f'attachment; filename={dataset}_variables_all.csv'
        output.headers['Content-type'] = 'text/csv'
        return output

    def reshape_canonical_data(self, df):
        new_df = pd.DataFrame(columns=df.columns)
        for i, row in df.iterrows():
            row[f"{row['variable_id']}"] = row['value']
            row['{}_unit'.format(row['variable_id'])] = row['value_unit']
            row['{}_name'.format(row['variable_id'])] = row['variable']

            new_df = new_df.append(row)
        return new_df
