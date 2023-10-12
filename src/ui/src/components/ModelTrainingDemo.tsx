import React, { useState, useEffect } from 'react';
import SocketManager from '../utility/SocketManager';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import io from 'socket.io-client';
import { fetchUserAuthenticationStatus } from '../utility/authHelper';
import {
    Button, FormControl, Select, InputLabel,
    CircularProgress, Snackbar, LinearProgress, Typography, MenuItem, Box, Grid, Container, Paper, CssBaseline,
    TableContainer, Table, TableHead, TableBody, TableRow, TableCell, Link
} from '@mui/material';
import Alert from '@mui/material/Alert';
import { styled } from '@mui/system';

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
    }
}));

const TrainingDemo = () => {
    const [progress, setProgress] = useState(0);
    const [isTraining, setIsTraining] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedLearningType, setSelectedLearningType] = useState('Supervised');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [symbol, setSymbol] = useState('');
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [validationError, setValidationError] = useState('');
    const [serverFeedback, setServerFeedback] = useState('');
    const [maeVal, setMaeVal] = useState(null);
    const [maeTest, setMaeTest] = useState(null);
    const [predictionResults, setPredictionResults] = useState([]);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    const clearResults = () => {
       // setTrainingStarted(false);
        setMaeVal(null);
        setMaeTest(null);
        setPredictionResults([]);
    };
    
 
    

    const validateInputs = () => {
        if (!symbol) {
            return "Symbol is required!";
        }

        if (!selectedModel) {
            return "Model is required!";
        }

        // Calculate maximum allowable end date based on selected start date
        const maxEndDate = new Date(startDate);
        maxEndDate.setDate(maxEndDate.getDate() + 365); // Allow up to 1 year in the future

        if (endDate < startDate || endDate > maxEndDate) {
            return "End Date should be after Start Date and within 1 year!";
        }
        return null;
    };

    const learningTypes = {
        'Supervised': {
            'Linear Models': ['Linear Regression', 'Logistic Regression'],
            'Decision Trees': ['Random Forest', 'Decision Tree', 'Extra Trees']
        },
        'Unsupervised': {
            'Dimensionality Reduction': ['Principal Component Analysis (PCA)']
        }
    };

    let socket = io('https://api.dev.io:5000');
    const socketManager = SocketManager.getInstance();

    useEffect(() => {
        // Clearing results whenever dependencies change
        clearResults();
    
        const checkAuthenticationStatus = async () => {
            const userIsAuthenticated = await fetchUserAuthenticationStatus();
            setIsAuthenticated(userIsAuthenticated);
        };
        checkAuthenticationStatus();
        socketManager.connect();
    
        socketManager.on('connect', () => console.log('Connected to server'));
        socketManager.on('training_complete', (data) => {
            console.log('Training complete:', data);
            setIsTraining(false);
            setIsLoading(false);
            setMaeVal(data.mae_val);
            setMaeTest(data.mae_test);
            setPredictionResults(data.predictions);
        });
        socketManager.on('training_error', (error) => {
            console.error('Training error:', error);
            setIsTraining(false);
            setIsLoading(false);
            setServerFeedback(error.message || 'Error during training.');
        });
        socketManager.on('progress', (data) => {
            console.log('Training progress:', data);
            setProgress(data.percentage);
        });
    
        return () => {
            socketManager.disconnect();
        };
    }, [symbol, startDate, endDate, selectedCategory, selectedModel]); // Dependencies are added here
    
    const startTraining = () => {
        setIsTraining(true);
        setIsLoading(true);
        socketManager.emit('train_model', {
            symbol: symbol,
            start_date: startDate,
            end_date: endDate,
            model: selectedModel
        });
    };
    
    const highlightStyle = {
        fontWeight: 'bold',
        color: 'blue',  // Change color or any style as needed
        fontSize: '1.1rem',
    };
    
    const scrollToPredictions = () => {
        const predictionsElement = document.getElementById('predictions');
        if (predictionsElement) {
            predictionsElement.scrollIntoView({ behavior: 'smooth' });
        }
    };

    return (
        <Container component="main" maxWidth="sm">
            <CssBaseline />
            <Paper elevation={5} style={{ padding: '2rem', marginTop: '2rem', borderRadius: '10px' }}>
                <Typography variant="h4" gutterBottom align="center">Start Training Now</Typography>
                <Typography variant="body1" gutterBottom align="center">
                    Welcome to the future of data-driven decision-making!
                    <br />
                    Select your options and start training your model to make accurate predictions.
                </Typography>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Symbol</InputLabel>
                            <Select value={symbol} onChange={(e) => setSymbol(e.target.value as string)}>
                                {['AAPL', 'GOOGL', 'MSFT', 'AMZN'].map(sym => (
                                    <MenuItem key={sym} value={sym}>{sym}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Learning Type</InputLabel>
                            <Select value={selectedLearningType} onChange={(e) => setSelectedLearningType(e.target.value as string)}>
                                {['Supervised', 'Unsupervised'].map(type => (
                                    <MenuItem key={type} value={type}>{type}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Category</InputLabel>
                            <Select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value as string)}>
                                {Object.keys(learningTypes[selectedLearningType] || {}).map(category => (
                                    <MenuItem key={category} value={category}>{category}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Model</InputLabel>
                            <Select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value as string)}>
                                {(learningTypes[selectedLearningType]?.[selectedCategory] || []).map(model => (
                                    <MenuItem key={model} value={model}>{model}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <StyledDatePicker
                            selected={startDate}
                            onChange={(date) => setStartDate(date as Date)}
                            dateFormat="dd/MM/yyyy"
                            placeholderText="Start Date"
                            maxDate={endDate}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                    <StyledDatePicker
                        selected={endDate}
                        onChange={(date) => setEndDate(date as Date)}
                        dateFormat="dd/MM/yyyy"
                        placeholderText="End Date"
                        minDate={startDate}
                        maxDate={new Date()} // This ensures the maximum date that can be picked is today.
                    />

                    </Grid>
                    <Grid item xs={12}>
                        {isTraining ? (
                            <Box mt={2}>
                                <Typography variant="body1">Training in progress...</Typography>
                                <LinearProgress variant="determinate" value={progress} />
                            </Box>
                        ) : (
                            <Button variant="contained" color="primary" onClick={() => { startTraining(); scrollToPredictions(); }} fullWidth>
                                Start Training
                            </Button>
                        )}
                    </Grid>
                </Grid>
                {validationError &&
                    <Snackbar open={true} autoHideDuration={6000}>
                        <Alert severity="error">{validationError}</Alert>
                    </Snackbar>
                }
                {serverFeedback && <Box mt={2}><Alert severity="info">{serverFeedback}</Alert></Box>}
            </Paper>
            {predictionResults.length > 0 && (
  <Paper 
  elevation={3} 
  style={{ 
      marginTop: '2rem', 
      padding: '1rem', 
      borderRadius: '10px', 
      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)' 
  }} 
  id="predictions"
>
  <Typography variant="h5" gutterBottom align="center" color="secondary">
      Prediction Results
  </Typography>
  <Typography variant="body1" gutterBottom align="center">
      These are the results of your model's predictions, assessed by Mean Absolute Error (MAE). A lower MAE value indicates better accuracy.
  </Typography>
  <Box mt={2}>
      <TableContainer component={Paper}>
          <Table>
              <TableHead>
                  <TableRow>
                      <TableCell>MAE Val</TableCell>
                      <TableCell>MAE Test</TableCell>
                  </TableRow>
              </TableHead>
              <TableBody>
                {predictionResults.map((result, index) => (
                    <TableRow key={index}>
                        <TableCell style={highlightStyle}>{result.mae_val}</TableCell>
                        <TableCell style={highlightStyle}>{result.mae_test}</TableCell>
                    </TableRow>
                ))}
            </TableBody>

          </Table>
      </TableContainer>
  </Box>

  <Typography variant="body1" style={{ marginTop: '1rem' }}>
      These values reflect the quality of your predictions:
  </Typography>
  <ul>
      <li>
          <Typography variant="body1">
              <strong>MAE Val (Validation):</strong> Refers to the prediction accuracy on the training data. A lower value is better.
          </Typography>
      </li>
      <li>
          <Typography variant="body1">
              <strong>MAE Test:</strong> Measures the model's accuracy on new, unseen data. Aim for a low score!
          </Typography>
      </li>
  </ul>

  {!isAuthenticated ? (
      <Typography variant="body1" style={{ marginTop: '1rem', color: '#E91E63', fontWeight: 'bold' }}>
          Unlock advanced features! <EnhancedLink href="/login">Log in</EnhancedLink> or <EnhancedLink href="/signup">Sign up</EnhancedLink> now.
      </Typography>
  ) : (
      <Typography variant="body1" style={{ marginTop: '1rem' }}>
          Dive deeper into the world of data modeling with our advanced features.
      </Typography>
  )}
</Paper>
)}

        </Container>
    );
};

export default TrainingDemo;
