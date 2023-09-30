// components/Layout.tsx
import React from 'react';
import ArrowRightAlt from '@mui/icons-material/ArrowRightAlt';
import Footer from './Footer';
import StockPrices from './StockPrices';
import LatestAINews from './LatestAINews';
import { Box, Container, Typography, Paper, Button } from '@mui/material';

// 1. Declare the children prop
interface LayoutProps {
    children: React.ReactNode;
}

// 2. Use the LayoutProps with your Layout component
const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', fontFamily: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif!important', transition: 'all 0.3s ease' }}>
            <Box component="header" sx={{ textAlign: 'center', p: 2, fontSize: '2rem', fontWeight: 'bold', display: 'flex', justifyContent: 'center', alignItems: 'center', letterSpacing: '2px' }}>
                <Typography variant="h5">Your Logo</Typography>
            </Box>
            
            <Container maxWidth="lg" component="main" sx={{ my: 3, position: 'relative', display: 'flex', gap: 2 }}>
                <Paper elevation={3} sx={{ flex: 1.5, p: 2 }}>
                    <Typography variant="h6" gutterBottom>Did You Know?</Typography>
                    <Typography>
                        Interesting facts related to your application go here.
                    </Typography>
            
                    <Button variant="outlined" startIcon={<ArrowRightAlt />} href="/get-started" sx={{ mt: 2 }}>Start Trading</Button>

                    <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>Advertisement</Typography>
                    <Box sx={{ width: '100%', height: '120px', backgroundColor: 'lightgray', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        Ad space
                    </Box>
            
                    <LatestAINews />
                </Paper>

                <Box sx={{ flex: 2 }}>
                    {children}
                </Box>

                <Paper elevation={3} sx={{ flex: 1.5, p: 2 }}>
                    <Typography variant="h6" gutterBottom>Latest Stock Prices</Typography>
                    <StockPrices />
                    
                    <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>User Testimonial</Typography>
                    <Typography>
                        "This application has been incredibly helpful in my trading journey!" - Satisfied User
                    </Typography>

                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mt: 3 }}>
                        <Button variant="outlined" endIcon={<ArrowRightAlt />} href="/contact">Contact Us</Button>
                        <Button variant="outlined" endIcon={<ArrowRightAlt />} href="/testimonials">Testimonials</Button>
                        <Button variant="outlined" endIcon={<ArrowRightAlt />} href="/faq">FAQ</Button>
                    </Box>
                </Paper>
                
            </Container>
            <Footer />
        </Box>
    );
};

export default Layout;
