import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { getToken, clearToken, clearCookie } from '../utility/sessionManager';
import { fetchUserAuthenticationStatus } from '../utility/authHelper';
import { useApiCall } from '../hooks/useApiCall';
import { APIProxy } from '../utility/apiProxy';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { useMediaQuery, Theme } from '@mui/material';
import { Divider } from '@mui/material';
import customTheme from '../../customTheme'; // Adjust the path as needed

import {
  AppBar,
  Toolbar,
  Button,
  Drawer,
  List,
  ListItem,
  IconButton,
  Typography,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import { Box } from '@mui/system';

const apiProxyInstance = new APIProxy();

const NavBar: React.FC = () => {
  const router = useRouter();
  const [darkMode, setDarkMode] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [loggedInUsername, setLoggedInUsername] = useState<string | null>(null);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const matchesSm = useMediaQuery((theme: Theme) => theme.breakpoints.down('sm'));

  const logoutApi = useApiCall(apiProxyInstance.fetchEndpoint);
  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/train', label: 'Explore Models' },
    { path: '/about', label: 'About Us' },
    { path: '/services', label: 'Services' },
    { path: '/contact', label: 'Contact' },
    { path: '/blog', label: 'Blog' },
    { path: '/portfolio', label: 'Portfolio' },
    { path: '/team', label: 'Our Team' },
    // ... [You can add even more items as needed]
  ];

  const lightTheme = createTheme({
    palette: {
      type: 'light',
      primary: {
        main: '#ff5722',
      },
      secondary: {
        main: '#2196f3',
      },
      background: {
        default: '#f5f5f5',
        paper: '#ffffff',
      },
    },
    typography: {
      fontFamily: 'Roboto, sans-serif',
    },
  });

  const darkTheme = createTheme({
    palette: {
      type: 'dark',
      primary: {
        main: '#ff5722',
      },
      secondary: {
        main: '#2196f3',
      },
      background: {
        default: '#303030',
        paper: '#424242',
      },
    },
    typography: {
      fontFamily: 'Roboto, sans-serif',
    },
  });

  const handleLogout = async () => {
    const sessionToken = getToken();
    try {
      const { message, error } = await logoutApi.call('/logout', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${sessionToken}`,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        credentials: 'include',
      });

      if (message) {
        clearToken();
        setIsAuthenticated(false);
        setLoggedInUsername(null);
        clearCookie('auth_cook');
        router.push('/');
        toast.success('Logged out successfully!');
      } else if (error) {
        toast.error(error);
      } else {
        toast.error('Logout failed. Please try again.');
      }
    } catch (error) {
      toast.error('Logout failed. Please try again.');
    }
  };

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  useEffect(() => {
    const checkAuthenticationStatus = async () => {
      const userIsAuthenticated = await fetchUserAuthenticationStatus();
      setIsAuthenticated(userIsAuthenticated);
      if (userIsAuthenticated) {
        const username = 'chid'; // Replace with the actual logic to get the username
        setLoggedInUsername(username);
      }
    };
    checkAuthenticationStatus();
  }, [getToken()]);

  return (
    <ThemeProvider theme={darkMode ? darkTheme : lightTheme}>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
        <AppBar position="static" color={darkMode ? 'default' : 'primary'}>
          <Toolbar
            sx={{
              display: 'flex',
              alignItems: 'center',
              padding: matchesSm ? '0 1rem' : '0 2rem',
            }}
          >
            <Link href="/" passHref>
              <Typography
                variant="h6"
                component="div"
                sx={{
                  cursor: 'pointer',
                  marginLeft: matchesSm ? '68rem' : '68rem',
                  marginRight: '0.5rem',
                }}
              >
                Q-Trader
              </Typography>
            </Link>
            {matchesSm ? (
              <IconButton
                color="inherit"
                sx={{ marginRight: '1rem' }}
                onClick={() => setMobileNavOpen(true)}
              >
                <MenuIcon />
              </IconButton>
            ) : (
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2,
                  flexGrow: 1,
                  justifyContent: 'left',
                  marginLeft: '0.2rem',
                }}
              >
                {navItems.map((item, index) => (
                  <React.Fragment key={item.path}>
                    {index > 0 && (
                      <Divider orientation="vertical" flexItem sx={{ height: 24, mx: 1, bgcolor: 'text.primary' }} />
                    )}
                    <Link href={item.path} passHref>
                      <Button color="inherit">{item.label}</Button>
                    </Link>
                  </React.Fragment>
                ))}
                <Divider orientation="vertical" flexItem sx={{ height: 24, mx: 1, bgcolor: 'text.primary' }} />
                <Button color="inherit" onClick={toggleTheme}>
                  {darkMode ? 'Light Mode' : 'Dark Mode'}
                </Button>
                {isAuthenticated ? (
                  <>
                    <Typography sx={{ ml: 2 }}>Welcome, {loggedInUsername}!</Typography>
                    <Button color="inherit" onClick={handleLogout}>
                      Logout
                    </Button>
                  </>
                ) : (
                  <Link href="/LoginPage" passHref>
                    <Button color="inherit">Login</Button>
                  </Link>
                )}
              </Box>
            )}
          </Toolbar>
        </AppBar>
      </motion.div>
    </ThemeProvider>
  );
};

export default NavBar;