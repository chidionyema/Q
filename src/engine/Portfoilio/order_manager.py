class OrderManager:
    def __init__(self, portfolio_manager, risk_manager):
        self.orders = defaultdict(list)
        self.portfolio_manager = portfolio_manager
        self.risk_manager = risk_manager
    
    def get_balance(self):
        return self.portfolio_manager.get_balance()

    def place_order(self, symbol, action, size, entry_price, stop=None, target=None):
        new_order = Order(symbol, action, size, entry_price, stop, target)
        is_valid, msg = self.risk_manager.validate_order(new_order)
        
        if is_valid:
            new_order.status = "SUBMITTED"
            self.orders[symbol].append(new_order)
            print(f"Order submitted: {new_order}")
            return new_order
        else:
            print(f"Order validation failed: {msg}")
            return None

    def process_orders(self, price_data):
        logging.debug("Processing orders...")
        print(self.orders.items())
        for symbol, orders in self.orders.items():
            
            current_price = price_data['Open']
            for order in orders:
                if order.status == "SUBMITTED":
                    print(f"Trying to fill order: {order}")
                    self.fill_order(order, current_price)

        self.portfolio_manager.check_positions(price_data)

    def fill_order(self, order, current_price):
        if self.get_balance() >= current_price * order.size:
            order.status = "FILLED"
            self.portfolio_manager.execute_order(order, current_price)
            print(f"Order filled: {order.id}")
        else:
            print(f"Insufficient funds to fill order {order.id}")