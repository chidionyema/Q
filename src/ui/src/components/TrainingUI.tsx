import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import axios from 'axios';

const TrainingDemo = () => {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const socket = io.connect('https://api.dev.io:5000/training');

        socket.on('progress', (data) => {
            setProgress(data.progress);
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    const startTraining = async () => {
        try {
            const response = await axios.post('https://api.dev.io:5000/startTraining', {
                symbol: "ExampleSymbol",
                start_date: "2022-01-01",
                end_date: "2023-01-01",
                model: "ExampleModel"
            });

            console.log(response.data);
        } catch (error) {
            console.error("Error starting training:", error);
        }
    };

    return (
        <div> <h2>Start Training Now</h2>
        
        {maeVal && <p><strong>MAE Val:</strong> {maeVal}</p>}
        {maeTest && <p><strong>MAE Test:</strong> {maeTest}</p>}
        
        {/* Display server feedback */}
        {serverFeedback && <div className="feedback">{serverFeedback}</div>}
        
        {/* Display validation error */}
        {validationError && <div className="error">{validationError}</div>}
  
            <div>
                Training Progress: {progress}%
            </div>
            <button onClick={startTraining}>Start Training</button>
        </div>
    );
};

export default TrainingDemo;
