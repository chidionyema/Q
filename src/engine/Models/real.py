from abc import ABC, abstractmethod
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from datetime import datetime, timedelta
import concurrent.futures
from collections import Counter
import pandas as pd
import yfinance as yf
import numpy as np

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

class RandomForest(BaseModel):
    def __init__(self, params=None):
        if not params:
            super().__init__("RandomForest", RandomForestClassifier())
        else:
            super().__init__("RandomForest", RandomForestClassifier(**params))

    def train(self, X_train, y_train):
        self.algorithm_instance.fit(X_train, y_train)

# --- Optimizers ---
class Optimizer(ABC):
    @abstractmethod
    def optimize(self, model, X_train, y_train):
        pass

class GridSearchOptimizer(Optimizer):
    def __init__(self, param_grid):
        self.param_grid = param_grid

    def optimize(self, model, X_train, y_train):
        grid_search = GridSearchCV(model.algorithm_instance, self.param_grid)
        grid_search.fit(X_train, y_train)
        model.algorithm_instance = grid_search.best_estimator_

# --- Model Builder ---
class ModelBuilder:
    def __init__(self, model_class, optimizer=None):
        self.model_class = model_class
        self.optimizer = optimizer

    def build(self, X_train, y_train):
        model = self.model_class()
        if self.optimizer:
            self.optimizer.optimize(model, X_train, y_train)
        else:
            model.train(X_train, y_train)
        return model

# --- Ensemble ---
class EnsembleStrategy(ABC):
    @abstractmethod
    def combine(self, predictions):
        pass

class AverageStrategy(EnsembleStrategy):
    def combine(self, predictions):
        """Assumes predictions are continuous values."""
        # Use numpy for more efficient array operations
        predictions_array = np.array(predictions)  # Shape should be (num_models, num_samples)
        return np.mean(predictions_array, axis=0)

class Ensemble:
 def __init__(self, models, strategy=None):
    if not models:
        raise ValueError("At least one model must be provided.")
        else:
            self.strategy = AverageStrategy()

    def train(self, X_train, y_train):
        for model in self.models:
            model.train(X_train, y_train)

    def predict(self, X):
    if len(self.models) == 1:
        return self.models[0].predict(X)
    predictions = [model.predict(X) for model in self.models]
    return self.strategy.combine(predictions)


# --- Data ---
class DataLoader:
    @staticmethod
    def fetch_stock_data_from_yahoo(symbol, start_date, end_date, interval="1d"):
        df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        df.reset_index(inplace=True)
        return df

class FeatureEngineer:
    def __init__(self, data=None):
        self.data = data

    def add_labels(self, data, target_column, prediction_period, lookback_period):
        data['SMA'] = data['Close'].rolling(window=lookback_period).mean()
        for column in data.columns:
            for i in range(1, lookback_period + 1):
                data[f'{column}_lag_{i}'] = data[column].shift(i)
            for i in range(1, prediction_period + 1):
                data[f'{target_column}_{i}_days_later'] = data[target_column].shift(-i)
        
        drop_columns = ['Close'] + [f'Close_{i}_days_later' for i in range(1, prediction_period + 1)]
        label_columns = [f'Close_{i}_days_later' for i in range(1, prediction_period + 1)]
        X = data.drop(columns=drop_columns).values
        y = data[label_columns].values
        return X, y
def sequential_split(X, y, train_size=0.7, val_size=0.2):
    train_end = int(train_size * len(X))
    val_end = int((train_size + val_size) * len(X))
    
    X_train = X[:train_end]
    y_train = y[:train_end]
    
    X_val = X[train_end:val_end]
    y_val = y[train_end:val_end]
    
    X_test = X[val_end:]
    y_test = y[val_end:]
    
    return X_train, X_val, X_test, y_train, y_val, y_test

# --- Pipeline ---
class Pipeline:
    LOOKBACK_PERIOD = 14
    PREDICTION_PERIOD = 3
   
    def __init__(self, feature_engineer, model_builders, stock_symbol, user_start_date="2011-01-30", end_date="2021-12-31"):
        self.feature_engineer = feature_engineer
        self.model_builders = model_builders
        self.stock_symbol = stock_symbol
        self.user_start_date = user_start_date
        self.end_date = end_date
        self.system_start_date = self.adjust_start_date(user_start_date, Pipeline.LOOKBACK_PERIOD)
        self.models = []
        self.ensemble = None

    @staticmethod
    def adjust_start_date(user_start_date_str, lookback_period):
        user_start_date = datetime.strptime(user_start_date_str, "%Y-%m-%d")
        system_start_date = user_start_date - timedelta(days=lookback_period)
        return system_start_date.strftime("%Y-%m-%d")

    def prep(self):
        df = DataLoader.fetch_stock_data_from_yahoo(self.stock_symbol, self.system_start_date, self.end_date)
        datasets_to_process = [df.iloc[i - self.LOOKBACK_PERIOD:i + self.PREDICTION_PERIOD] for i in range(self.LOOKBACK_PERIOD, len(df) - self.PREDICTION_PERIOD + 1)]
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.feature_engineer.add_labels, dataset, 'Close', self.PREDICTION_PERIOD, self.LOOKBACK_PERIOD) for dataset in datasets_to_process]
        return [future.result() for future in futures]

    def run(self):
        processed_data_list = self.prep()
        aggregated_X = []
        aggregated_y = []

        for X, y in processed_data_list:
            aggregated_X.extend(X)
            aggregated_y.extend(y)

        aggregated_X = np.array(aggregated_X)
        aggregated_y = np.array(aggregated_y)
        X_train, X_val, X_test, y_train, y_val, y_test = sequential_split(aggregated_X, aggregated_y)

       

        self.models = [builder.build(aggregated_X, aggregated_y) for builder in self.model_builders]
        self.ensemble = Ensemble(self.models)
        self.ensemble.train(aggregated_X, aggregated_y)

    def begin_predict(self, new_data):
        return self.ensemble.predict(new_data)

if __name__ == "__main__":
    rf_builder = ModelBuilder(RandomForest, optimizer=GridSearchOptimizer(param_grid={"n_estimators": [10, 50, 100]}))
    fe = FeatureEngineer()
    pipeline = Pipeline(fe, [rf_builder], "AAPL")
    pipeline.run()
    for idx, (X, y) in enumerate(results):
        print(f"\n--- Dataset {idx + 1} ---")
        print("Features (X):")
        print(X)
        print("\nLabels (y):")
        print(y)

  