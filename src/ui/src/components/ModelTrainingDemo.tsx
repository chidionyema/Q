import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import io from 'socket.io-client';
import axios from 'axios';
import {
    Button, FormControl, Select, InputLabel, 
    CircularProgress, Snackbar, LinearProgress, Typography, MenuItem, Box, Grid, Container, Paper, CssBaseline
} from '@mui/material';
import Alert from '@mui/material/Alert';
import 'react-datepicker/dist/react-datepicker.css';
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
    const [selectedLearningType, setSelectedLearningType] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [symbol, setSymbol] = useState('');
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    const [validationError, setValidationError] = useState('');
    const [serverFeedback, setServerFeedback] = useState('');
    const [maeVal, setMaeVal] = useState(null);
    const [maeTest, setMaeTest] = useState(null);

    const learningTypes = {
        'Supervised': {
            'Linear Models': ['Linear Regression', 'Logistic Regression'],
            'Decision Trees': ['Random Forest', 'Decision Tree', 'Extra Trees']
        },
        'Unsupervised': {
            'Dimensionality Reduction': ['Principal Component Analysis (PCA)']
        }
    };

    useEffect(() => {
        const socket = io('https://api.dev.io:5000/training');
        socket.on('progress', (data) => {
            setProgress(Number(data.progress));
        });
        
        return () => {
            socket.disconnect();
        };
    }, []);

    const startTraining = async () => {
        setIsTraining(true);
        setIsLoading(true);
        try {
            const response = await axios.post('https://api.dev.io:5000/startTraining', {
                symbol: symbol,
                start_date: startDate,
                end_date: endDate,
                model: selectedModel
            });
            const { mae_val, mae_test } = response.data;
            setMaeVal(mae_val);
            setMaeTest(mae_test);
            setIsTraining(false);
            setIsLoading(false);
        } catch (error) {
            setIsTraining(false);
            setIsLoading(false);
            setServerFeedback("Error during training.");
        }
    };

    return (
        <Container component="main" maxWidth="sm">
            <CssBaseline />
            <Paper elevation={5} style={{ padding: '2rem', marginTop: '2rem' }}>
                <Typography variant="h4" gutterBottom align="center">Start Training Now</Typography>
                {maeVal && <Typography variant="body1"><strong>MAE Val:</strong> {maeVal}</Typography>}
                {maeTest && <Typography variant="body1"><strong>MAE Test:</strong> {maeTest}</Typography>}
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Symbol</InputLabel>
                            <Select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
                                {['AAPL', 'GOOGL', 'MSFT', 'AMZN'].map(sym => (
                                    <MenuItem key={sym} value={sym}>{sym}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Learning Type</InputLabel>
                            <Select value={selectedLearningType} onChange={(e) => setSelectedLearningType(e.target.value)}>
                                {Object.keys(learningTypes).map(type => (
                                    <MenuItem key={type} value={type}>{type}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Category</InputLabel>
                            <Select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
                                {Object.keys(learningTypes[selectedLearningType] || {}).map(category => (
                                    <MenuItem key={category} value={category}>{category}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12}>
                        <FormControl fullWidth>
                            <InputLabel>Model</InputLabel>
                            <Select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
                                {(learningTypes[selectedLearningType]?.[selectedCategory] || []).map(model => (
                                    <MenuItem key={model} value={model}>{model}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <StyledDatePicker
                            selected={startDate}
                            onChange={(date: Date) => setStartDate(date)}
                            dateFormat="dd/MM/yyyy"
                            placeholderText="Start Date"
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <StyledDatePicker
                            selected={endDate}
                            onChange={(date: Date) => setEndDate(date)}
                            dateFormat="dd/MM/yyyy"
                            placeholderText="End Date"
                        />
                    </Grid>
                    <Grid item xs={12}>
                        {isTraining ? (
                            <Box mt={2}>
                                <Typography variant="body1">Training in progress...</Typography>
                                <LinearProgress variant="determinate" value={progress} />
                            </Box>
                        ) : (
                            <Button variant="contained" color="primary" onClick={startTraining} fullWidth>
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
        </Container>
    );
};

export default TrainingDemo;
