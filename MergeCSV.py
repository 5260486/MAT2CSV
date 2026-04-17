
import os

from MyClass import Filename
from MyClass import CSVHelper


folder_path='E:\DigSilent\DataTreating\DataFromRTDS\Austria-WTG-FRT\RTDS\Case03补做1105'
output_folder=folder_path
csvfiles = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

Filename.Filename.write_filenames(folder_path,csvfiles)
csvnames =Filename.Filename.read_filenames(folder_path,'filenames.txt')

group_num=7
CSVHelper.CSVHelper.merge_csv_by_name(folder_path,csvnames,group_num,output_folder)