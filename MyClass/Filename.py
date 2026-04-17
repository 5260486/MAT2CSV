import os
import re

class Filename:

    # get all filenames with one kind file type in a file.
    # and save them as txt.. 
    def write_filenames(folder_path,files):
        txt_path=os.path.join(folder_path, 'filenames.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            for name in files:
                name,ext = os.path.splitext(name)
                f.write(name + '\n')

        print(f"There are {len(files)} files in filenames.txt")

    # read filenames from txt
    def read_filenames(folder_path,name_of_txt):
        txt_path=os.path.join(folder_path, name_of_txt)
        with open(txt_path, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f.readlines()]
        return new_names

    def extract_digits_from_filename(filename, method):
        """
        从文件名中提取数字段，根据指定的方法选择数字段
        """
        # 使用正则表达式找到所有连续的数字段
        digits_list = re.findall(r'\d+', filename)
    
        if not digits_list:
            return None
    
        if method == 'first':
            return digits_list[0]
        elif method == 'longest':
            return max(digits_list, key=len)
        elif method == 'shortest':
            return min(digits_list, key=len)
        else:
            return None

    def get_extract_digits(filelist_B,method):
        # 从B中提取数字段
        B_digits = []
        for i, filename_B in enumerate(filelist_B):
            digits =Filename.extract_digits_from_filename(filename_B, method)
            if digits is None:
                print(f"警告: 文件B中的文件名 '{filename_B}' 没有数字段，将无法匹配。")
            B_digits.append(digits)
        return B_digits

    def find_B_digits_in_A(B_digits,filelist_A,filelist_B):
        # 匹配过程
        matched_pairs = []
        used_A_indices = set()  # 记录已经匹配的A文件索引
    
        # 遍历B中的每个文件名和对应的数字段
        for i, (b_file, b_digits) in enumerate(zip(filelist_B, B_digits)):
            if b_digits is None:
                matched_pairs.append((b_file, None))
                continue
            
            found = False
            # 在A中查找匹配的文件名
            for j, a_file in enumerate(filelist_A):
                if j in used_A_indices:
                    continue
                
                # 检查B的数字段是否包含在A的文件名中
                if b_digits in a_file:
                    matched_pairs.append((b_file, a_file))
                    used_A_indices.add(j)
                    found = True
                    break
                
            if not found:
                matched_pairs.append((b_file, None))
                print(f"警告: 对于B文件 '{b_file}' 数字段 '{b_digits}' 在A中找不到包含该数字段的文件名。")

        return matched_pairs
