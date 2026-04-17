import pandas as pd
import os

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
        print(f"已保存: {output_file}")

