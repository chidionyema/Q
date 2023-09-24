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