

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
