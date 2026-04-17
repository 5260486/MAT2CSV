import os
from MyClass.Filename import Filename

def main():
    
    b_file_path = 'E:\新建文件夹\A'
    b_csvfiles = [f for f in os.listdir(b_file_path) if f.endswith('.csv')]
    Filename.Filename.write_filenames(b_file_path,b_csvfiles)
    
    a_file_path ='E:\新建文件夹\B'
    a_csvfiles = [f for f in os.listdir(a_file_path) if f.endswith('.csv')]
    Filename.Filename.write_filenames(a_file_path,a_csvfiles)

    a_name_of_txt="filenames.txt"
    b_name_of_txt="filenames.txt"

    filelist_A=Filename.Filename.read_filenames(a_file_path,a_name_of_txt)
    filelist_B=Filename.Filename.read_filenames(b_file_path,b_name_of_txt)

    method = input("请选择从B中提取数字段的方式 (first, longest, shortest): ").strip().lower()
    # 验证输入
    if method not in ['first', 'longest', 'shortest']:
        print("错误: 提取方式必须是 'first', 'longest' 或 'shortest'")
        return

    # 检查文件A中的文件名数量是否大于等于文件B
    if len(filelist_A) < len(filelist_B):
        print("警告: 文件A中的文件名数目小于文件B，但要求A中文件名数目大于等于B。")
        return
    B_digits=Filename.Filename.get_extract_digits(filelist_B,method)
    matched_pairs=Filename.Filename.find_B_digits_in_A(B_digits,filelist_A,filelist_B)
    
    # 输出匹配结果
    print("\n匹配结果:")
    for b, a in matched_pairs:
        if a is None:
            print(f"{b} -> 无匹配")
        else:
            print(f"{b} -> {a}")
            filename_a=f"{a}.csv"
            old_path=os.path.join(a_file_path,filename_a)
            new_path=os.path.join(a_file_path,b)
            os.rename(old_path,f"{new_path}.csv")

if __name__ == "__main__":
    main()
