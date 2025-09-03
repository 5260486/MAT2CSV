# -*- coding: utf-8 -*-#
from fileinput import filename
import os

import Filename
import Mat2Csv


# 1.Read all mat files, save their names to txt
folder_path=input("Please input the path of .mat files: ").strip()
#folder_path='E:/work+study/DigSilent/DataTreating/Data_5S_Italy_FRT_20250821'
# get all .mat files and sort
matfiles = [f for f in os.listdir(folder_path) if f.endswith('.mat')]
matfiles.sort()  # sort files by name, the way of sorting can be changed

Filename.FileName.write_filenames(folder_path,matfiles)
new_names =Filename.FileName.read_filenames(folder_path,'filenames.txt')

# 2.Transfer mat to csv in circle
for idx,filename in enumerate(matfiles,1):
	mat_path = os.path.join(folder_path, filename)
	new_csv_filename=Mat2Csv.Mat2CSV.transfer_mat_to_csv(folder_path,mat_path,new_names,idx)
	
	if idx==1:
		# get new headers.
		# The arrangement of columns in all file is same,
		# so we can update headers with serial number. 
		# If the arrangement is random, we need read every file and update headers.  
		new_headers,selected_columns = Mat2Csv.Header.header_choice(os.path.join(folder_path, new_csv_filename))

	Mat2Csv.Mat2CSV.extract_data_from_csv(folder_path,new_csv_filename,new_headers,selected_columns)
