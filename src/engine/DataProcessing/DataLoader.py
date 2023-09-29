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