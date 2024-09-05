import pandas as pd
import random
from siamese_operations import format_siamese_output
from oracle_operations import filter_oracle
from skopt import gp_minimize
from skopt.space import Categorical
from skopt.utils import use_named_args
from siamese_search import execute_siamese_search
from generate_metrics import calculate_all_metrics
from datetime import datetime
from files_operations import most_recent_file
import yaml
import os

with open('parameters/parameters.yml', 'r') as file:
    param = yaml.safe_load(file)

n = []

for k,v in param.items():
    n.append(len(v) -1) 

dimensions=[Categorical(param['ngram'], name='ngramSize'),
            Categorical(param['minCloneSize'], name='minCloneSize'),
            Categorical(param['QRPercentileNorm'], name='QRPercentileNorm'),
            Categorical(param['QRPercentileT2'], name='QRPercentileT2'),
            Categorical(param['QRPercentileT1'], name='QRPercentileT1'),
            Categorical(param['QRPercentileOrig'], name='QRPercentileOrig'),
            Categorical(param['normBoost'], name='normBoost'),
            Categorical(param['t2Boost'], name='t2Boost'),
            Categorical(param['t1Boost'], name='t1Boost'),
            Categorical(param['origBoost'], name='origBoost'),
            Categorical(param['simThreshold'], name='simThreshold')]

def weighted_average(values, weights):
    if len(values) != len(weights):
        raise ValueError("Number of values must be equal to the number of weights.")
    
    total = sum(value * weight for value, weight in zip(values, weights))
    weight_sum = sum(weights)
    
    if weight_sum == 0:
        raise ValueError("Total weight cannot be zero.")
    
    return total / weight_sum

@use_named_args(dimensions)
def evaluate_tool(**parms):
    global exec_time_grid_global
    global current_datetime_global
    global mrr_weight_global
    global mop_weight_global

    current_datetime = current_datetime_global

    parms['algorithm'] = algorithm
    parms['output_folder'] = f'./output/{parms["algorithm"]}/{current_datetime}'
    siamese_output_path = parms['output_folder']

    start_time = datetime.now()
    execute_siamese_search(**parms)
    end_time = datetime.now()
    exec_time = end_time - start_time
    total_execution_time = end_time - start_total_time

    result_time_path = f'time_record/{algorithm}/{current_datetime}.txt'
    print(f"Runtime: {exec_time}")
    open(result_time_path, 'a').write(f'Success execution ')
    open(result_time_path, 'a').write( f'{list(parms.values())} \nRuntime: {exec_time}\n\n')

    most_recent_siamese_output, _ = most_recent_file(siamese_output_path)

    df_siamese = format_siamese_output(siamese_output_path, most_recent_siamese_output)
    folder_result = f'results_metrics/{algorithm}/{current_datetime}'
    metrics = calculate_all_metrics(most_recent_siamese_output, df_siamese, df_clones, folder_result)
    mrr = metrics["MRR (Mean Reciprocal Rank)"]
    mop = metrics["MOP (Mean Overall Precision)"]

    result = weighted_average([mrr, mop], [mrr_weight_global, mop_weight_global])
    
    loss = float(result) * -1

    if exec_time_grid_global <= total_execution_time:
        print(f"Total execution time: {total_execution_time}")
        open(result_time_path, 'a').write(f"\nTotal execution time: {total_execution_time}\n")
        print(f'Last Result - mrr:{mrr} | parms: {list(parms.values())}')
        raise Exception("Finish Bayesian Search")

    print(f'\n \n \nloss: {loss}\n \n \n')
    return loss


def execute_bayesian_search(exec_time_grid, mrr_weight, mop_weight):
    global exec_time_grid_global
    global current_datetime_global
    global mrr_weight_global
    global mop_weight_global

    current_datetime_global = datetime.now()

    exec_time_grid_global = exec_time_grid
    mrr_weight_global = mrr_weight
    mop_weight_global = mop_weight

    all_combinations = 4000
    seed = random.randint(1,51)
    print(f"SEED: {seed}\n")

    try:
        gp_minimize(evaluate_tool,
                    dimensions=dimensions,
                    n_calls=all_combinations,
                    random_state=seed)
    except:
        pass

    return current_datetime_global    
    
columns_parms = ['minCloneSize',
        'ngramSize',
        'QRPercentileNorm',
        'QRPercentileT2',
        'QRPercentileT1',
        'QRPercentileOrig',
        'normBoost',
        'T2Boost',
        'T1Boost',
        'origBoost',
        'simThreshold']

mrr_weight_global = None
mop_weight_global = None
current_datetime_global = None
exec_time_grid_global = exec_time_grid_global = None
algorithm = 'bayesian_search'
start_total_time = datetime.now()
df_clones = pd.read_csv('datasets/formatted_oracle.csv')
df_clones = filter_oracle(df_clones)
