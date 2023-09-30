import React from 'react';
import { Card, CardActionArea, CardContent, Typography } from '@material-ui/core';

type OptimizationCardProps = {
  optimization: {
    id: number;
    code: string;
    name: string;
  };
};

const OptimizationCard: React.FC<OptimizationCardProps> = ({ optimization }) => {
  return (
    <Card>
      <CardActionArea>
        <CardContent>
          <Typography variant="h5">{optimization.name}</Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default OptimizationCard;
