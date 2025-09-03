import os
import re
from collections import OrderedDict

class Filename:

    # save filenames as txt,which both file name and path can be changed. 
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

    def select_all_num_in_filename(filename):
        return re.findall(r'\d+',filename)

    def select_num_in_filename(filename,pattern):
        match=re.search(pattern,filename)
        if match:
            return match.group()
        return None

    def get_user_selection(num_segments):
        if not num_segments:
            print("Don't find any number in filenames.")
            return None

        while True:
            try:
                choice_num=input("Please choose the piece of numbers you need."+
                "If you input '0',The program will be next step.").strip()

                if choice_num=='0':
                    return None
                choice_num=int(choice_num)
                if 1<=choice_num<=len(num_segments):
                    return num_segments[choice_num-1]
                else:
                    print("Your number is out of range. ")
            except ValueError:
                print("Please input a right number.")

    """
        a_filenames: filenames as a reference
        b_filenames: filenames to be modified
        pattern: the pattern how to match files. 
                If pattern=none,we use all number in B.
    """
    def match_filenames(a_filenames,b_filenames,pattern=None):
        matches=OrderedDict()
        unmatched_b = b_filenames.copy()
        
        for b_filename in b_filenames:
            # 提取B文件中的数字段
            if pattern:
                b_number = Filename.select_num_in_filename(b_filename, pattern)
            else:
                b_numbers = Filename.select_all_num_in_filename(b_filename)
                if not b_numbers:
                    continue
                # 可以选择不同的策略：最长、最短、第一个、最后一个等
                b_number = max(b_numbers, key=len)  # 最长的数字段
        
            if not b_number:
                continue
            
            # 在A文件中寻找匹配
            best_match = None
            best_score = 0

            for a_filename in a_filenames:
                # 提取A文件中的数字段
                if pattern:
                    a_number = Filename.select_num_in_filename(a_filename, pattern)
                else:
                    a_numbers = Filename.select_all_num_in_filename(a_filename)
                    if not a_numbers:
                        continue
                    a_number = max(a_numbers, key=len)  # 最长的数字段
            
                if a_number == b_number:
                    # 完全匹配，优先级最高
                    matches[b_filename] = a_filename
                    if b_filename in unmatched_b:
                        unmatched_b.remove(b_filename)
                    break
                elif a_number and b_number and a_number in b_number:
                    # 部分匹配，可以设置优先级
                    score = len(a_number) / len(b_number)
                    if score > best_score:
                        best_score = score
                        best_match = a_filename
        
            # 如果没有完全匹配，但找到了部分匹配
            if b_filename not in matches and best_match:
                matches[b_filename] = best_match
                if b_filename in unmatched_b:
                    unmatched_b.remove(b_filename)
    
        return matches, unmatched_b





