// components/LatestAINews.tsx

import React from 'react';
import { Typography } from '@mui/material';

const LatestAINews: React.FC = () => {
  return (
    <div>
      <Typography variant="h6" gutterBottom>Latest AI News</Typography>
      <div>
        {/* Add your latest AI news articles or content here */}
        <div>
          <strong>Article 1:</strong> Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </div>
        <div>
          <strong>Article 2:</strong> Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        </div>
        <div>
          <strong>Article 3:</strong> Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
        </div>
        {/* Add more articles as needed */}
      </div>
    </div>
  );
};

export default LatestAINews;
