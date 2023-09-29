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