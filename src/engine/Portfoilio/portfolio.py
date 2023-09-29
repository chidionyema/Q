class Portfolio:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.positions = {}

    def add_position(self, order, fill_price):
        new_position = Position(order, fill_price)
        self.positions[order.id] = new_position

    def update_cash(self, amount):
        self.cash += amount

    def reset(self, initial_cash):
        self.cash = initial_cash
        self.positions = {}

    def get_balance(self):
        total_value = self.cash
        for position in self.positions.values():
            if position.status == "OPEN":
                total_value += position.current_value  # Assumes Position class has a current_value attribute
        return total_value