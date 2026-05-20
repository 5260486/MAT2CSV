import pandas as pd
import os
import numpy as np

class CSVHelper:

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


    def merge_csv_by_name(folder_path,filenames,num,output_folder):       
        groups={}
        for name in filenames:
            prefix = name[:num]               # 提取前 n 个字符作为分组键
            csv_path=os.path.join(folder_path, f"{name}.csv")
            groups.setdefault(prefix, []).append(csv_path)

        for prefix, file_list in groups.items():
            dfs = []
            for file_path in file_list:
                df = pd.read_csv(file_path)
                dfs.append(df)

        # 按列合并（axis=1）
        merged_df = pd.concat(dfs, axis=1)

        # 保存合并结果
        # 输出文件名用前缀命名（去除可能影响文件名的字符）
        safe_prefix = prefix.replace('\n', '_').replace('\r', '_').replace('/', '_')
        output_file = os.path.join(output_folder, f"merged_{safe_prefix}.csv")
        merged_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Merged: {output_file}")

    def cut_data(input_file,head_cut,tail_cut,output_file):
        with open(input_file, 'r', encoding='utf-8') as infile:
            # 读取所有行
            lines = infile.readlines()
        
        total_lines = len(lines)

        # 1. 单独提取表头（如果没有行则处理空文件）
        header = lines[0] if total_lines > 0 else None

        # 2. 计算数据行的起始和结束索引
        #    - 数据行从索引 1 开始（跳过表头）
        #    - 掐头从数据行的第 head_cut 行开始（即删除前 head_cut 条数据）
        data_start = 1 + head_cut
        data_end = total_lines - tail_cut

        # 3. 获取保留的数据行（确保起始不大于结束，否则无数据）
        if data_start < data_end:
            data_lines = lines[data_start:data_end]
        else:
            data_lines = []   # 掐头+去尾后无数据行

        # 4. 组合最终结果：表头 + 数据行
        preserved_lines = [header] + data_lines if header else []
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(preserved_lines)

        print(f"Finish: {output_file}")

    """
        target_col----the name of column need be operated 
        operation----the operation type: '+', '-', '*', '/'
        operate_value----the value to be operated with column
    """
    def operate_column(input_file,target_col,operation,operate_value,output_file):
        df = pd.read_csv(input_file)
        
        if operation == '+':
            result = df[target_col] + operate_value
        elif operation == '-':
            result = df[target_col] - operate_value
        elif operation == '*':
            result = df[target_col] * operate_value
        elif operation == '/':
            # 处理除数为0的情况：结果设为NaN或0，这里用NaN并警告
            if operate_value == 0:
               raise ValueError("除数不能为0")
            result = df[target_col] / operate_value
        else:
            raise ValueError("不支持的操作类型，请使用 '+', '-', '*', '/'")

        df[target_col] = result
        df.to_csv(output_file, index=False)
        print(f"Operated：{output_file}")