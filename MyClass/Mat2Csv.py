# -*- coding: utf-8 -*-#
import scipy.io
import os
import pandas as pd
import numpy as np

class Mat2CSV:

    def mat_struct_to_dict(matobj):
        from scipy.io.matlab.mio5_params import mat_struct
        result = {}
        for fieldname in matobj._fieldnames:
            elem = getattr(matobj, fieldname)
            if isinstance(elem, mat_struct):
                result[fieldname] = Mat2CSV.mat_struct_to_dict(elem)
            elif isinstance(elem, np.ndarray):
                result[fieldname] = Mat2CSV.parse_ndarray(elem)
            else:
                result[fieldname] = elem
        return result

    def parse_ndarray(arr):
        if arr.dtype == 'O':  # cell 或 struct 数组
            out = []
            for item in arr:
                if hasattr(item, '_fieldnames'):
                    out.append(Mat2CSV.mat_struct_to_dict(item))
                elif isinstance(item, np.ndarray):
                    out.append(Mat2CSV.parse_ndarray(item))
                else:
                    out.append(item)
            return out
        else:
            return arr.tolist()

    def flatten_to_str(v):
        # transfer data with complex struct in mat 
        if isinstance(v, dict):
            return str({k: Mat2CSV.flatten_to_str(val) for k, val in v.items()})
        elif isinstance(v, list):
            return str([Mat2CSV.flatten_to_str(i) for i in v])
        else:
            return str(v)

    def extract_to_single_csv(matfile, output_csv='all_variables.csv'):
        mat = scipy.io.loadmat(matfile, struct_as_record=False, squeeze_me=True)
        data_dict = {}
        max_len = 1

        for k, v in mat.items():
            if k.startswith('__'):
                continue
            if hasattr(v, '_fieldnames'):
                parsed = Mat2CSV.mat_struct_to_dict(v)
                flat = Mat2CSV.flatten_to_str(parsed)
                data_dict[k] = [flat]
            elif isinstance(v, np.ndarray):
                parsed = Mat2CSV.parse_ndarray(v)
                flat = Mat2CSV.flatten_to_str(parsed)
                if isinstance(parsed, list) and len(parsed) > 1:
                    data_dict[k] = [Mat2CSV.flatten_to_str(i) for i in parsed]
                    max_len = max(max_len, len(parsed))
                else:
                    data_dict[k] = [flat]
            else:
                data_dict[k] = [Mat2CSV.flatten_to_str(v)]

        # align the length of the column
        for k in data_dict:
            if len(data_dict[k]) < max_len:
                data_dict[k] += [''] * (max_len - len(data_dict[k]))

        df = pd.DataFrame(data_dict)
        df.to_csv(output_csv, index=False)

    def transfer_mat_to_csv(folder_path,mat_path,new_names,idx):

        # name the csv file with the corresponding mat filename,idx start with 1
        new_csv_filename=f"{new_names[idx-1]}.csv"
        new_csv_path=os.path.join(folder_path, new_csv_filename)
        Mat2CSV.extract_to_single_csv(mat_path,new_csv_path)

        print(f"Transfered: {new_csv_filename}")
        return new_csv_filename



