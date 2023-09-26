
class TrainingCoordinator:
    def __init__(self, models, processed_data, ensemble_class):
        self.models = models
        self.processed_data = processed_data
        self.ensemble_class = ensemble_class

    def suggest_strategy(self, selected_stocks):
        """
        Suggest an appropriate training strategy based on the number of selected stocks and models.

        Args:
            selected_stocks (list): List of selected stocks.

        Returns:
            str: Suggested strategy.
        """
        num_stocks = len(selected_stocks)
        num_models = len(self.models)

        # Suggest a strategy based on the number of stocks and models
        if num_stocks == 1 and num_models == 1:
            return "Single Model - Single Stock"
        elif num_stocks == 1 and num_models > 1:
            return "Multiple Models - Single Stock"
        elif num_stocks > 1 and num_models == 1:
            return "Single Model - Multiple Stocks"
        elif num_stocks > 1 and num_models > 1:
            return "Multiple Models - Multiple Stocks"

    def train_models(self, selected_stocks, selected_strategy):
        """
        Train models based on the selected strategy.

        Args:
            selected_stocks (list): List of selected stocks.
            selected_strategy (str): Selected training strategy.
        """
        if selected_strategy not in ["Single Model - Single Stock", "Multiple Models - Single Stock",
                                     "Single Model - Multiple Stocks", "Multiple Models - Multiple Stocks"]:
            raise ValueError("Invalid strategy selected.")

        # Use the selected strategy to train models
        if selected_strategy == "Single Model - Single Stock":
            model = self.models[0]
            ensemble = self.ensemble_class([model])
            data_splits = self.get_data_for_stock(selected_stocks[0])
            train_data, _, _ = data_splits
            X_train, y_train = train_data
            ensemble.train(X_train, y_train)
        elif selected_strategy == "Multiple Models - Single Stock":
            ensemble = self.ensemble_class(self.models)
            data_splits = self.get_data_for_stock(selected_stocks[0])
            train_data, _, _ = data_splits
            X_train, y_train = train_data
            ensemble.train(X_train, y_train)
        elif selected_strategy == "Single Model - Multiple Stocks":
            model = self.models[0]
            ensemble = self.ensemble_class([model])
            combined_data = self.combine_data_for_stocks(selected_stocks)
            train_data, _, _ = combined_data
            X_train, y_train = train_data
            ensemble.train(X_train, y_train)
        elif selected_strategy == "Multiple Models - Multiple Stocks":
            ensemble = self.ensemble_class(self.models)
            combined_data = self.combine_data_for_stocks(selected_stocks)
            train_data, _, _ = combined_data
            X_train, y_train = train_data
            ensemble.train(X_train, y_train)

    def get_data_for_stock(self, stock):
        """
        Get processed data splits for a specific stock.

        Args:
            stock (str): The stock symbol.

        Returns:
            tuple: Data splits (X_train, y_train, X_val, y_val, X_test, y_test) for the stock.
        """
        if stock in self.processed_data:
            return self.processed_data[stock]
        else:
            raise ValueError(f"Stock '{stock}' not found in processed data.")

    def combine_data_for_stocks(self, selected_stocks):
        """
        Combine data for selected stocks.

        Args:
            selected_stocks (list): List of selected stocks.

        Returns:
            tuple: Combined data (X_train, y_train, X_val, y_val, X_test, y_test).
        """
        combined_train, combined_val, combined_test = [], [], []
        for stock in selected_stocks:
            data_splits = self.get_data_for_stock(stock)
            train, val, test = data_splits
            combined_train.extend(train[0])
            combined_val.extend(val[0])
            combined_test.extend(test[0])
        return combined_train, combined_val, combined_test

