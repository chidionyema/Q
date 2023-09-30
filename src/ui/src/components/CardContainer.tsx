import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ModelCard from './ModelCard';
import EnsembleCard from './EnsembleCard';
import OptimizationCard from './OptimizationCard';
import { useSpring, animated } from 'react-spring';
import { Grid, Breadcrumbs, Link } from '@material-ui/core';

const CardContainer: React.FC = () => {
  const [models, setModels] = useState([]);
  const [ensembleStrategies, setEnsembleStrategies] = useState([]);
  const [optimizationTechniques, setOptimizationTechniques] = useState([]);
  const [selectedModel, setSelectedModel] = useState<string | null>(null);
  const [selectedEnsemble, setSelectedEnsemble] = useState<string | null>(null);

  const fadeIn = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
  });

  const AnimatedModelCard = animated(ModelCard);
  const AnimatedEnsembleCard = animated(EnsembleCard);
  const AnimatedOptimizationCard = animated(OptimizationCard);

  useEffect(() => {
    async function fetchData() {
      try {
        const modelResponse = await axios.get('/data/modelClasses.json');
        const ensembleResponse = await axios.get('/data/ensembleStrategies.json');
        const optimizationResponse = await axios.get('/data/optimizationTechniques.json');

        setModels(modelResponse.data);
        setEnsembleStrategies(ensembleResponse.data);
        setOptimizationTechniques(optimizationResponse.data);
      } catch (error) {
        console.error("Error fetching data", error);
      }
    }

    fetchData();
  }, []);

  return (
    <div>
      <Breadcrumbs aria-label="breadcrumb">
        <Link color="inherit" href="#" onClick={() => { setSelectedModel(null); setSelectedEnsemble(null); }}>
          Models
        </Link>
        {selectedModel && <Link color="inherit" href="#" onClick={() => setSelectedEnsemble(null)}>
          {selectedModel}
        </Link>}
        {selectedEnsemble && <Link color="inherit">{selectedEnsemble}</Link>}
      </Breadcrumbs>

      <Grid container spacing={3}>
        {!selectedModel && models.map((model) => (
          <Grid item xs={12} sm={6} md={4} key={model.id}>
            <AnimatedModelCard style={fadeIn} model={model} onClick={setSelectedModel} />
          </Grid>
        ))}
        {selectedModel && !selectedEnsemble && ensembleStrategies.map((ensemble) => (
          <Grid item xs={12} sm={6} md={4} key={ensemble.id}>
            <AnimatedEnsembleCard style={fadeIn} ensemble={ensemble} onClick={setSelectedEnsemble} />
          </Grid>
        ))}
        {selectedEnsemble && optimizationTechniques.map((optimization) => (
          <Grid item xs={12} sm={6} md={4} key={optimization.id}>
            <AnimatedOptimizationCard style={fadeIn} optimization={optimization} />
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default CardContainer;
