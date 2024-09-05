from grid_search import execute_grid_search
from random_search import execute_random_search
from bayesian_search import execute_bayesian_search
from nsga2 import execute_nsga2
from generate_metrics import get_metrics

current_datetime_grid, exec_time_grid = execute_grid_search()
current_datetime_random = execute_random_search(exec_time_grid)
current_datetime_beq = execute_bayesian_search(exec_time_grid, 0.5, 0.5)
current_datetime_bmrr = execute_bayesian_search(exec_time_grid, 0.7, 0.3)
current_datetime_bmop = execute_bayesian_search(exec_time_grid, 0.3, 0.7)
current_datetime_nsga2 = execute_nsga2(exec_time_grid)

algorithms = [
    'grid_search',
    'random_search',
    'bayesian_search',
    'bayesian_search',
    'bayesian_search',
    'nsga2'
]

datetime_list = [
    current_datetime_grid,
    current_datetime_random,
    current_datetime_beq,
    current_datetime_bmrr,
    current_datetime_bmop,
    current_datetime_nsga2
]

get_metrics(algorithms, datetime_list)
