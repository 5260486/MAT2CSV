# -*- coding: utf-8 -*-#
import os

from MyClass import Filename
from MyClass import Mat2Csv
from MyClass import Header
from MyClass import CSVHelper

from MyClass.Metadata import AUTHOR, VERSION, DESCRIPTION
print(f"作者: {AUTHOR}")
print(f"版本 {VERSION}")
print(f"{DESCRIPTION} ")


# 1.Read all mat files, save their names to txt
folder_path=input("Please input the path of .mat files: ").strip()

# get all .mat files and sort
matfiles = [f for f in os.listdir(folder_path) if f.endswith('.mat')]
matfiles.sort()  # sort files by name, the way of sorting can be changed

Filename.Filename.write_filenames(folder_path,matfiles)
new_names =Filename.Filename.read_filenames(folder_path,'filenames.txt')

# 2.Transfer mat to csv in circle

datatype=input("Please input yout test data, VRT or PPC: ").strip()
if datatype =="VRT":
	csv_format_same=True
else:
	csv_format_same=False

for idx,filename in enumerate(matfiles,1):
	mat_path = os.path.join(folder_path, filename)
	new_csv_filename=Mat2Csv.Mat2CSV.transfer_mat_to_csv(folder_path,mat_path,new_names,idx)
	
	if csv_format_same:
		if idx==1:
			# get new headers.
			# The arrangement of columns in all file is same,
			# so we can update headers with serial number. 
			new_headers,selected_columns = Header.Header.header_choice(os.path.join(folder_path, new_csv_filename))

		CSVHelper.CSVHelper.extract_data_from_csv(folder_path,new_csv_filename,new_headers,selected_columns)
	# If the arrangement is random, we need read every file and update headers.  
	else:
		new_headers,selected_columns = Header.Header.header_choice(os.path.join(folder_path, new_csv_filename))
		CSVHelper.CSVHelper.extract_data_from_csv(folder_path,new_csv_filename,new_headers,selected_columns)

	

