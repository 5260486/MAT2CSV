from MyClass import Header
import os
from MyClass import Mat2Csv
import pandas as pd

file_path = '........'

csvfiles = [f for f in os.listdir(file_path) if f.endswith('.csv')]
for item in csvfiles:
	Header.Header.merge_header(os.path.join(file_path,item),file_path,2)

