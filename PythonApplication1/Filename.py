import os

class FileName:

    def __init__(self,foleder_path,files):
        self.folder_path=foleder_path
        self.files=files;

    # save filenames as txt,which both file name and path can be changed. 
    def write_filenames(self):
        txt_path=os.path.join(self.folder_path, 'filenames.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            for name in self.files:
                name, ext = os.path.splitext(name)
                f.write(name + '\n')

        print(f"There are {len(self.files)} files in filenames.txt")

    # read filenames from txt
    def read_filenames(self):
    
        txt_path=os.path.join(self.folder_path, 'filenames.txt')
        with open(txt_path, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f.readlines()]
        return new_names





