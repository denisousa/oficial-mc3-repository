from grid_search import execute_grid_search
from generate_metrics import get_metrics
from download_datasource import download_projects
from siamese_indexing import execute_siamese_index_properties
import yaml
import datetime
import os


def create_folders(folder_list):
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder created: {folder}")
        else:
            print(f"Folder already exists: {folder}")



def execute_indexing(ngrams):
    for i in ngrams:
        start_time = datetime.datetime.now()
        execute_siamese_index_properties(i)
        end_time = datetime.datetime.now()
        exec_time = end_time - start_time

        print("Execution time:", exec_time)
        open('time_execution.txt', 'a').write(f'{exec_time}\n')

folders = [
    "configurations",
    "datasets",
    "output",
    "results_metrics",
    "results_excel",
    "time_record"
]
create_folders(folders)
download_projects()

with open('parameters/parameters_grid_search_mini.yml', 'r') as file:
    param = yaml.safe_load(file)
    param = [v for v in param.values()]

ngrams = param[0]

execute_indexing(ngrams)

current_datetime_grid, exec_time_grid = execute_grid_search()

algorithms = [
    'grid_search',
]

datetime_list = [
    current_datetime_grid,
]

get_metrics(algorithms, datetime_list)
