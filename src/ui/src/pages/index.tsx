import React from 'react';
import Link from 'next/link';
import ModelTrainingDemo from '../components/ModelTrainingDemo';
import StepsSection from '../components/StepsSection';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import SearchIcon from '@mui/icons-material/Search';
import SecurityIcon from '@mui/icons-material/Security';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

const HomePage: React.FC = () => {
    return (
        <Box sx={{ fontFamily: '"Poppins", sans-serif', background: 'linear-gradient(135deg, #33364f 0%, #5f667c 100%)', minHeight: '100vh', color: '#FFF', textAlign: 'center', padding: '5% 0' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 60px' }}>
                <Typography variant="h2" gutterBottom>Elevate Your Trading with AI Precision</Typography>
                <Typography variant="body1" gutterBottom>
                    Introducing Q-Trader: Merging the prowess of AI with real-time market intelligence. Seamlessly craft, test, and hone your trading strategies with unmatched accuracy.
                </Typography>

                {/* Model Training Demo */}
                <StepsSection />
                <ModelTrainingDemo />

                <Box sx={{ display: 'flex', gap: '20px', mt: 4 }}>
                    <Link href="/signup" passHref>
                        <Button variant="contained">Dive In</Button>
                    </Link>
                    <Link href="/models" passHref>
                        <Button variant="contained">Explore Our Models</Button>
                    </Link>
                    <Link href="/leaderboard" passHref>
                        <Button variant="contained">Check The Leaderboard</Button>
                    </Link>
                </Box>

                <Typography variant="h4" gutterBottom mt={8}>Why Is Q-Trader a Game-Changer?</Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', p: 0 }}>
                    <Box>
                        {/* Replace with Robot icon when available */}
                        <SearchIcon fontSize="large" color="action" />
                        State-of-the-art trading algorithms at your fingertips.
                    </Box>
                    <Box>
                        <SearchIcon fontSize="large" color="action" />
                        Insights powered by meticulous data analysis.
                    </Box>
                    <Box>
                        <AccessTimeIcon fontSize="large" color="action" />
                        Witness real-time performance via immersive dashboards.
                    </Box>
                    <Box>
                        <SecurityIcon fontSize="large" color="action" />
                        Robust risk management tools fortifying your investments.
                    </Box>
                </Box>

                <Box mt={8}>
                    <Typography variant="body1" gutterBottom>
                        Join the revolution. A community where novice traders and seasoned experts converge. Q-Trader delivers bespoke tools and insights tailored for every trading journey.
                    </Typography>
                    <Link href="/signup" passHref>
                        <Button variant="contained" color="secondary">Embark Now</Button>
                    </Link>
                </Box>
            </Box>
        </Box>
    );
};

export default HomePage;
