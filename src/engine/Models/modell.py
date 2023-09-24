

class LSTMModel:
    def __init__(self, look_back):
        self.look_back = look_back
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(look_back, 4)),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')
