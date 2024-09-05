from siamese_search import execute_siamese_search
from datetime import datetime
from itertools import product
import re
import yaml

current_datetime = datetime.now()

with open('parameters/parameters_grid_search.yml', 'r') as file:
    param = yaml.safe_load(file)
    param = [v for v in param.values()]

def cofigure_text(text):
    text = text.replace('minCloneSize-','')
    text = text.replace('ngramSize-','')
    text = text.replace('qrNorm-','')
    text = text.replace('normBoost-','')
    text = text.replace('t2Boost-','')
    text = text.replace('t1Boost-','')
    text = text.replace('origBoost-','')
    return text

def extract_numbers(text):
    pattern = r'-?\d+'
    numbers = re.findall(pattern, text)
    return numbers

def get_parameters_in_dict(text):
    numbers = [int(i) for i in extract_numbers(text)]
    return {
        "minCloneSize": numbers[0],
        "ngramSize": numbers[1],
        "qrNorm": numbers[2],
        "normBoost": numbers[3],
        "t2Boost": numbers[4],
        "t1Boost": numbers[5],
        "origBoost": numbers[6],
    }

def get_parameters_in_list(text):
    numbers = [int(i) for i in extract_numbers(text)]
    return {
        "minCloneSize": numbers[0],
        "ngramSize": numbers[1],
        "qrNorm": numbers[2],
        "normBoost": numbers[3],
        "t2Boost": numbers[4],
        "t1Boost": numbers[5],
        "origBoost": numbers[6],
    }

def get_combination(text):
    text = cofigure_text(text)
    return [int(i) for i in extract_numbers(text)]


def format_dimension(parms):
    return {'ngramSize' : parms[0],
            'minCloneSize' : parms[1],
            'QRPercentileNorm' : parms[2],
            'QRPercentileT2' : parms[3],
            'QRPercentileT1' : parms[4],
            'QRPercentileOrig' : parms[5], 
            'normBoost': parms[6],
            't2Boost': parms[7],
            't1Boost': parms[8],
            'origBoost': parms[9],
            'simThreshold': parms[10]}

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    parms['output_folder'] = f'./output/{parms["algorithm"]}/{current_datetime}'
    execute_siamese_search(**parms)

def execute_grid_search():
    combinations = list(product(*param))
    algorithm = 'grid_search'

    start_total_time = datetime.now()
    for i, combination in enumerate(combinations):
        i += 1

        print(f"\n\nCount {i}")
        print(f"Combination {combination}")

        start_time = datetime.now()
        evaluate_tool(combination)
        end_time = datetime.now()
        exec_time = end_time - start_time

        print(f"Runtime: {exec_time}")
        result_time_path = f'time_record/{algorithm}/{current_datetime}.txt'
        open(result_time_path, 'a').write('Success execution ')
        open(result_time_path, 'a').write( f'{combination} \nRuntime: {exec_time}\n\n')

    total_execution_time = end_time - start_total_time
    print(f"Total execution time: {total_execution_time}")
    open(result_time_path, 'a').write(f"\nTotal execution time: {total_execution_time}\n")
    
    return current_datetime, exec_time
