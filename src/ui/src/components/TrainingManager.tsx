import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import SocketManager from './SocketManager'; // Adjust the import based on your project structure

const TrainingManager = ({ symbol, startDate, endDate, model, onTrainingComplete, onTrainingError, onProgress }) => {
  const [isTraining, setIsTraining] = useState(false);

  useEffect(() => {
    const socketManager = SocketManager.getInstance();
    socketManager.connect();

    socketManager.on('connect', () => console.log('Connected to server'));
    socketManager.on('training_complete', (data) => {
      setIsTraining(false);
      onTrainingComplete(data);
    });
    socketManager.on('training_error', (error) => {
      setIsTraining(false);
      onTrainingError(error.message || 'Error during training.');
    });
    socketManager.on('progress', (data) => {
      onProgress(data.percentage);
    });

    return () => {
      socketManager.disconnect();
    };
  }, [onTrainingComplete, onTrainingError, onProgress]);

  const startTraining = () => {
    setIsTraining(true);
    const socketManager = SocketManager.getInstance();
    socketManager.emit('train_model', { symbol, start_date: startDate, end_date: endDate, model });
  };

  return (
    <div>
      <button onClick={startTraining} disabled={isTraining}>Start Training</button>
      {isTraining && <p>Training in progress...</p>}
    </div>
  );
};

export default TrainingManager;
