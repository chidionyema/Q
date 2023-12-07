
import React, { useState, useEffect } from 'react';
import {
  Grid, Typography, Tabs, Tab, FormControl, InputLabel, Select, MenuItem, Button,
  TextField, Autocomplete, Box, Switch, FormControlLabel, Paper, TableContainer, Table, TableHead, TableBody, TableRow, TableCell
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { styled } from '@mui/system';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import SocketManager from '../utility/SocketManager';
import { useApiCall } from '../hooks/useApiCall';
import { APIProxy } from '../utility/apiProxy';
// Define interfaces for props
interface StyledDateInputProps {
  value: string;
  onClick: () => void;
}

// Create a styled DatePicker component
const StyledDatePicker = styled(DatePicker)(({ theme }) => ({
  width: '100%',
  padding: '14px 16px',
  fontSize: '1rem',
  border: '1px solid rgba(0, 0, 0, 0.23)',
  borderRadius: '4px',
  '&:focus': {
    borderColor: theme.palette.primary.main,
    boxShadow: `0 0 0 2px ${theme.palette.primary.light}`,
    outline: 'none',
  },
  position: 'absolute',
  top: 0,
  right: 0,
  zIndex: 9999,
}));


// Styled component for styling purposes
const StyledDateInputWrapper = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: theme.spacing(1),
  border: `1px solid ${theme.palette.divider}`,
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  '& span': {
    flexGrow: 1,
  },
  '& button': {
    padding: theme.spacing(1),
    border: 'none',
    borderRadius: theme.shape.borderRadius,
    cursor: 'pointer',
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    transition: 'background-color 0.3s',
    '&:hover': {
      backgroundColor: theme.palette.primary.dark,
    },
  },
}));

// Functional component to handle logic
const StyledDateInput = ({ value, onClick }: StyledDateInputProps) => (
  <StyledDateInputWrapper>
    <span>{value}</span>
    <button onClick={onClick}>Pick a date</button>
  </StyledDateInputWrapper>
);

const App = () => {
  const stocksList = ['AAPL', 'GOOGL', 'AMZN', 'TSLA'];
 
  interface SelectOption {
    id: string;
    name: string;
  }
  
  const [models, setModels] = useState<SelectOption[]>([]);
  const [optimizers, setOptimizers] = useState<SelectOption[]>([]);
  const [votingStrategies, setVotingStrategies] = useState<SelectOption[]>([]);
  const [advancedMode, setAdvancedMode] = useState<boolean>(false);
  const [selectedStocks, setSelectedStocks] = useState<string[]>([]);
  const [currentStockTab, setCurrentStockTab] = useState<number>(0);
  const [stockConfig, setStockConfig] = useState<{[key: string]: any}>({});
  const [serverFeedback, setServerFeedback] = useState('');
  const [configErrors, setConfigErrors] = useState({});
  const [predictionResults, setPredictionResults] = useState<StockPredictionResults>({});
  const today = new Date();
  // Create a single instance of APIProxy
  const apiProxyInstance = new APIProxy();
  const apiCall = useApiCall(apiProxyInstance.fetchEndpoint);

  interface ConfigErrors {
    [key: string]: string;
  }
  
// Validation function
const validateConfig = () => {
  let errors: ConfigErrors = {};
  selectedStocks.forEach(stock => {
    const config = stockConfig[stock];
    if (!config.startDate) {
      errors[`${stock}-startDate`] = 'Start date is required';
    }
    if (!config.endDate) {
      errors[`${stock}-endDate`] = 'End date is required';
    }
    if (!config.Model) {
      errors[`${stock}-Model`] = 'Model selection is required';
    }
    if (!config.Optimizer) {
      errors[`${stock}-Optimizer`] = 'Optimizer selection is required';
    }
    if (!config['Voting Strategy']) {
      errors[`${stock}-VotingStrategy`] = 'Voting strategy selection is required';
    }
  });
  setConfigErrors(errors);
  return Object.keys(errors).length === 0;
};

  

const fetchModels = async () => {
  try {
    const response = await apiCall.call('/fetch-models');
    if (response) {
      console.log('yes response')
      setModels(response);
    } else {
      // Handle the case where data is not present in the response
      setModels([]);
    }
  } catch (error) {
    console.error('Error fetching models:', error);
    setModels([]);
  }
};

  
  
  const fetchOptimizers = async () => {
    try {
      const response = await apiCall.call('/fetch_optimizers');

      if (response && response) {
        console.log('yes response')
        setOptimizers( response);
      } else {
        console.log(response);
        console.log(response);
        console.log('no response')
        // Handle the case where data is not present in the response
        setOptimizers([]);
      }
    } catch (error) {
      console.error('Error fetching optimizers:', error);
    }
  };
  
  const fetchVotingStrategies = async () => {
    try {
      const response = await apiCall.call('/fetch_ensembles');
      if (response) {
        console.log('yes response')
        setVotingStrategies(response);
      } else {
        // Handle the case where data is not present in the response
        setVotingStrategies([]);
      }
    } catch (error) {
      console.error('Error fetching voting strategies:', error);
    }
  };
  

  const updateConfig = (key: string, value: any) => {
    setStockConfig(prev => ({
      ...prev,
      [selectedStocks[currentStockTab]]: {
        ...prev[selectedStocks[currentStockTab]],
        [key]: key === 'Model' ? [...value] : value  // Handle multiple models
      }
    }));
  };

  const isStockConfigComplete = (stock: string) => {
    const config = stockConfig[stock];
    return config && Array.isArray(config.Model) && config.Model.length > 0 && config.Optimizer && config['Voting Strategy'];
  };
  

  const handleStartDateChange = (date: Date | null) => {
    if (date) {
      updateConfig('startDate', date);
      if (date > new Date(stockConfig[selectedStocks[currentStockTab]]?.endDate || new Date())) {
        updateConfig('endDate', date);
      }
    }
  };

  const handleEndDateChange = (date: Date | null) => {
    if (date && date <= new Date() && date >= new Date(stockConfig[selectedStocks[currentStockTab]]?.startDate || new Date())) {
      updateConfig('endDate', date);
    }
  };

  useEffect(() => {
    fetchModels();
    fetchOptimizers();
    fetchVotingStrategies();
  }, []);
  
  const socketManager = SocketManager.getInstance();
 
  interface StockPredictionResult {
    symbol: string;
    mae_val: number;
    mae_test: number;
    // Add new metrics here
    mse_val?: number; // Mean Squared Error for Validation
    mse_test?: number; // Mean Squared Error for Test
    r2_val?: number;   // R-squared for Validation
    r2_test?: number;  // R-squared for Test
    mape_val?: number; // Mean Absolute Percentage Error for Validation
    mape_test?: number; // Mean Absolute Percentage Error for Test
}

type StockPredictionResults = {
    [key: string]: StockPredictionResult;
};


  useEffect(() => {  
      socketManager.connect();
      socketManager.on('connect', () => console.log('Connected to server'));
      
      socketManager.on('training_complete', (data) => {
        const updatedResults: { [key: string]: StockPredictionResult } = { ...predictionResults };
        console.log(data);
        if (data.predictions && Array.isArray(data.predictions)) {
            data.predictions.forEach((result: StockPredictionResult) => {
                updatedResults[result.symbol] = result;
            });
            setPredictionResults(updatedResults);
        } else {
            console.error("Unexpected data format:", data);
        }
    });
    
    
    
      socketManager.on('training_error', (error) => {
          console.error('Training error:', error);
         // setIsTraining(false);
         // setIsLoading(false);
         // setServerFeedback(error.message || 'Error during training.');
      });
      socketManager.on('progress', (data) => {
          console.log('Training progress:', data);
          //setProgress(data.percentage);
      });

      return () => {
          socketManager.disconnect();
      };
  }, []);

  const startTraining = () => {
    if (!validateConfig()) return;
    //  setIsTraining(true);
     // setIsLoading(true);
     console.log("in");
     const trainingData = selectedStocks.map(stock => ({
      symbol: stock,
      config: stockConfig[stock],
      models: stockConfig[stock].Model 
    }));
    socketManager.emit('submit_configurations', trainingData);
  };
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>Stock Analysis Configuration</Typography>
        <Paper style={{ padding: '16px', backgroundColor: '#f9f9f9' }}>
          <Box display="flex" alignItems="center" mt={2} mb={2}>
            <FormControlLabel
              control={<Switch checked={advancedMode} onChange={e => setAdvancedMode(e.target.checked)} color="primary" />}
              label="Advanced Mode"
            />
          </Box>
          <Autocomplete
            multiple
            options={stocksList}
            value={selectedStocks}
            onChange={(event, newValue) => setSelectedStocks(newValue)}
            renderInput={(params) => (
              <TextField {...params} variant="outlined" label="Select Stocks" placeholder="Search" fullWidth />
            )}
          />
        </Paper>
      </Grid>

      {selectedStocks.length > 0 && (
        <Grid item xs={12}>
          <Paper style={{ padding: '16px', backgroundColor: '#f9f9f9' }}>
            <Tabs value={currentStockTab} onChange={(event, newValue) => setCurrentStockTab(newValue)}>
              {selectedStocks.map(stock => (
                <Tab 
                  key={stock} 
                  label={stock} 
                  icon={isStockConfigComplete(stock) ? <CheckCircleOutlineIcon /> : undefined} 
                />
              ))}
            </Tabs>
            <Box mt={2}>
            <FormControl fullWidth>
              <InputLabel>Start Date</InputLabel>
              <StyledDatePicker
                selected={new Date(stockConfig[selectedStocks[currentStockTab]]?.startDate || new Date())}
                onChange={handleStartDateChange}
                dateFormat="dd/MM/yyyy"
                maxDate={today} // Set the max date to today
                showYearDropdown
                showMonthDropdown
                customInput={<StyledDateInput value={(stockConfig[selectedStocks[currentStockTab]]?.startDate || new Date()).toDateString()} onClick={() => {}} />}
                popperPlacement="top-end"
              />
            </FormControl>
          </Box>
          <Box mt={2}>
            <FormControl fullWidth>
              <InputLabel>End Date</InputLabel>
              <StyledDatePicker
                selected={new Date(stockConfig[selectedStocks[currentStockTab]]?.endDate || new Date())}
                onChange={handleEndDateChange}
                dateFormat="dd/MM/yyyy"
                maxDate={today} // Set the max date to today
                showYearDropdown
                showMonthDropdown
                customInput={<StyledDateInput value={(stockConfig[selectedStocks[currentStockTab]]?.endDate || new Date()).toDateString()} onClick={() => {}} />}
                popperPlacement="top-end"
              />
            </FormControl>
            </Box>
          

          {!advancedMode && (
          <FormControl fullWidth variant="outlined">
          <InputLabel htmlFor="model-select">Model</InputLabel>
          <Select
            id="model-select"
            value={stockConfig[selectedStocks[currentStockTab]]?.Model || ''}
            onChange={(e) => updateConfig('Model', e.target.value)}
          >
            {models.map(model => (
              <MenuItem key={model.id} value={model.name}>{model.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
      )}

          {advancedMode && (
        <FormControl fullWidth variant="outlined">
          <InputLabel htmlFor="model-select">Model</InputLabel>
          <Select
            id="model-select"
            multiple
            value={stockConfig[selectedStocks[currentStockTab]]?.Model || []}
            onChange={(e) => updateConfig('Model', e.target.value)}
            renderValue={(selected) => selected.join(', ')}
          >
            {models.map(model => (
              <MenuItem key={model.id} value={model.name}>{model.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
      )}

          <FormControl fullWidth variant="outlined">
            <InputLabel htmlFor="optimizer-select">Optimizer</InputLabel>
            <Select
              id="optimizer-select"
              value={stockConfig[selectedStocks[currentStockTab]]?.Optimizer || ''}
              onChange={(e) => updateConfig('Optimizer', e.target.value)}
            >
              {optimizers.map(optimizer => (
                <MenuItem key={optimizer.id} value={optimizer.name}>{optimizer.name}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth variant="outlined">
            <InputLabel htmlFor="voting-strategy-select">Voting Strategy</InputLabel>
            <Select
              id="voting-strategy-select"
              value={stockConfig[selectedStocks[currentStockTab]]?.['Voting Strategy'] || ''}
              onChange={(e) => updateConfig('Voting Strategy', e.target.value)}
            >
              {votingStrategies.map(strategy => (
                <MenuItem key={strategy.id} value={strategy.name}>{strategy.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
            {/* Advanced Mode Configuration Here */}
            <Box mt={3}>
              <Button variant="contained" color="primary" disabled={Object.keys(configErrors).length > 0} onClick={startTraining}>Submit Configurations</Button>
            </Box>
          </Paper>
          {
   
    selectedStocks.length > 0 && (
        <Grid item xs={12}>
            {selectedStocks.map(stock => (
                <Paper key={stock} elevation={3} style={{ marginTop: '1rem', padding: '1rem' }}>
                    <Typography variant="h5" gutterBottom align="center">Prediction Results for {stock}</Typography>
                    <Box mt={2}>
                    {predictionResults[stock] ? (
    <>
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>MAE Val</TableCell>
                        <TableCell>MAE Test</TableCell>
                        <TableCell>MSE Val</TableCell>
                        <TableCell>MSE Test</TableCell>
                        <TableCell>R2 Val</TableCell>
                        <TableCell>R2 Test</TableCell>
                        <TableCell>MAPE Val</TableCell>
                        <TableCell>MAPE Test</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow>
                        <TableCell>{predictionResults[stock].mae_val}</TableCell>
                        <TableCell>{predictionResults[stock].mae_test}</TableCell>
                        <TableCell>{predictionResults[stock].mse_val}</TableCell>
                        <TableCell>{predictionResults[stock].mse_test}</TableCell>
                        <TableCell>{predictionResults[stock].r2_val}</TableCell>
                        <TableCell>{predictionResults[stock].r2_test}</TableCell>
                        <TableCell>{predictionResults[stock].mape_val}</TableCell>
                        <TableCell>{predictionResults[stock].mape_test}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
        <Typography variant="caption" display="block" gutterBottom style={{ marginTop: '10px' }}>
            <strong>Explanation of Metrics:</strong>
            <br /><strong>MAE (Mean Absolute Error):</strong> Average of absolute differences between predicted and actual values.
            <br /><strong>MSE (Mean Squared Error):</strong> Average of squared differences between predicted and actual values.
            <br /><strong>R2 (R-squared):</strong> Proportion of variance in the dependent variable predictable from the independent variables.
            <br /><strong>MAPE (Mean Absolute Percentage Error):</strong> Average of absolute percentage differences between predicted and actual values.
        </Typography>
    </>
) : (
    <Typography variant="body1">No results available yet for {stock}</Typography>
)}

        </Box>
                </Paper>
            ))}
        </Grid>
    )
  }



        </Grid>
        
      )}
    </Grid>
  );
};

export default App;
