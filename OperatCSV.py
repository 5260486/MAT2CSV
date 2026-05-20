
import os
from MyClass import Filename
from MyClass import CSVHelper

folder_path='D:\Personal\下载\新建文件夹'
output_folder_path='D:\Personal\下载\新建文件夹\sss'
csvfiles = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

Filename.Filename.write_filenames(folder_path,csvfiles)
csvnames =Filename.Filename.read_filenames(folder_path,'filenames.txt')

target_col='current'
operation='/'
operate_value=0.9

for idx,filename in enumerate(csvfiles,1):
    input_file = os.path.join(folder_path, filename)
    output_file = os.path.join(output_folder_path, filename)

    CSVHelper.CSVHelper.operate_column(input_file,target_col,operation,operate_value,output_file)