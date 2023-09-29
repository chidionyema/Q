
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from skopt import BayesSearchCV
from pyswarm import pso
from scipy.optimize import minimize
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
from deap import base, creator, tools, algorithms
import optuna


# --- Optimizers ---
class Optimizer(ABC):
    @abstractmethod
    def optimize(self, model, X_train, y_train):
        pass


# Define your model, X_train, and y_train

# 1. Randomized Search (using RandomizedSearchCV from scikit-learn)
class RandomSearchOptimizer(Optimizer):
    def __init__(self, param_distributions, n_iter=100):
        self.param_distributions = param_distributions
        self.n_iter = n_iter

    def optimize(self, model, X_train, y_train):
        random_search = RandomizedSearchCV(model.algorithm_instance, self.param_distributions, n_iter=self.n_iter)
        random_search.fit(X_train, y_train)
        model.algorithm_instance = random_search.best_estimator_

# 2. Bayesian Optimization (using BayesSearchCV from scikit-learn)
class BayesianOptimizer(Optimizer):
    def __init__(self, param_space, n_iter=50):
        self.param_space = param_space
        self.n_iter = n_iter

    def optimize(self, model, X_train, y_train):
        bayes_search = BayesSearchCV(model.algorithm_instance, self.param_space, n_iter=self.n_iter)
        bayes_search.fit(X_train, y_train)
        model.algorithm_instance = bayes_search.best_estimator_

# 3. Particle Swarm Optimization (PSO) - using pyswarm
class PSOOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train):
        def loss_function(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            return -1 * model.algorithm_instance.score(X_train, y_train)

        lb = [0.001, 1]  # Lower bounds for parameters, e.g., learning rate and regularization
        ub = [0.1, 100]  # Upper bounds

        xopt, fopt = pso(loss_function, lb, ub)
        optimal_parameters = dict(zip(['param1', 'param2'], xopt))
        model.algorithm_instance.set_params(**optimal_parameters)

# 4. Simulated Annealing - using scipy.optimize
class SimulatedAnnealingOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train):
        def loss_function(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            return -1 * model.algorithm_instance.score(X_train, y_train)

        result = minimize(loss_function, [0.01, 10], method='SLSQP')
        optimal_parameters = dict(zip(['param1', 'param2'], result.x))
        model.algorithm_instance.set_params(**optimal_parameters)

# 5. Tree-structured Parzen Estimator (TPE) - using hyperopt
class TPEOptimizer(Optimizer):
    def __init__(self, space):
        self.space = space

    def optimize(self, model, X_train, y_train):
        def objective(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            loss = -1 * model.algorithm_instance.score(X_train, y_train)
            return {'loss': loss, 'status': STATUS_OK}

        trials = Trials()
        best = fmin(fn=objective, space=self.space, algo=tpe.suggest, max_evals=100, trials=trials)
        model.algorithm_instance.set_params(**best)

# 6. Optuna CMA-ES Optimization - using optuna
class OptunaCMAESOptimizer(Optimizer):
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def optimize(self, model, X_train, y_train):
        sampler = optuna.samplers.CmaEsSampler()
        study = optuna.create_study(sampler=sampler, direction='minimize')
        study.optimize(self.objective_function, n_trials=100)
        best_params = study.best_params
        model.algorithm_instance.set_params(**best_params)

# 7. Differential Evolution (DEAP GA Optimization) - using deap
from deap import base, creator, tools, algorithms

class DEAPGAOptimizer(Optimizer):
    def __init__(self, objective_function, toolbox):
        self.objective_function = objective_function
        self.toolbox = toolbox  # DEAP's toolbox

    def optimize(self, model, X_train, y_train):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Sample a population and evolve it using a genetic algorithm
        population = self.toolbox.population(n=100)
        algorithms.eaSimple(population, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=100)

        # Extract the best individual's parameters and set them to the model
        best_individual = tools.selBest(population, k=1)[0]
        best_params = dict(zip(model.parameters_keys, best_individual))
        model.algorithm_instance.set_params(**best_params)

# 8. Grid Search (using GridSearchCV from scikit-learn)
class GridSearchOptimizer(Optimizer):
    def __init__(self, param_grid):
        self.param_grid = param_grid

    def optimize(self, model, X_train, y_train):
        grid_search = GridSearchCV(model.algorithm_instance, self.param_grid)
        grid_search.fit(X_train, y_train)
        model.algorithm_instance = grid_search.best_estimator_



# 10. Nelder-Mead Optimization (using scipy.optimize)
class NelderMeadOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train):
        def loss_function(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            return -1 * model.algorithm_instance.score(X_train, y_train)

        result = minimize(loss_function, [0.01, 10], method='Nelder-Mead')
        optimal_parameters = dict(zip(['param1', 'param2'], result.x))
        model.algorithm_instance.set_params(**optimal_parameters)





# 17. Sequential Model-Based Optimization (SMBO) (Placeholder - Custom Implementation Required)
class SMOptimization(Optimizer):
    def optimize(self, model, X_train, y_train):
        # Implement sequential model-based optimization (SMBO) here
        pass






import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from skopt import BayesSearchCV
from sklearn.model_selection import RandomizedSearchCV
from deap import base, creator, tools, algorithms
import ray
from ray.tune.sklearn import TuneSearchCV
from copy import deepcopy
import random

# Assuming data has already been split into X_train, X_test, y_train, y_test

class Optimizer:
    """Base Optimizer class. All custom optimizers should inherit from this."""
    def optimize(self, model, X_train, y_train):
        raise NotImplementedError("Subclasses must implement `optimize`")

from deap import gp, base, creator, tools, algorithms
import operator
import numpy as np

class GeneticProgrammingOptimizer(Optimizer):
    
    def __init__(self, lag_range=(1, 6), 
                 primitives=None, 
                 mate_func=gp.cxOnePoint, 
                 mutate_func=gp.mutUniform,
                 select_func=tools.selTournament, 
                 tournsize=3, 
                 min_depth=1, 
                 max_depth=5,
                 stats_funcs=None):
        
        self.lag_range = lag_range
        self.mate_func = mate_func
        self.mutate_func = mutate_func
        self.select_func = select_func
        self.tournsize = tournsize
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.primitives = primitives or [operator.add, operator.sub, operator.mul]
        
        # Default statistics if none provided
        self.stats_funcs = stats_funcs or {
            "avg": np.mean,
            "std": np.std,
            "min": np.min,
            "max": np.max
        }
        
        self.pset = self._define_primitives()
        self.toolbox = self._setup_toolbox()

    def _define_primitives(self):
        """Defines and returns the primitive set for GP."""
        pset = gp.PrimitiveSetTyped("main", [], float)
        for primitive in self.primitives:
            pset.addPrimitive(primitive, [float, float], float)
        for lag in range(self.lag_range[0], self.lag_range[1]):
            pset.addTerminal(float(lag), float, name=f"Lag_{lag}")
        return pset

    def _setup_toolbox(self):
        """Configures and returns DEAP's toolbox for GP."""
        toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=self.pset)
        
        toolbox.register("expr", gp.genHalfAndHalf, pset=self.pset, min_=self.min_depth, max_=self.max_depth)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("compile", gp.compile, pset=self.pset)
        
        toolbox.register("evaluate", self._evaluate)
        toolbox.register("select", self.select_func, tournsize=self.tournsize)
        toolbox.register("mate", self.mate_func)
        toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
        toolbox.register("mutate", self.mutate_func, expr=toolbox.expr_mut, pset=self.pset)
        
        return toolbox

    def _evaluate(self, individual):
        """Evaluation function for optimization."""
        func = self.toolbox.compile(expr=individual)
        predictions = [func() for _ in range(len(X_test))]
        mse = mean_squared_error(y_test, predictions)
        return mse,

    def optimize(self, model, X_train, y_train, ngen=50, pop_size=100, crossover_prob=0.7, mutation_prob=0.3):
        """Main optimization function."""
        population = self.toolbox.population(n=pop_size)
        hof = tools.HallOfFame(1)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        for key, func in self.stats_funcs.items():
            stats.register(key, func)

        algorithms.eaSimple(population, self.toolbox, crossover_prob, mutation_prob, ngen, stats, halloffame=hof)
        
        # Return the best strategy as a callable function
        best_expr = hof[0]
        best_func = self.toolbox.compile(expr=best_expr)
        return best_func


# 1. Hill Climbing
class HillClimbingOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train, param_ranges, max_iter=100):
        current_params = model.get_params()
        best_mse = float('inf')
        
        for _ in range(max_iter):
            new_params = deepcopy(current_params)
            for param, (lower, upper) in param_ranges.items():
                change = random.uniform(-0.05, 0.05) * current_params[param]
                new_params[param] = int(current_params[param] + change)
                new_params[param] = max(min(new_params[param], upper), lower)
                
            model.set_params(**new_params)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            
            if mse < best_mse:
                best_mse = mse
                current_params = new_params
        
        model.set_params(**current_params)
        return model

# 2. Bayesian Optimization
class CustomBayesianOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train, search_space):
        bayes_search = BayesSearchCV(model, search_space, n_iter=50, n_jobs=-1, cv=5)
        bayes_search.fit(X_train, y_train)
        model.set_params(**bayes_search.best_params_)
        return model

# 3. Grid Search with Randomized Search
class GridSearchRandomizedOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train, param_dist, n_iter_search=50):
        random_search = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=n_iter_search)
        random_search.fit(X_train, y_train)
        model.set_params(**random_search.best_params_)
        return model

# 4. Population-Based Optimization using DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

class PopulationBasedOptimizer(Optimizer):
    def __init__(self):
        self.toolbox = base.Toolbox()
        # Example for n_estimators; can be extended for more hyperparameters
        self.toolbox.register("n_estimators", random.randint, 10, 200)
        self.toolbox.register("individual", tools.initCycle, creator.Individual, 
                              (self.toolbox.n_estimators,), n=1)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", self.evaluation_function)

    def evaluation_function(self, individual):
        model = RandomForestRegressor(n_estimators=individual[0])
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        return mse,

    def optimize(self, model, X_train, y_train, param_ranges, ngen=10, pop_size=50, mutation_prob=0.2, crossover_prob=0.8):
        population = self.toolbox.population(n=pop_size)
        algorithms.eaSimple(population, self.toolbox, crossover_prob, mutation_prob, ngen)
        best_individual = tools.selBest(population, 1)[0]
        best_params = {'n_estimators': best_individual[0]}
        model.set_params(**best_params)
        return model

# 5. RL-Based Hyperparameter Optimization using Ray Tune
class RLHyperparameterOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train, config, num_samples=10):
        ray.init(ignore_reinit_error=True)
        search = TuneSearchCV(model, config, n_iter=num_samples, early_stopping=True, max_iters=10)
        search.fit(X_train, y_train)
        model.set_params(**search.best_params_)
        return model
