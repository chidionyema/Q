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