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