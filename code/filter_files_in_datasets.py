import pandas as pd
import shutil
import os

def delete_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

def copy_files(file_paths, destination_folder):
    for file_path in file_paths:
        destination_path = os.path.join(destination_folder, file_path)
        file_path = os.path.join(source_folder, file_path)
        shutil.copy(file_path, destination_path)


file_name = 'new_clones.csv'
df = pd.read_csv(file_name)
column_file2 = df['file2'].tolist()

source_folder = 'my_projects/qualitas_corpus_clean'
destination_folder = 'my_projects/qualitas_corpus_clean_new'
copy_files(column_file2, destination_folder)
