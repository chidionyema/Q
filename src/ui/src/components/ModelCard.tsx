import React from 'react';
import { Card, CardActionArea, CardContent, Typography } from '@material-ui/core';

type ModelCardProps = {
  model: {
    id: number;
    code: string;
    name: string;
  };
  onClick: (modelCode: string) => void;
};

const ModelCard: React.FC<ModelCardProps> = ({ model, onClick }) => {
  return (
    <Card onClick={() => onClick(model.code)}>
      <CardActionArea>
        <CardContent>
          <Typography variant="h5">{model.name}</Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default ModelCard;
