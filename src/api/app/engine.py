
from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from datetime import datetime, timedelta
import concurrent.futures
from collections import Counter
import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.impute import SimpleImputer
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor

# Define classes and functions you want to expose
__all__ = [
   
    'DataLoader',
    'OptimizerFactory',
    'GridSearchOptimizer',
    'ModelBuilder',
    'BaseModel',
    'RandomForest',  # Assuming RandomForest is a defined class
    'SVM',
    'GBM',
    'LogReg',
    'KNN',
    'NeuralNetwork',
    'XGBoost',
    'Optimizer',
    'RandomSearchOptimizer',
    'BayesianOptimizer',
    'PSOOptimizer',
    'SimulatedAnnealingOptimizer',
    'TPEOptimizer',
    'OptunaCMAESOptimizer',
    'DEAPGAOptimizer',
    'OptunaTPEOptimizer',
    'EnsembleStrategy',
    'ThresholdVotingStrategy',
    'BordaCountStrategy',
    'SoftVotingStrategy',
    'MaxVotingStrategy',
    'MinVotingStrategy',
    'ProductStrategy',
    'RankAveragingStrategy',
    'MajorityVoteStrategy',
    'AverageStrategy',
    'MappingLayer',
    # Add more class
    'Ensemble',
    'DataPreparation',
    'Pipeline2',
    'WalkForwardValidation',
    'TrainingCoordinator',
    # Add more as needed...
]
from abc import ABC, abstractmethod
from collections import Counter, defaultdict

from sklearn.model_selection import RandomizedSearchCV
from skopt import BayesSearchCV




# --- Models ---
class BaseModel(ABC):
    def __init__(self, name, algorithm_instance):
        self.name = name
        self.algorithm_instance = algorithm_instance

    @abstractmethod
    def train(self, X_train, y_train):
        pass

    def predict(self, X):
        return self.algorithm_instance.predict(X)
    
class EnsembleStrategy(ABC):
    @abstractmethod
    def combine(self, predictions):
        pass

# --- Optimizers ---
class Optimizer(ABC):
    @abstractmethod
    def optimize(self, model, X_train, y_train):
        pass

class OptimizerFactory:
    @staticmethod
    def create_optimizer(optimizer_name, **kwargs):
        """
        Factory method to create optimizer instances.

        :param optimizer_name: Name of the optimizer.
        :param kwargs: Additional keyword arguments specific to each optimizer.
        :return: An instance of the requested optimizer.
        """
        if optimizer_name == "GridSearch":
            return GridSearchOptimizer(**kwargs)
        elif optimizer_name == "RandomSearchOptimizer":
            return RandomSearchOptimizer(**kwargs)
        elif optimizer_name == "BayesianOptimizer":
            return BayesianOptimizer(**kwargs)
        elif optimizer_name == "PSOOptimizer":
            return PSOOptimizer(**kwargs)
        elif optimizer_name == "SimulatedAnnealingOptimizer":
            return SimulatedAnnealingOptimizer(**kwargs)
        elif optimizer_name == "TPEOptimizer":
            return TPEOptimizer(**kwargs)
        elif optimizer_name == "OptunaCMAESOptimizer":
            return OptunaCMAESOptimizer(**kwargs)
        elif optimizer_name == "DEAPGAOptimizer":
            return DEAPGAOptimizer(**kwargs)
        elif optimizer_name == "OptunaTPEOptimizer":
            return OptunaTPEOptimizer(**kwargs)
        else:
            raise ValueError(f"Optimizer '{optimizer_name}' not recognized.")

# Example usage




class RandomForest(BaseModel):
    def __init__(self, params=None):
        if not params:
            super().__init__("RandomForest", RandomForestRegressor())
        else:
            super().__init__("RandomForest", RandomForestRegressor(**params))
    
    def is_temporal():
        return False

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)





class GridSearchOptimizer(Optimizer):
    def __init__(self, param_grid):
        self.param_grid = param_grid

    def optimize(self, model, X_train, y_train):
        grid_search = GridSearchCV(model.algorithm_instance, self.param_grid)
        grid_search.fit(X_train, y_train)
        model.algorithm_instance = grid_search.best_estimator_

class RandomSearchOptimizer(Optimizer):
    def __init__(self, param_distributions, n_iter=100):
        self.param_distributions = param_distributions
        self.n_iter = n_iter

    def optimize(self, model, X_train, y_train):
        random_search = RandomizedSearchCV(model.algorithm_instance, self.param_distributions, n_iter=self.n_iter)
        random_search.fit(X_train, y_train)
        model.algorithm_instance = random_search.best_estimator_

class BayesianOptimizer(Optimizer):
    def __init__(self, param_space, n_iter=50):
        self.param_space = param_space
        self.n_iter = n_iter

    def optimize(self, model, X_train, y_train):
        bayes_search = BayesSearchCV(model.algorithm_instance, self.param_space, n_iter=self.n_iter)
        bayes_search.fit(X_train, y_train)
        model.algorithm_instance = bayes_search.best_estimator_

from pyswarm import pso
from scipy.optimize import minimize

class PSOOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train):
        # Define a loss function to minimize. Note: This is a simple illustrative implementation and might need adjustments for real-world tasks.
        def loss_function(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            # Here, -1 is used because we want to maximize accuracy (or minimize -accuracy)
            return -1 * model.algorithm_instance.score(X_train, y_train)

        lb = [0.001, 1] # lower bounds for parameters, e.g., learning rate and regularization
        ub = [0.1, 100] # upper bounds 

        xopt, fopt = pso(loss_function, lb, ub)
        optimal_parameters = dict(zip(['param1', 'param2'], xopt))
        model.algorithm_instance.set_params(**optimal_parameters)

class SimulatedAnnealingOptimizer(Optimizer):
    def optimize(self, model, X_train, y_train):
        def loss_function(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            return -1 * model.algorithm_instance.score(X_train, y_train)

        result = minimize(loss_function, [0.01, 10], method='SLSQP')
        optimal_parameters = dict(zip(['param1', 'param2'], result.x))
        model.algorithm_instance.set_params(**optimal_parameters)
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK

class TPEOptimizer(Optimizer):
    def __init__(self, space):
        # space is the search space definition using hyperopt's hp module
        self.space = space

    def optimize(self, model, X_train, y_train):
        def objective(params):
            model.algorithm_instance.set_params(**params)
            model.algorithm_instance.fit(X_train, y_train)
            loss = -1 * model.algorithm_instance.score(X_train, y_train)
            return {'loss': loss, 'status': STATUS_OK}

        trials = Trials()
        best = fmin(fn=objective,
                    space=self.space,
                    algo=tpe.suggest,
                    max_evals=100,
                    trials=trials)

        model.algorithm_instance.set_params(**best)

class OptunaCMAESOptimizer(Optimizer):
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def optimize(self, model, X_train, y_train):
        sampler = optuna.samplers.CmaEsSampler()
        study = optuna.create_study(sampler=sampler, direction='minimize')
        study.optimize(self.objective_function, n_trials=100)
        
        best_params = study.best_params
        model.algorithm_instance.set_params(**best_params)
from deap import base, creator, tools, algorithms

class DEAPGAOptimizer:
    def __init__(self, objective_function, toolbox):
        self.objective_function = objective_function
        self.toolbox = toolbox  # DEAP's toolbox

    def optimize(self, model, X_train, y_train):
        # Assuming objective_function takes in an individual from the population
        # and evaluates it based on X_train and y_train
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        # Sample a population and evolve it using genetic algorithm
        population = self.toolbox.population(n=100)
        algorithms.eaSimple(population, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=100)
        
        # Extract the best individual's parameters and set them to the model
        best_individual = tools.selBest(population, k=1)[0]
        best_params = dict(zip(model.parameters_keys, best_individual))
        model.algorithm_instance.set_params(**best_params)


import optuna

class OptunaTPEOptimizer:
    def __init__(self, objective_function):
        self.objective_function = objective_function

    def optimize(self, model, X_train, y_train):
        # TPE is the default sampler in Optuna
        study = optuna.create_study(direction='minimize')
        study.optimize(self.objective_function, n_trials=100)
        
        best_params = study.best_params
        model.algorithm_instance.set_params(**best_params)


from sklearn.svm import SVC

class SVM(BaseModel):
    def __init__(self, params=None):
        super().__init__("SVM", SVC(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)
        
from sklearn.ensemble import GradientBoostingClassifier

class GBM(BaseModel):
    def __init__(self, params=None):
        super().__init__("GBM", GradientBoostingClassifier(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)

from sklearn.linear_model import LogisticRegression

class LogReg(BaseModel):
    def __init__(self, params=None):
        super().__init__("LogReg", LogisticRegression(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)

from sklearn.neighbors import KNeighborsClassifier

class KNN(BaseModel):
    def __init__(self, params=None):
        super().__init__("KNN", KNeighborsClassifier(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)

from sklearn.neural_network import MLPClassifier

class NeuralNetwork(BaseModel):
    def __init__(self, params=None):
        super().__init__("NeuralNetwork", MLPClassifier(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)

from xgboost import XGBClassifier

class XGBoost(BaseModel):
    def __init__(self, params=None):
        super().__init__("XGBoost", XGBClassifier(**params if params else {}))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)


class ThresholdVotingStrategy(EnsembleStrategy):
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        
    def combine(self, predictions):
        """Assumes predictions are probability values."""
        mean_prob = sum(predictions) / len(predictions)
        return 1 if mean_prob > self.threshold else 0

class BordaCountStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes each classifier ranks each class."""
        scores = defaultdict(int)
        for prediction in predictions:
            for rank, class_ in enumerate(prediction):
                scores[class_] += rank
        return min(scores, key=scores.get)

class SoftVotingStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes predictions are probability values."""
        summed = sum(predictions)
        avg = summed / len(predictions)
        return round(avg)

class MaxVotingStrategy(EnsembleStrategy):
    def combine(self, predictions):
        flattened_predictions = [pred for sublist in predictions for pred in sublist]
        return max(set(flattened_predictions), key=flattened_predictions.count)

class MinVotingStrategy(EnsembleStrategy):
    def combine(self, predictions):
        flattened_predictions = [pred for sublist in predictions for pred in sublist]
        return min(set(flattened_predictions), key=flattened_predictions.count)

class ProductStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes predictions are probability values between 0 and 1."""
        flattened_predictions = [pred for sublist in predictions for pred in sublist]
        product = 1
        for pred in flattened_predictions:
            product *= pred
        return product

class RankAveragingStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes classifiers return a ranking for each class."""
        averaged_rank = [sum(rank) / len(rank) for rank in zip(*predictions)]
        return averaged_rank.index(min(averaged_rank))

# Stacking would need a separate implementation since it would involve training another model.


class MajorityVoteStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Return the mode (most common) prediction."""
        flattened_predictions = [pred for sublist in predictions for pred in sublist]
        return Counter(flattened_predictions).most_common(1)[0][0]

class AverageStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes predictions are continuous values."""
        flattened_predictions = [pred for sublist in predictions for pred in sublist]
        return sum(flattened_predictions) / len(flattened_predictions)
    

class MappingLayer:
    models_mapping = {
    "SVM": SVM,
    "RandomForestRegressor": RandomForest,
    "LogReg": LogReg,
    "KNN": KNN,
    "NeuralNetwork": NeuralNetwork,
    "XGBoost": XGBoost,
    }

    optimizers_mapping = {
    "RandomSearch": RandomSearchOptimizer,
    "BayesianOptimizer": BayesianOptimizer,
    "PSO": PSOOptimizer,
    "SimulatedAnnealing": SimulatedAnnealingOptimizer,
    "TPE": TPEOptimizer,
    "OptunaCMAES": OptunaCMAESOptimizer,
    "DEAPGA": DEAPGAOptimizer,
    "OptunaTPE": OptunaTPEOptimizer,
    # Add other optimizers here
    }

    ensemble_strategies_mapping = {
    "ThresholdVoting": ThresholdVotingStrategy,
    "BordaCount": BordaCountStrategy,
    "SoftVoting": SoftVotingStrategy,
    "MaxVoting": MaxVotingStrategy,
    "MinVoting": MinVotingStrategy,
    "Product": ProductStrategy,
    "RankAveraging": RankAveragingStrategy,
    "MajorityVote": MajorityVoteStrategy,
# "Average": AverageStrategy,
    # Add other strategies here
}

class DataLoader:
    @staticmethod
    def fetch_stock_data_from_yahoo(symbol, start_date, end_date, interval="1d"):
        try:
            logging.info(f"Attempting to fetch data for symbol: {symbol} from {start_date} to {end_date} with interval {interval}")
            df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
            
            # Ensure data is sorted in ascending order by 'Date'
            df.sort_values(by='Date', inplace=True)

            df.reset_index(inplace=True)  # Reset the index
            df['Formatted_Date'] = df['Date'].dt.strftime("%Y-%m-%d")  # Format the 'Date' column as 'YYYY-MM-DD'
            
            logging.info(f"Data fetched successfully for symbol: {symbol}. Shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Error fetching data for symbol {symbol}: {str(e)}")
            raise


# --- Model Builder ---
class ModelBuilder:
    def __init__(self, model_class, optimizer=None):
        self.model_class = model_class
        self.optimizer = optimizer
        logging.info(f"model class: { self.model_class}. optiizer class: { self.optimizer}")

    def build(self, X_train, y_train):
        if isinstance(X_train, (list, tuple)):
            print(f"[ModelBuilder.build] Before any operations - X_train length: {len(X_train)}, y_train length: {len(y_train)}")
        else:
            # Assuming they are numpy arrays or pandas data structures
            print(f"[ModelBuilder.build] Before any operations - X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
        logging.info(f"model class: { self.model_class}. optiizer class: { self.optimizer}")

        model = self.model_class()
        
        if self.optimizer:
            self.optimizer.optimize(model, X_train, y_train)
        else:
            model.train(X_train, y_train)

        return model



class Ensemble:
    def __init__(self, models, strategy=None):
        if not models:
            raise ValueError("At least one model must be provided.")
        if isinstance(models, dict):
            self.models = list(models.values())
        else:
            self.models = models  # We ensure that models are stored as a list.
        
        if strategy:
            self.strategy = strategy
        else:
            self.strategy = AverageStrategy()

    def train(self, X_train, y_train):
        for model in self.models:
            model.train(X_train, y_train)

    def predict(self, X):
        if len(self.models) == 1:
            return self.models[0].predict(X)  # Accessing the first model directly, since it's a list.

        predictions = [model.predict(X) for model in self.models]
        return self.strategy.combine(predictions)

    def run(self):
        try:
            X, y = self.prep()
            X_train, X_val, X_test, y_train, y_val, y_test = sequential_split(X, y)

            self.models = [builder.build(X_train, y_train) for builder in self.model_builders]
            self.ensemble = Ensemble(self.models)
            self.ensemble.train(X_train, y_train)

            val_predictions = self.ensemble.predict(X_val)
            mae_val = mean_absolute_error(y_val, val_predictions)
            logging.info(f"Validation Mean Absolute Error: {mae_val}")

            test_predictions = self.ensemble.predict(X_test)
            mae_test = mean_absolute_error(y_test, test_predictions)
            logging.info(f"Test Mean Absolute Error: {mae_test}")

        except Exception as e:
            logging.error(f"Error in Pipeline run: {e}")
            logging.error(traceback.format_exc())
            return None

        return test_predictions

    def begin_predict(self, new_data):             
        return self.ensemble.predict(new_data)


      
class DataPreparation:
    LOOKBACK_PERIOD = 14
    PREDICTION_PERIOD = 3

    def __init__(self, dataset):
        self.dataset = dataset
        self.calculate_technical_indicators()  # Calculate technical indicators once

    @staticmethod
    def calculate_sma(data, window):
        """
        Calculate the Simple Moving Average (SMA) for a given window.

        :param data: Input data as a Pandas DataFrame.
        :param window: Window size for SMA calculation.
        :return: Series containing the SMA values.
        """
        print(f"Calculating SMA with a window of {window}...")
        # Use min_periods to handle NaN values
        return data['Close'].rolling(window=window, min_periods=1).mean()

    def calculate_technical_indicators(self):
        print("Calculating technical indicators...")
        self.dataset['SMA'] = self.calculate_sma(self.dataset, self.LOOKBACK_PERIOD)
        # You can add more technical indicators here
    
    def process_day(self, i):
        try:
            current_date = self.dataset.iloc[i]['Date']

            # Extract the historical data (past x days) and future data (next y days)
            historical_data = self.dataset.iloc[i - self.LOOKBACK_PERIOD:i + 1]  # Include current day

            if len(historical_data) < self.LOOKBACK_PERIOD + 1:
                # Not enough historical data for this day, skip processing
                return None

            future_data = self.dataset.iloc[i:i + self.PREDICTION_PERIOD]

            # Sort historical data by date in descending order (most recent first)
            historical_data = historical_data.sort_values(by='Date', ascending=False)

            # Extract the SMA values for historical data
            historical_sma_dates = historical_data['Date'].astype(str).tolist()  # Convert datetime to string
            historical_sma_values = historical_data['SMA'].tolist()

            # Sort future data by date in ascending order (future dates first)
            future_data = future_data.sort_values(by='Date')

            # Extract the closing prices for the future data
            future_closing_dates = future_data['Date'].astype(str).tolist()  # Convert datetime to string
            future_closing_prices = future_data['Close'].tolist()

            # Calculate the closing prices for the next y days
            next_y_closing_prices = future_closing_prices[:self.PREDICTION_PERIOD]

            # Extract Open, High, Low, and Volume for both historical and future data
            historical_open = historical_data['Open'].tolist()
            historical_high = historical_data['High'].tolist()
            historical_low = historical_data['Low'].tolist()
            historical_volume = historical_data['Volume'].tolist()

            future_open = future_data['Open'].tolist()
            future_high = future_data['High'].tolist()
            future_low = future_data['Low'].tolist()
            future_volume = future_data['Volume'].tolist()

            day_data = {
                'Current Date': current_date,
                'Historical Dates': [{'Date': date, 'SMA_14': sma_value, 'Open': open_val, 'High': high_val, 'Low': low_val, 'Volume': volume_val} 
                                    for date, sma_value, open_val, high_val, low_val, volume_val in zip(historical_sma_dates, historical_sma_values, historical_open, historical_high, historical_low, historical_volume)],
                'Future Dates': [{'Date': date, 'Close': closing_price, 'Open': open_val, 'High': high_val, 'Low': low_val, 'Volume': volume_val} 
                                for date, closing_price, open_val, high_val, low_val, volume_val in zip(future_closing_dates, future_closing_prices, future_open, future_high, future_low, future_volume)],
                'Target Prices': next_y_closing_prices  # Include target variable
            }

            # Ensure that the length of the 'Future Dates' list matches the prediction horizon (y)
            if len(day_data['Target Prices']) == self.PREDICTION_PERIOD:
                # print(f"Processed data for {current_date}")
                return day_data
            else:
                return None

        except Exception as e:
            print(f"Error processing data for {current_date}: {str(e)}")
            return None

    def process_days_concurrently(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.process_day, range(len(self.dataset))))

        # Filter out None values (skipped days)
        processed_data = [result for result in results if result is not None]

        return processed_data


    def prepare_data_structure(self):
        data_structure = []

        for i in range(self.LOOKBACK_PERIOD, len(self.dataset) - self.PREDICTION_PERIOD):
            day_data = self.process_day(i)
            data_structure.append(day_data)

        data_structure.sort(key=lambda x: x['Date'])

        print("Data structure preparation completed.")
        print(f"Data structure:\n{data_structure[:5]}")  # Print the first 5 entries for illustration
        return data_structure

class Pipeline2:
    def __init__(self, stocks_info):
        self.stocks_info = [(symbol, self.adjust_start_date(user_start_date, lookback_period), end_date, lookback_period, prediction_period, model_builder)
                            for symbol, user_start_date, end_date, lookback_period, prediction_period, model_builder in stocks_info]
        self.models = {}
        self.ensemble = None

    @staticmethod
    def adjust_start_date(user_start_date_str, lookback_period):
        user_start_date = pd.to_datetime(user_start_date_str)
        dates = pd.date_range(end=user_start_date, periods=lookback_period*2, freq='B')
        system_start_date = dates[0].date()
        print(f"[adjust_start_date] system_start_date: {system_start_date}")
        return system_start_date

    def load_data_serially(self):
        data_tuples = []
        for stock_info in self.stocks_info:
            print(f"[load_data_serially] Processing stock_info: {stock_info}")
            symbol, user_start_date, end_date, lookback_period, prediction_period, model_builder = stock_info
            system_start_date = self.adjust_start_date(user_start_date, lookback_period)
            dataset = DataLoader.fetch_stock_data_from_yahoo(symbol, system_start_date, end_date)
            if dataset is not None:
                data_tuples.append((stock_info, dataset))
        return data_tuples

    def load_data_concurrently(self):
        loaded_data = []
        with ThreadPoolExecutor() as executor:
            futures = {}
            for stock_info in self.stocks_info:
                symbol, user_start_date, end_date, lookback_period, prediction_period, model_builder = stock_info
                system_start_date = self.adjust_start_date(user_start_date, lookback_period)
                future = executor.submit(DataLoader.fetch_stock_data_from_yahoo, symbol, system_start_date, end_date)
                futures[future] = stock_info

            for future in futures:
                stock_info = futures[future]
                try:
                    dataset = future.result()
                    if dataset is not None:
                        loaded_data.append((stock_info, dataset))
                except Exception as e:
                    print(f"Error fetching data for {stock_info[0]}: {e}")

        return loaded_data

    def prep_data(self, dataset):
        data_prep = DataPreparation(dataset)
        data_structure = data_prep.process_days_concurrently()
        print(f"[prep_data] Prepared data structure length: {len(data_structure)}")
        return data_structure

    def prepare_data_concurrently(self, data_tuples):
        prepped_data = []
        with ThreadPoolExecutor() as executor:
            for stock_info, dataset in data_tuples:
                future = executor.submit(self.prep_data, dataset)
                prepped_data.append((stock_info, future))

        prepped_data = [(stock_info, future.result()) for stock_info, future in prepped_data]
        return prepped_data
    
    def train_and_evaluate(self, stock_info, X_train, y_train, X_val, y_val, X_test, y_test):
        """Trains models and evaluates their performance on validation and test data."""
        symbol, _, _, _, _, model_builder = stock_info
        try:
            
            self.models[symbol] = model_builder.build(X_train, y_train)
            
            self.ensemble = Ensemble(list(self.models.values()))

            self.ensemble.train(X_train, y_train)

            val_predictions = self.ensemble.predict(X_val)
            mae_val = mean_absolute_error(y_val, val_predictions)
            print(f"Validation Mean Absolute Error for {symbol}: {mae_val}")

            test_predictions = self.ensemble.predict(X_test)
            mae_test = mean_absolute_error(y_test, test_predictions)
            print(f"Test Mean Absolute Error for {symbol}: {mae_test}")

            return test_predictions, mae_val, mae_test  # Return test predictions, MAE on validation data, and MAE on test data

        except Exception as e:
            logging.error(f"Error in Pipeline run for {symbol}: {e}")
            logging.error(traceback.format_exc())
        return None, None, None  # Return None values if there is an error
# Return test predictions


    def extract_features_and_labels(self, processed_data, is_temporal_model):
        features = []
        labels = []

        for day_data in processed_data:
            historical_data = day_data['Historical Dates']
            feature_vector = [[historical_datum['SMA_14'], historical_datum['Open'], 
                            historical_datum['High'], historical_datum['Low'], 
                            historical_datum['Volume']] 
                            for historical_datum in historical_data]

            if not is_temporal_model:
                feature_vector = [item for sublist in feature_vector for item in sublist]

            features.append(feature_vector)
            labels.append(day_data['Target Prices'][0])

        print(f"[extract_features_and_labels] features: {len(features)}, labels: {len(labels)}")
        return features, labels

    def time_series_split(self, data, train_size, val_size):
        n = len(data)
        train_end = int(train_size * n)
        val_end = int(val_size * n) + train_end

        train = data[:train_end]
        val = data[train_end:val_end]
        test = data[val_end:]

        print(f"[time_series_split] train: {len(train)}, val: {len(val)}, test: {len(test)}")
        return train, val, test

    def split_data(self, stock_info, data, is_temporal_model, train_size=0.7, val_size=0.15):
        train_data, val_data, test_data = self.time_series_split(data, train_size, val_size)

        X_train, y_train = self.extract_features_and_labels(train_data, is_temporal_model)
        print(f"[split_data] X_train: {len(X_train)}, y_train: {len(y_train)}")

        X_val, y_val = self.extract_features_and_labels(val_data, is_temporal_model)
        print(f"[split_data] X_val: {len(X_val)}, y_val: {len(y_val)}")

        X_test, y_test = self.extract_features_and_labels(test_data, is_temporal_model)
        print(f"[split_data] X_test: {len(X_test)}, y_test: {len(y_test)}")

        return stock_info, (X_train, y_train, X_val, y_val, X_test, y_test)

    def prepare_data_for_ml(self, X_train, X_val, X_test):
        X_train_flattened = [self.flatten_data(sample) for sample in X_train]
        X_val_flattened = [self.flatten_data(sample) for sample in X_val]
        X_test_flattened = [self.flatten_data(sample) for sample in X_test]

        print(f"[prepare_data_for_ml] X_train_flattened: {len(X_train_flattened)}, X_val_flattened: {len(X_val_flattened)}, X_test_flattened: {len(X_test_flattened)}")
        return X_train_flattened, X_val_flattened, X_test_flattened


    @staticmethod
    def flatten_data(data):
        return [item for sublist in data for item in sublist]

    def process_data_pipeline(self, load_concurrently=False, train_size=0.7, val_size=0.15):
        if load_concurrently:
            data_tuples = self.load_data_concurrently()
        else:
            data_tuples = self.load_data_serially()

        prepped_data = self.prepare_data_concurrently(data_tuples)
        test_predictions_list = []

        for stock_info, data in prepped_data:
            split_result = self.split_data(stock_info, data, train_size, val_size)
            si, (X_train, y_train, X_val, y_val, X_test, y_test) = split_result

            print(f"[process_data_pipeline] Data dimensions BEFORE preprocessing - X_train: {len(X_train)}, X_val: {len(X_val)}, X_test: {len(X_test)}")

            X_train, X_val, X_test = self.prepare_data_for_ml(X_train, X_val, X_test)

            print(f"[process_data_pipeline] Data dimensions AFTER preprocessing - X_train: {len(X_train)}, X_val: {len(X_val)}, X_test: {len(X_test)}")

            test_predictions, mae_val, mae_test = self.train_and_evaluate(si, X_train, y_train, X_val, y_val, X_test, y_test)
            test_predictions_list.append((si, test_predictions, mae_val, mae_test))

        return test_predictions_list




    def begin_predict(self, new_data):             
        return self.ensemble.predict(new_data)

        from sklearn.metrics import mean_absolute_error

class WalkForwardValidation:
    def __init__(self, initial_train_size, validation_size, pipeline):
        self.initial_train_size = initial_train_size
        self.validation_size = validation_size
        self.pipeline = pipeline  # Instance of the Pipeline2 class
    
    def validate(self, data):
        performances = []
        predictions_list = []

        train_start = 0
        train_end = int(self.initial_train_size * len(data))
        val_end = train_end + int(self.validation_size * len(data))

        while val_end <= len(data):
            train_data = data[train_start:train_end]
            val_data = data[train_end:val_end]

            # Extract features and labels from train_data and val_data
            X_train, y_train = self.extract_features_labels(train_data)
            X_val, y_val = self.extract_features_labels(val_data)

            # Train and evaluate the model
            predictions = self.pipeline.train_and_evaluate(X_train, y_train, X_val, y_val, [], [])
            mae = mean_absolute_error(y_val, predictions)
            performances.append(mae)
            predictions_list.append(predictions)

            # Slide or expand the window
            train_end = val_end
            val_end = train_end + int(self.validation_size * len(data))

        return performances, predictions_list
    
    def extract_features_labels(self, data):
        # Define this method to appropriately extract features and labels from your data
        # This is just a placeholder and needs to be adapted based on your dataset
        X = [item['Historical Dates'] for item in data]
        y = [item['Target Prices'] for item in data]
        return X, y







