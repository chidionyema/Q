import yfinance as yf
import numpy as np
import pandas as pd
import logging
from skopt import gp_minimize
from skopt.space import Integer, Real
from statsmodels.tsa.stattools import adfuller
from sklearn.model_selection import TimeSeriesSplit
import random
from functools import partial
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score 
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.utils.class_weight import compute_class_weight
from random import choices
import json
from sqlalchemy import create_engine
import pickle

import pandas as pd
import numpy as np

class TechnicalAnalysis:

    @staticmethod
    def calculate_atr(data, window=14):
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = np.abs(high - close.shift(1))
        tr3 = np.abs(low - close.shift(1))
        
        tr = np.maximum.reduce([tr1, tr2, tr3])
        tr_series = pd.Series(tr, index=data.index)
        atr = tr_series.rolling(window=window).mean()

        data['ATR'] = atr
        return data

    @staticmethod
    def calculate_EMA(data, short_window=12, long_window=26):
        data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
        data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
        return data

    @staticmethod
    def calculate_AdaptiveBollingerBands(data, window=20, sensitivity=2):
        if len(data) < window:
            actual_window = len(data)
        else:
            actual_window = window
        
        median = data['Close'].rolling(window=actual_window).median()
        rolling_std = data['Close'].rolling(window=actual_window).std()
        volatility = rolling_std / median
        adaptive_window = np.floor(actual_window * (1 / (1 + sensitivity * volatility)))
    
        adaptive_sma = data['Close'].rolling(window=adaptive_window.astype(int)).mean()
        adaptive_std = data['Close'].rolling(window=adaptive_window.astype(int)).std()
    
        data['Adaptive_Upper_Band'] = adaptive_sma + (adaptive_std * 2)
        data['Adaptive_Lower_Band'] = adaptive_sma - (adaptive_std * 2)
        return data

    @staticmethod
    def calculate_FibonacciLevels(data, window=50):
        high = data['High'].rolling(window=window).max()
        low = data['Low'].rolling(window=window).min()
        diff = high - low
        data['Fib_38.2'] = high - 0.382 * diff
        data['Fib_50'] = high - 0.5 * diff
        data['Fib_61.8'] = high - 0.618 * diff
        return data

    @staticmethod
    def calculate_KeltnerChannels(data, atr_window=14, multiplier=1.5):
        middle_line = data['Close'].ewm(span=atr_window, adjust=False).mean()
        atr = TechnicalAnalysis.calculate_atr(data, atr_window)['ATR']
        data['Keltner_Upper'] = middle_line + multiplier * atr
        data['Keltner_Lower'] = middle_line - multiplier * atr
        return data

    @staticmethod
    def calculate_SMA(data, sma_short, sma_long):
        data['SMA_Short'] = data['Close'].rolling(window=sma_short).mean()
        data['SMA_Long'] = data['Close'].rolling(window=sma_long).mean()
        return data

    @staticmethod
    def calculate_bollinger_bands(data, window, num_std_dev):
        sma = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        data['Upper_Band'] = sma + (rolling_std * num_std_dev)
        data['Lower_Band'] = sma - (rolling_std * num_std_dev)
        return data

    @staticmethod
    def calculate_support_resistance(data, window):
        data['Support'] = data['Low'].rolling(window=window).min()
        data['Resistance'] = data['High'].rolling(window=window).max()
        return data

    @staticmethod
    def calculate_rsi(data, window=14):
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        data['RSI'] = rsi
        return data

    @staticmethod
    def calculate_MACD(data, short_window=12, long_window=26, signal_window=9):
        data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
        data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
        data['MACD'] = data['EMA_Short'] - data['EMA_Long']
        data['MACD_Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        return data

    @staticmethod
    def calculate_StochasticOscillator(data, k_window=14, d_window=3):
        high = data['High'].rolling(window=k_window).max()
        low = data['Low'].rolling(window=k_window).min()
        data['%K'] = 100 * ((data['Close'] - low) / (high - low))
        data['%D'] = data['%K'].rolling(window=d_window).mean()
        return data

    @staticmethod
    def calculate_OBV(data):
        obv = (np.sign(data['Close'].diff(1)) * data['Volume']).fillna(0).cumsum()
        data['OBV'] = obv
        return data

# Utilize the class as per requirement on your DataFrame.


class UtilityFunctions:
    @staticmethod
    def transaction_cost(price, volume):
        cost = price * volume * SETTINGS['commission'] + (price * volume * SETTINGS['slippage'])
        return cost

    @staticmethod
    def sharpe_ratio(portfolio_value):
        returns = np.diff(portfolio_value)
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
        return sharpe_ratio

    @staticmethod
    def check_stationarity(data):
        result = adfuller(data)
        return result[1] <= 0.05

    @staticmethod
    def position_size(portfolio_value, risk_percentage, stop_loss_percentage, current_price, atr, rsi):
        risk_per_trade = portfolio_value * risk_percentage
        stop_loss = current_price - (current_price * stop_loss_percentage)
        position_size = risk_per_trade / (current_price - stop_loss)
        return position_size

class PortfolioReportManager:
    """Generate and log reports related to portfolio performance."""

    def __init__(self, portfolio):
        self.portfolio = portfolio
        logging.basicConfig(filename='portfolio_reports.log', level=logging.INFO)

    def calculate_total_return(self):
        return self.portfolio.get_balance() - self.portfolio.cash

    def calculate_total_return_percentage(self):
        return self.calculate_total_return() * 100

    def log_equity(self):
        report = {
            'initial_balance': 1000000,
            'final_balance': self.portfolio.get_balance(),
            'total_return': self.calculate_total_return(),
            'total_return_percentage': self.calculate_total_return_percentage(),
            'positions': self.portfolio.positions  # Assuming this attribute exists
        }
        

        # Also print
        print("Portfolio Report:")
        print(report)      
class RiskVisualizationManager:
    """Visualize risk metrics based on RiskManager data."""
    
    def __init__(self, risk_manager):
        self.risk_manager = risk_manager
    
    def plot_equity_curve(self):
        """Plot the equity curve."""
        plt.figure()
        plt.title('Equity Curve')
        plt.plot(self.risk_manager.equity_curve)
        plt.xlabel('Time')
        plt.ylabel('Portfolio Value')
        plt.show()
        
    def plot_daily_returns(self):
        """Plot daily returns."""
        plt.figure()
        plt.title('Daily Returns')
        plt.plot(self.risk_manager.daily_returns)
        plt.xlabel('Time')
        plt.ylabel('Daily Return')
        plt.show()

    def plot_histogram_daily_returns(self):
        """Plot a histogram of daily returns."""
        plt.figure()
        plt.title('Histogram of Daily Returns')
        plt.hist(self.risk_manager.daily_returns, bins=50, alpha=0.75)
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        plt.show()

    def generate_visual_report(self):
        """Generate a full visual risk report."""
        self.plot_equity_curve()
        self.plot_daily_returns()
        self.plot_histogram_daily_returns()

class LabelGenerator:
    def generate_labels(self, data):
        raise NotImplementedError("Subclasses must implement generate_labels")

class FeatureSelector:
    def select_features(self, data):
        raise NotImplementedError("Subclasses must implement select_features")

class ModelTrainer:
    def train_model(self, data, model):
        raise NotImplementedError("Subclasses must implement train_model")


# Custom FeatureSelector
class DefaultFeatureSelector:
    def select_features(self, data):
        # Extract feature selection logic based on data types
        numeric_features = ['ATR', 'SMA_Short', 'SMA_Long', 'Upper_Band', 'Lower_Band', 'Support', 'Resistance', 'RSI']
        selected_features = data[numeric_features].copy()
        return selected_features

class GridSearchModelTrainer:
    def train_model(self, X_train, y_train, model):
        # Extract model training logic from the original code
        # Example: Train the model using your custom logic
        # Here, we're using grid search with a RandomForestClassifier as an example
        param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20, 30]}
        tscv = TimeSeriesSplit(n_splits=5)
    
        grid_search = GridSearchCV(model, param_grid, cv=tscv, scoring='f1')
        grid_search.fit(X_train, y_train)
        trained_model = grid_search.best_estimator_
        return trained_model

class DefaultLabelGenerator:
    def generate_labels(self, data):
        data['Signal'] = 0.0
        data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1.0
        data.loc[data['SMA_Short'] <= data['SMA_Long'], 'Signal'] = -1.0
        data.dropna(inplace=True)
        return data  # Returning DataFrame instead of Series

class DefaultDataPreparator:
    def prepare_data(self, data):
        # Assuming TechnicalAnalysis.calculate_* methods return DataFrames
        data = TechnicalAnalysis.calculate_atr(data)
        data = TechnicalAnalysis.calculate_SMA(data, sma_short=50, sma_long=200)
        data = TechnicalAnalysis.calculate_bollinger_bands(data, window=20, num_std_dev=2)
        data = TechnicalAnalysis.calculate_support_resistance(data, window=20)
        data = TechnicalAnalysis.calculate_rsi(data)
        data.dropna(inplace=True)
        return data  # Assuming this returns a DataFrame


class DefaultDataSplitter:
    def split_data(self, data):
        X = data.drop("Signal", axis=1)
        y = data["Signal"]
        
        # First, create the training and a temp set
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, shuffle=False)
        
        # Then, create the validation and test sets from the temp set
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)
        
        return X_train, X_val, X_test, y_train, y_val, y_test


# Define the builder class
class RandomForestTradingModelBuilder:
    def __init__(self):
        self.model = RandomForestTradingModel()
    
    def set_symbol(self, symbol):
        self.model.symbol = symbol
        return self

    def set_data(self, data):
        self.model.data = data
        return self

    def set_label_generator(self, label_generator):
        self.model.label_generator = label_generator
        return self

    def set_feature_selector(self, feature_selector):
        self.model.feature_selector = feature_selector
        return self

    def set_model_trainer(self, model_trainer):
        self.model.model_trainer = model_trainer
        return self

    def set_data_preparator(self, data_preparator):
        self.model.data_preparator = data_preparator
        return self

    def set_data_splitter(self, data_splitter):
        self.model.data_splitter = data_splitter
        return self

    def set_model_params(self, n_estimators, max_depth):
        self.model.model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        return self

    def build(self):
        return self.model
            
class RandomForestTradingModel:
    def __init__(self):
        self.label_generator = None
        self.feature_selector = None
        self.data_preparator = None
        self.data_splitter = None
        self.model_trainer = None
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.selected_features = None
        self.feature_columns = None
        self.all_features = None

    def prepare_data(self, data):
        self.data = self.data_preparator.prepare_data(data)
        self.data = self.label_generator.generate_labels(self.data)
        self.data.dropna(inplace=True)

    def train(self):    
        self.prepare_data(data)  # Assuming 'data' is defined somewhere or passed as an argument
        X = self.data.drop("Signal", axis=1)
        y = self.data["Signal"]

        # Split the data
        X_train, X_val, X_test, y_train, y_val, y_test = self.data_splitter.split_data(self.data)

        # Feature selection
        self.selected_features = self.feature_selector.select_features(X_train)
        self.feature_columns = self.selected_features.columns.tolist()
        
        # Use GridSearchModelTrainer for hyperparameter tuning
        trainer = GridSearchModelTrainer()
        self.model = trainer.train_model(X_train[self.feature_columns], y_train, self.model)
        
        # Validate the model
        y_val_pred = self.model.predict(X_val[self.feature_columns])
        val_accuracy = accuracy_score(y_val, y_val_pred)
        val_f1 = f1_score(y_val, y_val_pred, average='weighted')
        print(f"Validation Accuracy: {val_accuracy}, F1 Score: {val_f1}")


    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'selected_features': self.selected_features,
                'feature_columns': self.feature_columns
            }, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.selected_features = data['selected_features']
            self.feature_columns = data['feature_columns']

    def predict(self, feature_vector):
        try:
            return self.model.predict(feature_vector)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def predict_proba(self, feature_vector):
        try:
            return self.model.predict_proba(feature_vector)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

class LSTMModel:
    def __init__(self, look_back):
        self.look_back = look_back
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(look_back, 4)),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

class LSTMModelTrainer(ModelTrainer):
    def train_model(self, X, y, model):
        tscv = TimeSeriesSplit(n_splits=5)
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            model.fit(X_train, y_train, epochs=10, batch_size=64)

class LSTMTradingModelBuilder:
    def __init__(self):
        self.model = LSTMModel(look_back=60)
    
    def set_data(self, data):
        self.data = data
        return self

    def set_label_generator(self, label_generator):
        self.label_generator = label_generator
        return self

    def set_feature_selector(self, feature_selector):
        self.feature_selector = feature_selector
        return self

    def set_model_trainer(self, model_trainer):
        self.model_trainer = model_trainer
        return self

    def build(self):
        data = self.data
        data = self.label_generator.generate_labels(data)
        selected_features = self.feature_selector.select_features(data)
        
        X = selected_features.values
        y = data['Signal'].values

        self.model_trainer.train_model(X, y, self.model)
        return self.model

class AdvancedModel:
    def __init__(self, data):
        self.data = data
        
        # Initialize various models
        self.rf_model = RandomForestClassifier(random_state=42)
        self.svm_model = SVC(probability=True, kernel='rbf', C=1.0, gamma='scale')
        self.xgb_model = XGBClassifier()
        
        self.models = [('rf', self.rf_model), ('svm', self.svm_model), ('xgb', self.xgb_model)]
        
        self.ensemble_model = VotingClassifier(estimators=self.models, voting='soft')
        
        self.lstm_model = self.build_lstm_model()
        
    def build_lstm_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(None, 1)))
        model.add(LSTM(50))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def prepare_data(self):
        self.generate_labels()
        self.data.dropna(inplace=True)
    
    def generate_labels(self):
        self.data['Signal'] = 0.0  # Default to no action
        
        # Example logic for generating buy and sell signals
        condition1 = (self.data['EMA_Short'] > self.data['EMA_Long']) & (self.data['ATR_EMA'] > 10)
        condition2 = (self.data['Close'] > self.data['Fibonacci_Level_0.618']) & (self.data['Close'] < self.data['Upper_BollingerBand'])
        condition3 = self.data['Close'] < self.data['Keltner_Channel_Lower']

        # Buy condition
        self.data.loc[condition1 & condition2, 'Signal'] = 1.0  
    
        # Sell condition
        self.data.loc[condition3, 'Signal'] = -1.0  
    
        self.data.dropna(inplace=True)
    
    def train(self):
        X = self.data.drop(['Signal'], axis=1)
        y = self.data['Signal']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Class weights for imbalance
        class_weights = compute_class_weight('balanced', np.unique(y_train), y_train)
        
        # Hyperparameter tuning and model selection
        tscv = TimeSeriesSplit(n_splits=5)
        param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 10]}
        scorer = make_scorer(f1_score, greater_is_better=True)
        
        grid_rf = GridSearchCV(self.rf_model, param_grid, cv=tscv, scoring=scorer)
        grid_rf.fit(X_train, y_train)
        
        # Train ensemble
        self.ensemble_model.fit(X_train, y_train)
        
        # Train LSTM
        self.lstm_model.fit(X_train.values.reshape((X_train.shape[0], X_train.shape[1], 1)), y_train, epochs=10, batch_size=32)
    
    def predict(self, feature_vector):
        # Use ensemble model to make a prediction
        ensemble_pred = self.ensemble_model.predict_proba(feature_vector.reshape(1, -1))
        
        # Use LSTM to make a prediction
        lstm_pred = self.lstm_model.predict(feature_vector.reshape(1, feature_vector.shape[0], 1))
        
        # Weighted averaging (you can adjust the weights)
        final_pred = (0.7 * ensemble_pred + 0.3 * lstm_pred).flatten()
        
        return final_pred
    
    def evaluate(self, X_test, y_test):
        y_pred = self.ensemble_model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")
    
    def select_best_model(self, X_train, y_train, X_val, y_val):
        # Train and evaluate models/ensemble
        self.rf_model.fit(X_train, y_train)
        self.svm_model.fit(X_train, y_train)
        self.xgb_model.fit(X_train, y_train)
        self.ensemble_model.fit(X_train, y_train)

        # Evaluate models on validation data
        rf_score = self.rf_model.score(X_val, y_val)
        svm_score = self.svm_model.score(X_val, y_val)
        xgb_score = self.xgb_model.score(X_val, y_val)
        ensemble_score = self.ensemble_model.score(X_val, y_val)

        # Select the best model based on validation score
        best_model = None
        if rf_score >= svm_score and rf_score >= xgb_score and rf_score >= ensemble_score:
            best_model = self.rf_model
        elif svm_score >= rf_score and svm_score >= xgb_score and svm_score >= ensemble_score:
            best_model = self.svm_model
        elif xgb_score >= rf_score and xgb_score >= svm_score and xgb_score >= ensemble_score:
            best_model = self.xgb_model
        else:
            best_model = self.ensemble_model

        return best_model

class PivotPointCalculator:
    def __init__(self, data_path):
        self.data = self.load_data(data_path)

    def load_data(self, data_path):
        data = pd.read_csv(data_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        return data

    def calculate_pivot_points(self, window):
        pivot_points = (self.data['High'].rolling(window=window).max() +
                        self.data['Low'].rolling(window=window).min() +
                        self.data['Close'].rolling(window=window).mean()) / 3

        return pivot_points

    def get_pivot_points(self):
        pivot_points = {
            'LongTerm': self.calculate_pivot_points(252 * 10),  # 10 years
            'MediumTerm': self.calculate_pivot_points(252 * 3),  # 3 years
            'ShortTerm': self.calculate_pivot_points(252 // 2),  # 6 months
            'ThreeMonth': self.calculate_pivot_points(252 // 4),  # 3 months
            'OneMonth': self.calculate_pivot_points(252 // 12),  # 1 month
            'OneWeek': self.calculate_pivot_points(252 // 52)  # 1 week
        }
        return pivot_points


class SupportResistanceLevels:
    def __init__(self, data_path):
        self.data = self.load_data(data_path)
        self.tolerance = 0.01

    def load_data(self, data_path):
        data = pd.read_csv(data_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        return data

    def calculate_levels(self, window):
        support_levels = self.data['Low'].rolling(window=window).min().dropna().unique()
        resistance_levels = self.data['High'].rolling(window=window).max().dropna().unique()

        # Filter out levels that are too close to each other
        filtered_support_levels = []
        for support in support_levels:
            if all(abs(support - resistance) > self.tolerance for resistance in resistance_levels):
                filtered_support_levels.append(support)

        filtered_resistance_levels = []
        for resistance in resistance_levels:
            if all(abs(resistance - support) > self.tolerance for support in support_levels):
                filtered_resistance_levels.append(resistance)

        return filtered_support_levels, filtered_resistance_levels

    def get_levels(self):
        levels = {
            'LongTerm': self.calculate_levels(252 * 10),  # 10 years
            'MediumTerm': self.calculate_levels(252 * 3),  # 3 years
            'ShortTerm': self.calculate_levels(252 // 2),  # 6 months
            'ThreeMonth': self.calculate_levels(252 // 4),  # 3 months
            'OneMonth': self.calculate_levels(252 // 12),  # 1 month
            'OneWeek': self.calculate_levels(252 // 52)  # 1 week
        }
        return levels


class AdvancedModel:
    def __init__(self, data):
        self.data = data
        
        # Initialize various models
        self.rf_model = RandomForestClassifier(random_state=42)
        self.svm_model = SVC(probability=True, kernel='rbf', C=1.0, gamma='scale')
        self.xgb_model = XGBClassifier()
        
        self.models = [('rf', self.rf_model), ('svm', self.svm_model), ('xgb', self.xgb_model)]
        
        self.ensemble_model = VotingClassifier(estimators=self.models, voting='soft')
        
        self.lstm_model = self.build_lstm_model()
        
    def build_lstm_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(None, 1)))
        model.add(LSTM(50))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def prepare_data(self):
        self.generate_labels()
        self.data.dropna(inplace=True)
    
    def generate_labels(self):
        self.data['Signal'] = 0.0  # Default to no action
        
        # Example logic for generating buy and sell signals
        condition1 = (self.data['EMA_Short'] > self.data['EMA_Long']) & (self.data['ATR_EMA'] > 10)
        condition2 = (self.data['Close'] > self.data['Fibonacci_Level_0.618']) & (self.data['Close'] < self.data['Upper_BollingerBand'])
        condition3 = self.data['Close'] < self.data['Keltner_Channel_Lower']

        # Buy condition
        self.data.loc[condition1 & condition2, 'Signal'] = 1.0  
    
        # Sell condition
        self.data.loc[condition3, 'Signal'] = -1.0  
    
        self.data.dropna(inplace=True)
    
    def train(self):
        X = self.data.drop(['Signal'], axis=1)
        y = self.data['Signal']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Class weights for imbalance
        class_weights = compute_class_weight('balanced', np.unique(y_train), y_train)
        
        # Hyperparameter tuning and model selection
        tscv = TimeSeriesSplit(n_splits=5)
        param_grid = {'n_estimators': [50, 100], 'max_depth': [None, 10]}
        scorer = make_scorer(f1_score, greater_is_better=True)
        
        grid_rf = GridSearchCV(self.rf_model, param_grid, cv=tscv, scoring=scorer)
        grid_rf.fit(X_train, y_train)
        
        # Train ensemble
        self.ensemble_model.fit(X_train, y_train)
        
        # Train LSTM
        self.lstm_model.fit(X_train.values.reshape((X_train.shape[0], X_train.shape[1], 1)), y_train, epochs=10, batch_size=32)
    
    def predict(self, feature_vector):
        # Use ensemble model to make a prediction
        ensemble_pred = self.ensemble_model.predict_proba(feature_vector.reshape(1, -1))
        
        # Use LSTM to make a prediction
        lstm_pred = self.lstm_model.predict(feature_vector.reshape(1, feature_vector.shape[0], 1))
        
        # Weighted averaging (you can adjust the weights)
        final_pred = (0.7 * ensemble_pred + 0.3 * lstm_pred).flatten()
        
        return final_pred
    
    def evaluate(self, X_test, y_test):
        y_pred = self.ensemble_model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"Accuracy: {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")
    
    def select_best_model(self, X_train, y_train, X_val, y_val):
        # Train and evaluate models/ensemble
        self.rf_model.fit(X_train, y_train)
        self.svm_model.fit(X_train, y_train)
        self.xgb_model.fit(X_train, y_train)
        self.ensemble_model.fit(X_train, y_train)

        # Evaluate models on validation data
        rf_score = self.rf_model.score(X_val, y_val)
        svm_score = self.svm_model.score(X_val, y_val)
        xgb_score = self.xgb_model.score(X_val, y_val)
        ensemble_score = self.ensemble_model.score(X_val, y_val)

        # Select the best model based on validation score
        best_model = None
        if rf_score >= svm_score and rf_score >= xgb_score and rf_score >= ensemble_score:
            best_model = self.rf_model
        elif svm_score >= rf_score and svm_score >= xgb_score and svm_score >= ensemble_score:
            best_model = self.svm_model
        elif xgb_score >= rf_score and xgb_score >= svm_score and xgb_score >= ensemble_score:
            best_model = self.xgb_model
        else:
            best_model = self.ensemble_model

        return best_model

order_id_counter = 0
def generate_order_id():
    global order_id_counter
    order_id_counter += 1
    return f"O_{order_id_counter}"

class Order:
    order_count = 0

    def __init__(self, symbol, action, size, entry_price, stop=None, target=None):
        self.id = Order.order_count
        Order.order_count += 1
        self.symbol = symbol
        self.action = action
        self.size = size
        self.entry_price = entry_price
        self.status = "SUBMITTED"
        self.stop = stop
        self.target = target

# Exception classes for robust error handling
class InsufficientMarginError(Exception):
    pass

class TooVolatileError(Exception):
    pass

class VaRTooHighError(Exception):
    pass


class Position:
    def __init__(self, order, fill_price):
        self.order = order
        self.status = "OPEN"
        self.fill_price = fill_price
        self.current_price = None  # Initialize to None; you'll update this

    def update_current_price(self, current_price):
        self.current_price = current_price
    @property
    def symbol(self):
        return self.order.symbol 

    @property
    def current_value(self):
        if self.current_price is not None:
            return self.current_price * self.order.size  # Assumes the 'size' attribute is in the order
        else:
            return 0
class Portfolio:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.positions = {}

    def add_position(self, order, fill_price):
        new_position = Position(order, fill_price)
        self.positions[order.id] = new_position

    def update_cash(self, amount):
        self.cash += amount

    def reset(self, initial_cash):
        self.cash = initial_cash
        self.positions = {}

    def get_balance(self):
        total_value = self.cash
        for position in self.positions.values():
            if position.status == "OPEN":
                total_value += position.current_value  # Assumes Position class has a current_value attribute
        return total_value


class Order:
    def __init__(self, symbol, action, size, entry_price, stop, target):
        self.id = f"{symbol}:{action}:{size}"
        self.symbol = symbol
        self.action = action  # 'BUY' or 'SELL'
        self.size = size
        self.entry_price = entry_price
        self.stop = stop
        self.target = target
        self.status = "CREATED"
def check_positions(self, price_data):
    print("[INFO] Checking positions...")
    for order_id, position in self.portfolio.positions.items():
        symbol = position.symbol  # Assumes Position class has a 'symbol' attribute
        if position.status == "OPEN" and symbol in price_data:
            current_price = price_data[symbol]['open']

            # Update the current price of the position
            position.update_current_price(current_price)

            print(f"[INFO] Price update: {symbol} is currently priced at {current_price}")

            if position.order.stop and current_price <= position.order.stop:
                position.status = "CLOSED"
                self.portfolio.update_cash(current_price * position.order.size)
                print(f"[INFO] Position {position.order.id} closed due to stop-loss at {current_price}. Updated Cash Balance: {self.get_balance()}")

            elif position.order.target and current_price >= position.order.target:
                position.status = "CLOSED"
                self.portfolio.update_cash(current_price * position.order.size)
                print(f"[INFO] Position {position.order.id} closed due to target hit at {current_price}. Updated Cash Balance: {self.get_balance()}")


class PortfolioManager:
    def __init__(self, portfolio):
        self.portfolio = portfolio


    def get_balance(self):
        return self.portfolio.get_balance()

    def execute_order(self, order, fill_price):
        self.portfolio.update_cash(-fill_price * order.size)
        self.portfolio.add_position(order, fill_price)
        print(f"[INFO] Order Executed: {order.action} order for {order.size} units of {order.symbol} at price {fill_price}.")
        print(f"[INFO] Updated Cash Balance: {self.get_balance()}")

    def check_positions(self, price_data):
        print("[INFO] Checking positions...")
        for order_id, position in self.portfolio.positions.items():
            symbol = position.symbol  # Assumes Position class has a 'symbol' attribute
            if position.status == "OPEN" and symbol in price_data:
                current_price = price_data[symbol]['open']

                # Update the current price of the position
                position.update_current_price(current_price)

                print(f"[INFO] Price update: {symbol} is currently priced at {current_price}")

                if position.order.stop and current_price <= position.order.stop:
                    position.status = "CLOSED"
                    self.portfolio.update_cash(current_price * position.order.size)
                    print(f"[INFO] Position {position.order.id} closed due to stop-loss at {current_price}. Updated Cash Balance: {self.get_balance()}")

                elif position.order.target and current_price >= position.order.target:
                    position.status = "CLOSED"
                    self.portfolio.update_cash(current_price * position.order.size)
                    print(f"[INFO] Position {position.order.id} closed due to target hit at {current_price}. Updated Cash Balance: {self.get_balance()}")


import logging
class OrderManager:
    def __init__(self, portfolio_manager, risk_manager):
        self.orders = defaultdict(list)
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
    
    def get_balance(self):
        return self.portfolio_manager.get_balance()

    def place_order(self, symbol, action, size, entry_price, stop=None, target=None):
        new_order = Order(symbol, action, size, entry_price, stop, target)
        is_valid, msg = self.risk_manager.validate_order(new_order)
        
        if is_valid:
            new_order.status = "SUBMITTED"
            self.orders[symbol].append(new_order)
            print(f"Order submitted: {new_order}")
            return new_order
        else:
            print(f"Order validation failed: {msg}")
            return None

    def process_orders(self, price_data):
        logging.debug("Processing orders...")
        print(self.orders.items())
        for symbol, orders in self.orders.items():
            
            current_price = price_data['Open']
            for order in orders:
                if order.status == "SUBMITTED":
                    print(f"Trying to fill order: {order}")
                    self.fill_order(order, current_price)

        self.portfolio_manager.check_positions(price_data)

    def fill_order(self, order, current_price):
        if self.get_balance() >= current_price * order.size:
            order.status = "FILLED"
            self.portfolio_manager.execute_order(order, current_price)
            print(f"Order filled: {order.id}")
        else:
            print(f"Insufficient funds to fill order {order.id}")

# Abstract classes that define the contract for our implementations

from abc import ABC, abstractmethod
class Logger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass

class Database(ABC):
    @abstractmethod
    def save_trade(self, trade):
        pass

# Concrete implementations
class ConsoleLogger(Logger):
    def log(self, message: str):
        print(f"LOG: {message}")

class SQLiteDatabase(Database):
    def __init__(self, conn):
        self.conn = conn

    def save_trade(self, trade):
        c = self.conn.cursor()
        c.execute("INSERT INTO trade_log (log) VALUES (?)", (trade,))
        self.conn.commit()

class SignalGeneration:
    def __init__(self, max_positions):
        self.max_positions = max_positions

    def generate(self, symbol, row, pred, size, action , stop, target):
        if pred is None:
            return []

        if action:
            return [{
                'symbol': symbol,
                'action': action,
                'price': row['Close'],
                'size': size,
                'stop': stop,
                'target': target
            }]

        return []

class RiskUtility:
    
    @staticmethod
    def calculate_stop(row, stop_multiplier_low, stop_multiplier_close):
        return row['Low'] * stop_multiplier_low + row['Close'] * stop_multiplier_close

    @staticmethod
    def calculate_target(row, target_multiplier_high, target_multiplier_close):
        return row['High'] * target_multiplier_high + row['Close'] * target_multiplier_close

    @staticmethod
    def calculate_sharpe_ratio(daily_returns):
        return np.mean(daily_returns) / np.std(daily_returns)

    @staticmethod
    def calculate_drawdown(equity_curve, current_balance):
        peak = max(equity_curve)
        return (peak - current_balance) / peak

    @staticmethod
    def calculate_position_size(atr, price, balance, risk_per_trade):
        risk_amount = balance * risk_per_trade
        return int((risk_amount / atr) / price)

    @staticmethod
    def validate_order(order, portfolio, historical_volatility, max_portfolio_risk):
        try:
            if order.size * order.entry_price > portfolio.cash * 2:
                raise Exception("Insufficient margin.")
            
            if historical_volatility > 0.5:
                raise Exception("Too volatile.")
            
            alpha = 0.05
            VaR = norm.ppf(1 - alpha, loc=0, scale=historical_volatility)
            if VaR > max_portfolio_risk:
                raise Exception("VaR too high.")
            
            return True, ""
        except Exception as e:
            return False, str(e)
from scipy.stats import norm


class RiskManager:

    def __init__(self, portfolio, initial_risk_per_trade=0.09, max_drawdown=7, 
                 stop_multiplier_low=0.99, stop_multiplier_close=0.97, 
                 target_multiplier_high=3.01, target_multiplier_close=3.03, max_exposure_pct=20):
        self.portfolio = portfolio
        self.risk_per_trade = initial_risk_per_trade
        self.max_drawdown = max_drawdown
        self.equity_curve = [portfolio.get_balance()]
        self.daily_returns = []
        self.stop_multiplier_low = stop_multiplier_low
        self.stop_multiplier_close = stop_multiplier_close
        self.target_multiplier_high = target_multiplier_high
        self.target_multiplier_close = target_multiplier_close
        self.max_exposure_pct = max_exposure_pct
        self.max_portfolio_risk = 100000  # This could be dynamic based on portfolio value

    def validate_order(self, order, historical_volatility = 0.09):
        try:
            if order.size * order.entry_price > self.portfolio.get_balance() * 2:
                raise Exception("Insufficient margin.")
            
            if historical_volatility > 0.5:
                raise Exception("Too volatile.")
            
            alpha = 0.05
            VaR = norm.ppf(1 - alpha, loc=0, scale=historical_volatility)
            if VaR > self.max_portfolio_risk:
                raise Exception("VaR too high.")
            
            return True, ""
        except Exception as e:
            return False, str(e)

    def calculate_stop(self, row):
        return RiskUtility.calculate_stop(row, self.stop_multiplier_low, self.stop_multiplier_close)

    def calculate_target(self, row):
        return RiskUtility.calculate_target(row, self.target_multiplier_high, self.target_multiplier_close)

    def calculate_position_size(self, atr, price):
        return RiskUtility.calculate_position_size(atr, price, self.portfolio.get_balance(), self.risk_per_trade)

    def update_equity_curve(self):
        current_balance = self.portfolio.get_balance()
        self.equity_curve.append(current_balance)
        
        if len(self.equity_curve) > 1:
            daily_return = (self.equity_curve[-1] - self.equity_curve[-2]) / self.equity_curve[-2]
            self.daily_returns.append(daily_return)

    def calculate_sharpe_ratio(self):
        return RiskUtility.calculate_sharpe_ratio(self.daily_returns)

    def calculate_drawdown(self):
        return RiskUtility.calculate_drawdown(self.equity_curve, self.portfolio.get_balance())

    def check_drawdown(self):
        return self.calculate_drawdown() < self.max_drawdown

    def adjust_risk(self, new_risk_per_trade):
        self.risk_per_trade = new_risk_per_trade


class RiskReportManager:
    """Generate a risk report based on RiskManager data."""
    
    def __init__(self, risk_manager):
        self.risk_manager = risk_manager

    def log_and_print(self, message):
        """Logs and prints the given message."""
        print(message)
        logging.info(message)

    def generate_report(self):
        """Generate a risk report."""
        self.log_and_print("=== Risk Report ===")

        # Daily returns
        daily_returns = self.risk_manager.daily_returns
        if daily_returns:
            daily_return_msg = f"Daily Returns: {np.mean(daily_returns):.4f} +/- {np.std(daily_returns):.4f}"
        else:
            daily_return_msg = "Daily Returns: N/A"
        self.log_and_print(daily_return_msg)

        # Sharpe ratio
        sharpe_ratio = self.risk_manager.calculate_sharpe_ratio()
        sharpe_ratio_msg = f"Sharpe Ratio: {sharpe_ratio if sharpe_ratio is not None else 'N/A'}"
        self.log_and_print(sharpe_ratio_msg)

        # Drawdown
        drawdown = self.risk_manager.calculate_drawdown()
        drawdown_msg = f"Current Drawdown: {drawdown:.4f}"
        self.log_and_print(drawdown_msg)

        # Max drawdown
        max_drawdown_msg = f"Maximum Allowed Drawdown: {self.risk_manager.max_drawdown:.4f}"
        self.log_and_print(max_drawdown_msg)

        # Risk per trade
        risk_per_trade_msg = f"Current Risk per Trade: {self.risk_manager.risk_per_trade:.4f}"
        self.log_and_print(risk_per_trade_msg)

        # Portfolio balance
        balance_msg = f"Current Portfolio Balance: {self.risk_manager.portfolio.cash}"
        self.log_and_print(balance_msg)

        # Equity curve
        equity_curve_msg = f"Equity Curve: {self.risk_manager.equity_curve}"
         #self.log_and_print(equity_curve_msg)

        self.log_and_print("===================")



class BaseTradingStrategy:
    def generate_signals(self, symbol, row, prediction):
        raise NotImplementedError

    def execute_trades(self, signals):
        raise NotImplementedError

    def run_strategy(self, symbol, row, prediction):
        raise NotImplementedError

# DefaultTradingStrategy class;
class DefaultTradingStrategy(BaseTradingStrategy):
    def __init__(self, model, order_manager, max_positions=50, trading_fee=0.001, slippage=0.001):
        print("Initializing DefaultTradingStrategy")
        self.model = model
        self.order_manager = order_manager
        self.order_log = {}
        self.max_positions = max_positions
        self.trading_fee = trading_fee
        self.slippage = slippage
        self.signal_generator = SignalGeneration(self.max_positions)
        print(f"Strategy parameters: max_positions={max_positions}, trading_fee={trading_fee}, slippage={slippage}")

    def execute_strategy(self, signals):
        print("Executing strategy...")
        for signal in signals:
            print(f"Processing signal: {signal}")
            symbol = signal['symbol']
            action = signal['action']
            price = signal['price']
            size = signal['size']
            stop = signal.get('stop', None)
            target = signal.get('target', None)
            
            print("Placing order...")
            success = self.order_manager.place_order(symbol, action, size, price, stop, target)
            
            if success:
                print("Order initiated for signal")
                print(signal)

    def run_strategy(self, symbol, price_data, prediction):
        print("Running oending orders...")
        print(f"Price data: {price_data}")
        print(f"Prediction: {prediction}")

        self.order_manager.process_orders(price_data)
        
        print("Calculating position size...")
        position_size = self.order_manager.risk_manager.calculate_position_size(price_data['ATR'], price_data['Close']) / 5
        print(f"Position size: {position_size}")

        if position_size <= 0:
            print("Position size <= 0, exiting.")
            return []

        print("Calculating stop and target...")
        stop = self.order_manager.risk_manager.calculate_stop(price_data)
        target = self.order_manager.risk_manager.calculate_target(price_data)
        
        print(f"Stop: {stop}, Target: {target}")

        action = 'BUY' if prediction == 1 else 'SELL' if prediction == -1 else None
        print(f"Action: {action}")

        print("Generating signals...")
        signals = self.signal_generator.generate(symbol, price_data, prediction, position_size, action, stop, target)
        
        print("Executing strategy with generated signals...")
        self.execute_strategy(signals)


class Backtest:
    def __init__(self, strategy, feature_columns, symbol, data, model, portfolio, optimization_interval=20000, monte_carlo_runs=1000):
        self.strategy = strategy
        self.feature_columns = feature_columns
        self.symbol = symbol
        self.data = data
        self.model = model
        self.portfolio = portfolio
        self.optimization_interval = optimization_interval
        self.monte_carlo_runs = monte_carlo_runs
        self.monte_carlo_results = []

    def run(self):
        self.portfolio.reset(1000000)
        rolling_window_data = []  # Initialize an empty list for rolling_window_data

        for index, row in self.data.iterrows():
            try:
                rolling_window_data.append(row)
                if len(rolling_window_data) > 30:
                    rolling_window_data.pop(0)

                if len(rolling_window_data) < 30:
                    continue
                
                rolling_window = pd.DataFrame(rolling_window_data)
                feature_vector = rolling_window.iloc[-1][self.feature_columns].values.reshape(1, -1)
                prediction = self.model.predict(feature_vector)[0]
                
            except Exception as e:
                print(f"An error occurred: {e}")
                prediction = None
                
            self.strategy.run_strategy(self.symbol, row, prediction)

        self.collect_metrics()
        #self.run_monte_carlo_simulation()

    def make_prediction(self, feature_vector):
        prediction = self.model.predict(feature_vector)[0]
        probabilities = self.model.predict_proba(feature_vector)
        position_multiplier = probabilities[0][1]
        base_position_size = self.risk_manager.calculate_base_position_size()
        position_size = base_position_size * position_multiplier
        base_stop_loss, base_take_profit = self.risk_manager.calculate_base_stop_and_profit()
        dynamic_stop_loss = base_stop_loss * (1 + probabilities[0][1] - 0.5)
        dynamic_take_profit = base_take_profit * (1 + probabilities[0][1] - 0.5)
        if prediction == 1:
            print(prediction)
        elif prediction == -1:
                print(prediction)

    def run_monte_carlo_simulation(self):
        print("Running Monte Carlo Simulation...")
        
        for _ in range(self.monte_carlo_runs):
            simulated_data = choices(self.data.values.tolist(), k=len(self.data))
            simulated_data_df = pd.DataFrame(simulated_data, columns=self.data.columns)
            self.run_single_simulation(simulated_data_df)

        avg_profit = sum(self.monte_carlo_results) / len(self.monte_carlo_results)
        print(f"Average profit from {self.monte_carlo_runs} Monte Carlo runs: {avg_profit}")

    def run_single_simulation(self, simulated_data):
        self.strategy.risk_manager.portfolio.reset(self.initial_balance)
        rolling_window_data = []

        for index, row in simulated_data.iterrows():
            try:
                rolling_window_data.append(row)
                if len(rolling_window_data) > 30:
                    rolling_window_data.pop(0)

                if len(rolling_window_data) < 30:
                    continue
                
                rolling_window = pd.DataFrame(rolling_window_data)
                feature_vector = rolling_window.iloc[-1][self.strategy.feature_columns].values.reshape(1, -1)
                prediction = self.model.predict(feature_vector)[0]
                
            except Exception as e:
                print(f"An error occurred during simulation: {e}")
                prediction = None

            self.strategy.run_strategy(self.symbol, row, prediction)
        
        final_balance = self.strategy.order_manager.risk_manager.portfolio.balance
        self.monte_carlo_results.append(final_balance - self.initial_balance)

    def collect_metrics(self):
        riskReport = RiskReportManager(self.strategy.order_manager.risk_manager)
        portfolioReport = PortfolioReportManager(self.strategy.order_manager.risk_manager.portfolio)       
        portfolioReport.log_equity()
        riskReport.generate_report()

if __name__ == "__main__":
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    start_date = '2011-01-01'
    end_date = '2023-01-01'

    import sqlite3

    conn = sqlite3.connect('trading_system.db')
    logger = ConsoleLogger()
    database = SQLiteDatabase(conn)

    for symbol in symbols:
        # Download historical data
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")
            continue
        # Create a builder instance and chain the configuration methods
        rf_model = (
            RandomForestTradingModelBuilder()
            .set_symbol(symbol)
            .set_data(data)
            .set_label_generator(DefaultLabelGenerator())  # Use custom label generator
            .set_feature_selector(DefaultFeatureSelector())  # Use custom feature selector
            .set_model_trainer(GridSearchModelTrainer())  # Use custom model trainer
            .set_data_preparator(DefaultDataPreparator())  # Use custom data preparator
            .set_data_splitter(DefaultDataSplitter())  # Use custom data splitter
            .set_model_params(n_estimators=100, max_depth=None)
            .build())
        
        rf_model.train()
        rf_model.save('AAPL_trading_model.pkl')
        rf_model.load('AAPL_trading_model.pkl')
        feature_columns = rf_model.feature_columns 
        portfolio = Portfolio(1000000)

        my_risk_manager = RiskManager(portfolio=portfolio, 
                               initial_risk_per_trade=0.09, 
                               max_drawdown=7,
                               stop_multiplier_low=0.99,
                               stop_multiplier_close=0.97,
                               target_multiplier_high=3.01,
                               target_multiplier_close=3.03,
                               max_exposure_pct=20)

        portfolio_manager = PortfolioManager(portfolio)

        order_manager = OrderManager(portfolio_manager, my_risk_manager)
        strategy = DefaultTradingStrategy(model=rf_model, order_manager=order_manager)
        backtest = Backtest(strategy, feature_columns, symbol, data, rf_model, portfolio)
        backtest.run()

        # Show results
        print(f'Final Portfolio Balance: ${portfolio.cash}')