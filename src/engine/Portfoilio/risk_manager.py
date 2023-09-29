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


