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
        with concurrent.futures.ProcessPoolExecutor() as executor:
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