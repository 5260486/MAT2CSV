import pandas as pd
import re
import csv
import os
import tempfile

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
        print("\n Please input column number you need, which divided by ','.")
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

    def merge_header(input_file,folder_path,n):
        """
        将CSV文件的前n行合并为一行作为新表头，直接修改原文件
    
        参数:
            input_file: 输入CSV文件路径
            n: 需要合并的行数
        """
        try:
            # 创建临时文件
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8',dir=folder_path)
        
            with open(input_file, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                writer = csv.writer(temp_file)
            
                # 读取前n行
                header_rows = []
                for i in range(n):
                    try:
                        row = next(reader)
                        header_rows.append(row)
                    except StopIteration:
                        # 文件行数不足n行
                        print(f"警告: 文件只有 {i} 行，少于要求的 {n} 行")
                        break
            
                # 确定最大列数
                max_cols = max(len(row) for row in header_rows) if header_rows else 0
            
                # 合并每一列的前n行
                new_header = []
                for col in range(max_cols):
                    col_values = []
                    for row in header_rows:
                        if col < len(row):
                            col_values.append(str(row[col]).strip())
                        else:
                            col_values.append("")
                
                    # 使用空格合并同一列的值
                    merged_value = " ".join(col_values).strip()
                    new_header.append(merged_value)
            
                # 写入新的表头
                writer.writerow(new_header)
            
                # 直接复制剩余的行
                for row in reader:
                    writer.writerow(row)
        
            # 关闭临时文件
            temp_file.close()
        
            # 用临时文件替换原文件
            os.replace(temp_file.name, input_file)
        
            print(f"成功处理文件: {input_file}")
            print(f"合并了前 {n} 行作为新表头")
        
        except Exception as e:
            # 如果出错，删除临时文件
            if 'temp_file' in locals() and not temp_file.closed:
                temp_file.close()
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            print(f"处理文件时出错: {e}")