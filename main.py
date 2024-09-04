from grid_search import execute_grid_search
from random_search import execute_random_search
from bayesian_search import execute_bayesian_search
from nsga2 import execute_nsga2

exec_time_grid = execute_grid_search()
execute_random_search(exec_time_grid)
execute_bayesian_search(exec_time_grid, 0.5, 0.5)
execute_bayesian_search(exec_time_grid, 0.7, 0.3)
execute_bayesian_search(exec_time_grid, 0.3, 0.7)
execute_nsga2(exec_time_grid)