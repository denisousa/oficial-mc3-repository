from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.pntx import SinglePointCrossover
from nsga2_mutation import MyMutation
from nsga2_problem import MyProblem
import time

def execute_nsga2(exec_time_grid):
    algorithm = NSGA2(pop_size=10,
                    sampling=IntegerRandomSampling(),
                    crossover=SinglePointCrossover(),
                    mutation=MyMutation(),
                    eliminate_duplicates=True)

    
    exec_time_grid = str(exec_time_grid).split(' ')[0].split('.')[0]
    problem = MyProblem()
    result = minimize(problem,
                algorithm,
                get_termination("time", exec_time_grid), 
                seed=int(time.time()),
                verbose=True)
