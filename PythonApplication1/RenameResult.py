import os
import re
import Filename

def display_number_segments(filename, segments):
    """显示文件名中的数字段及其位置"""
    print(f"\n文件名: {filename}")
    print("数字段:")
    for i, segment in enumerate(segments, 1):
        print(f"{i}. {segment} (位置: {filename.find(segment)})")

def main():
    """主函数"""
    print("文件名匹配工具")
    print("=" * 50)
    
    # 获取文件路径
    # a_file = input("请输入A文件路径（标准文件名）: ").strip()
    # a_name_of_txt=input("a_name_of_txt: ").strip()
    # b_file = input("请输入B文件路径（需要匹配的文件名）: ").strip()
    # b_name_of_txt=input("b_name_of_txt: ").strip()
    
    a_file="D:/programs"
    a_name_of_txt="filenames.txt"
    b_file="D:/programs"
    b_name_of_txt="B_filenames.txt"

    # 验证文件存在
    if not os.path.exists(a_file):
        print(f"错误: A文件 {a_file} 不存在")
        return
    if not os.path.exists(b_file):
        print(f"错误: B文件 {b_file} 不存在")
        return
    
    # 读取文件名
    a_filenames = Filename.Filename.read_filenames(a_file,a_name_of_txt)
    b_filenames = Filename.Filename.read_filenames(b_file,b_name_of_txt)
    
    print(f"A文件中找到 {len(a_filenames)} 个文件名")
    print(f"B文件中找到 {len(b_filenames)} 个文件名")
    
    # 显示B文件示例
    print("\nB文件示例:")
    for i, filename in enumerate(b_filenames[:5], 1):
        print(f"{i}. {filename}")
    if len(b_filenames) > 5:
        print("...")
    
    # 让用户选择匹配模式
    print("\n请选择匹配模式:")
    print("1. 自动匹配最长的数字段")
    print("2. 手动选择数字段")
    choice = input("请输入选择 (1 或 2): ").strip()
    
    pattern = None
    if choice == "2":
        # 手动选择数字段
        sample_file = b_filenames[0] if b_filenames else ""
        segments = Filename.Filename.select_all_num_in_filename(sample_file)
        display_number_segments(sample_file, segments)
        selected_segment = Filename.Filename.get_user_selection(segments)
        
        if selected_segment:
            # 创建正则表达式模式来匹配选择的数字段
            pattern = re.escape(selected_segment)
            print(f"将使用数字段 '{selected_segment}' 进行匹配")
        else:
            print("将使用自动匹配模式")
    
    # 执行匹配
    print("\n开始匹配文件...")
    matches, unmatched = Filename.Filename.match_filenames(a_filenames, b_filenames, pattern)
    
    # 显示匹配结果
    print(f"\n匹配结果: 成功匹配 {len(matches)}/{len(b_filenames)} 个文件")
    
    if matches:
        print("\n匹配成功的文件:")
        for b, a in matches.items():
            print(f"{b} -> {a}")
    
    if unmatched:
        print("\n未匹配的文件:")
        for filename in unmatched:
            print(filename)
    
    # 保存结果到文件
    #output_file = input("\n请输入输出文件路径 (直接回车使用默认路径): ").strip()
    output_file="D:/programs/filename_matches.txt"
    if not output_file:
        output_file = "filename_matches.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            
            for b, a in matches.items():
                f.write(a+"\n")
            
            if unmatched:
                f.write("\n未匹配的文件:\n")
                for filename in unmatched:
                    f.write(f"{filename}\n")
        
        print(f"结果已保存到 {output_file}")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")

if __name__ == "__main__":
    main()