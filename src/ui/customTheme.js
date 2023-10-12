import { createTheme } from '@mui/material/styles';

const customTheme = createTheme({
  palette: {
    // Customize your theme colors here
    primary: {
      main: '#ff5722', // Change this to your desired primary color
    },
    secondary: {
      main: '#2196f3', // Change this to your desired secondary color
    },
    // Add more palette customization if needed
  },
  typography: {
    // Customize typography styles here
    fontFamily: 'Roboto, sans-serif',
  },
});

export default customTheme;
