import React, { useState } from 'react';
import { Box, Typography, Paper, Tooltip } from '@mui/material';

const mockStocks = [
  { symbol: "AAPL", price: 150.10, change: "+1.35%" },
  { symbol: "GOOGL", price: 2829.15, change: "-0.12%" },
  { symbol: "AMZN", price: 3350.72, change: "+2.05%" },
  { symbol: "MSFT", price: 300.25, change: "-0.80%" }
];

const StockPrices: React.FC = () => {
  const [selectedStock, setSelectedStock] = useState(null);

  const handleStockHover = (stock) => {
    setSelectedStock(stock);
  };

  return (
    <Paper elevation={3} sx={{ p: 2, mt: 3 }}>
      <Typography variant="h6" gutterBottom>Latest Stock Prices</Typography>
      <Box sx={{ gap: 2, display: 'flex', flexDirection: 'column' }}>
        {mockStocks.map(stock => (
          <Tooltip title={`Price Change: ${stock.change}`} arrow key={stock.symbol} >
            <Typography 
              onMouseEnter={() => handleStockHover(stock)}
              onMouseLeave={() => setSelectedStock(null)}
            >
              {stock.symbol}: ${stock.price}
            </Typography>
          </Tooltip>
        ))}
        {selectedStock && 
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2">Details for {selectedStock.symbol}:</Typography>
            <Typography variant="body2">Current Price: ${selectedStock.price}</Typography>
            <Typography variant="body2">Price Change: {selectedStock.change}</Typography>
          </Box>
        }
      </Box>
    </Paper>
  );
};

export default StockPrices;
