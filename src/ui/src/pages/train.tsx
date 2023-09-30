import React from 'react';
import FeasibilityMatrix from '../components/FeasibilityMatrix'; // Import the TrainingUI component

const Train: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
  <FeasibilityMatrix></FeasibilityMatrix>
    </div>
  );
};

export default Train;
