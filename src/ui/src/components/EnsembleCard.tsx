import React from 'react';
import { Card, CardActionArea, CardContent, Typography } from '@material-ui/core';

type EnsembleCardProps = {
  ensemble: {
    id: number;
    code: string;
    name: string;
  };
  onClick: (ensembleCode: string) => void;
};

const EnsembleCard: React.FC<EnsembleCardProps> = ({ ensemble, onClick }) => {
  return (
    <Card onClick={() => onClick(ensemble.code)}>
      <CardActionArea>
        <CardContent>
          <Typography variant="h5">{ensemble.name}</Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default EnsembleCard;
