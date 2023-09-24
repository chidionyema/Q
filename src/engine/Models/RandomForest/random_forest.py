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