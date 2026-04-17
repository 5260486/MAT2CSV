from MyClass import Header
import os
from MyClass import Mat2Csv
import pandas as pd
file_path = 'E:\DigSilent\DataFitting\Austria-WTG-PQ\Dig Q'
#file_path = 'E:\PSCAD\West Australia/0. R1'
csvfiles = [f for f in os.listdir(file_path) if f.endswith('.csv')]
for item in csvfiles:
	Header.Header.merge_header(os.path.join(file_path,item),file_path,2)


# file_path = 'D:\Personal\桌面'
# csvfiles = [f for f in os.listdir(file_path) if f.endswith('.csv')]
# for idx,filename in enumerate(csvfiles,1):
# 	if idx==1:
# 		new_headers,selected_columns = Header.Header.header_choice(os.path.join(file_path, filename))

# 	Mat2Csv.Mat2CSV.extract_data_from_csv(file_path,filename,new_headers,selected_columns)
