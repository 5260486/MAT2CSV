
import os

from MyClass import Filename
from MyClass import CSVHelper

folder_path='D:\Personal\下载\csv_processor'
output_folder_path='D:\Personal\下载\csv_processor\sss'
csvfiles = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

Filename.Filename.write_filenames(folder_path,csvfiles)
csvnames =Filename.Filename.read_filenames(folder_path,'filenames.txt')

head_cut=1
tail_cut=0
for idx,filename in enumerate(csvfiles,1):
    input_file = os.path.join(folder_path, filename)
    output_file = os.path.join(output_folder_path, filename)

    CSVHelper.CSVHelper.cut_data(input_file,csvnames,head_cut,tail_cut,output_file)