# -*- coding: utf-8 -*-#
import scipy.io
import os
import pandas as pd
import numpy as np
import re

class ReadMat:

    def mat_struct_to_dict(matobj):
        from scipy.io.matlab.mio5_params import mat_struct
        result = {}
        for fieldname in matobj._fieldnames:
            elem = getattr(matobj, fieldname)
            if isinstance(elem, mat_struct):
                result[fieldname] = ReadMat.mat_struct_to_dict(elem)
            elif isinstance(elem, np.ndarray):
                result[fieldname] = ReadMat.parse_ndarray(elem)
            else:
                result[fieldname] = elem
        return result

    def parse_ndarray(arr):
        if arr.dtype == 'O':  # cell 或 struct 数组
            out = []
            for item in arr:
                if hasattr(item, '_fieldnames'):
                    out.append(ReadMat.mat_struct_to_dict(item))
                elif isinstance(item, np.ndarray):
                    out.append(ReadMat.parse_ndarray(item))
                else:
                    out.append(item)
            return out
        else:
            return arr.tolist()

    def flatten_to_str(v):
        # transfer data with complex struct in mat 
        if isinstance(v, dict):
            return str({k: ReadMat.flatten_to_str(val) for k, val in v.items()})
        elif isinstance(v, list):
            return str([ReadMat.flatten_to_str(i) for i in v])
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
                parsed = ReadMat.mat_struct_to_dict(v)
                flat = ReadMat.flatten_to_str(parsed)
                data_dict[k] = [flat]
            elif isinstance(v, np.ndarray):
                parsed = ReadMat.parse_ndarray(v)
                flat = ReadMat.flatten_to_str(parsed)
                if isinstance(parsed, list) and len(parsed) > 1:
                    data_dict[k] = [ReadMat.flatten_to_str(i) for i in parsed]
                    max_len = max(max_len, len(parsed))
                else:
                    data_dict[k] = [flat]
            else:
                data_dict[k] = [ReadMat.flatten_to_str(v)]

        # align the length of the column
        for k in data_dict:
            if len(data_dict[k]) < max_len:
                data_dict[k] += [''] * (max_len - len(data_dict[k]))

        df = pd.DataFrame(data_dict)
        df.to_csv(output_csv, index=False)


class Mat2CSV:

    def transfer_mat_to_csv(folder_path,mat_path,new_names,idx):

        # name the csv file with the corresponding mat filename,idx start with 1
        new_csv_filename=f"{new_names[idx-1]}.csv"
        new_csv_path=os.path.join(folder_path, new_csv_filename)
        ReadMat.extract_to_single_csv(mat_path,new_csv_path)

        print(f"Transfered: {new_csv_filename}")
        return new_csv_filename

    """
        new_headers----Modify header to a uniform form 
        selected_columns----select data needed
    """
    def extract_data_from_csv(folder_path,new_csv_filename,new_headers,selected_columns):
        input_file=os.path.join(folder_path, new_csv_filename)
        df = pd.read_csv(input_file)
        df.columns = new_headers

        csv_output_filename=f"{'new_'+new_csv_filename}"
        output_path=os.path.join(folder_path,csv_output_filename)
        df[selected_columns].to_csv(output_path, index=False)
        print(f"Extracted：{output_path}")


class Header:
    def header_choice(file_path):

        df=pd.read_csv(file_path)
        original_headers=df.columns.tolist()

        # 格式化列名
        formatted_headers = [Header.header_format(header) for header in original_headers]
        
        # 更新DataFrame的列名
        df.columns = formatted_headers
        
        # 显示处理后的表头
        print("\nAll columns:")
        for i, header in enumerate(formatted_headers, 1):
            print(f"{i}. {header}")
        
        # 显示前两行数据
        print("\nThe data in the first two rows:")
        print(df.head(2).to_string(index=False))

        # 获取用户选择的列
        print("\nPlease input column number you need, which divided by ','.")
        print("\n You can input 'all' to choose all columns.")
        user_input = input().strip()
        
        selected_columns = []
        
        if user_input.lower() == 'all':
            selected_columns = formatted_headers
        else:
            # 处理用户输入的列序号
            try:
                selected_indices = [int(idx.strip()) - 1 for idx in user_input.split(',')]
                
                # 验证索引是否有效
                for idx in selected_indices:
                    if idx < 0 or idx >= len(formatted_headers):
                        print(f"Error: Number {idx+1} is invalid，passed")
                        continue
                    selected_columns.append(formatted_headers[idx])
            except ValueError:
                print("You have a error of input format!")
                return
        
        # 显示用户选择的列
        print(f"\nColumns you have choosen: {', '.join(selected_columns)}")
        
        return formatted_headers,selected_columns
    
    def header_format(header_old):

        """
        格式化表头：首字母大写，其余字母小写，符号保持不变
    
        参数:
        header: 原始表头字符串
    
        返回:
        格式化后的表头
        """
        # 如果表头为空，直接返回
        if not header_old or pd.isna(header_old):
            return header_old
    
        # 将字符串转换为字符串类型（避免可能的数字类型问题）
        header_str = str(header_old)
    
        # 使用正则表达式匹配单词边界，将每个单词的首字母大写，其余小写
        # 同时保留非字母字符不变
        def capitalize_word(match):
            word = match.group(0)
            if len(word) > 0:
                return word[0].upper() + word[1:].lower()
            return word
    
        # 匹配单词（字母序列）
        formatted_header = re.sub(r'[a-zA-Z]+', capitalize_word, header_str)

        return formatted_header