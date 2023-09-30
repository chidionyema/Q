import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useRouter } from 'next/router';
import { getToken, clearToken, clearCookie } from '../utility/sessionManager';
import { fetchUserAuthenticationStatus } from '../utility/authHelper';
import { APIProxy } from '../utility/apiProxy';
import { useApiCall } from '../hooks/useApiCall';

const apiProxyInstance = new APIProxy();

const NavBar: React.FC = () => {
  const router = useRouter();
  const [darkMode, setDarkMode] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [loggedInUsername, setLoggedInUsername] = useState<string | null>(null);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  const logoutApi = useApiCall(apiProxyInstance.fetchEndpoint);

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
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <nav className={`navBar ${darkMode ? 'dark-mode' : 'light-mode'}`}>
        <div className="container">
          <Link href="/">
            <span className="logo">Q-Trader</span>
          </Link>
          <ul className={`navList ${mobileNavOpen ? 'open' : ''}`}>
            <li className="navItem">
              <Link href="/">
                <span>Home</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/train">
                <span>Explore ML Models</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/simulation">
                <span>Backtest and Simulate</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/results">
                <span>Evaluate Performance</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/leaderboardpage">
                <span>Leaderboard</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/FAQ">
                <span>FAQ</span>
              </Link>
            </li>
            <li className="navItem">
              <Link href="/contact">
                <span>Contact</span>
              </Link>
            </li>
          </ul>
          <button onClick={toggleTheme} className="themeButton">
            {darkMode ? 'Light Mode' : 'Dark Mode'}
          </button>
          <button onClick={() => setMobileNavOpen(!mobileNavOpen)} className="mobileNavToggle">
            {mobileNavOpen ? 'Close' : 'Menu'}
          </button>
          {isAuthenticated ? (
            <div className="userLoggedIn">
              <span>Welcome, {loggedInUsername}!</span>
              <button onClick={handleLogout}>Logout</button>
            </div>
          ) : (
            <div className="userLoggedOut">
              <Link href="/LoginPage">
                <span>Login</span>
              </Link>
            </div>
          )}
        </div>
      </nav>

      <style jsx>{`
        .navBar {
          background-color: ${darkMode ? '#2C2C2C' : '#f4f4f4'};
          color: ${darkMode ? '#FFF' : '#333'};
          padding: 15px 0;
          transition: background-color 0.3s;
        }

        .container {
          display: flex;
          justify-content: space-between;
          align-items: center;
          max-width: 1200px;
          margin: 0 auto;
        }

        .logo {
          font-family: 'Poppins', sans-serif;
          font-size: 28px;
          font-weight: bold;
          cursor: pointer;
          transition: color 0.3s;
        }

        .navList {
          display: flex;
          gap: 25px;
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .navItem span {
          cursor: pointer;
          font-family: 'Poppins', sans-serif;
          padding: 8px 16px;
          border-radius: 5px;
          transition: background-color 0.3s, color 0.3s;
        }

        .navItem span:hover {
          background-color: rgba(0, 0, 0, 0.1);
        }

        .themeButton,
        .mobileNavToggle,
        button {
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          font-family: 'Poppins', sans-serif;
          transition: background-color 0.3s, color 0.3s;
          cursor: pointer;
        }

        .themeButton:hover,
        .mobileNavToggle:hover,
        button:hover {
          background-color: rgba(0, 0, 0, 0.1);
        }

        .userLoggedIn,
        .userLoggedOut {
          display: flex;
          align-items: center;
        }

        .userLoggedIn span {
          margin-right: 10px;
        }

        .mobileNavToggle {
          display: none;
          background-color: transparent;
          border: 1px solid currentColor;
        }

        @media (max-width: 768px) {
          .mobileNavToggle {
            display: block;
          }

          .navList {
            display: ${mobileNavOpen ? 'block' : 'none'};
            position: absolute;
            top: 60px;
            left: 0;
            background-color: ${darkMode ? '#2C2C2C' : '#f4f4f4'};
            width: 100%;
            flex-direction: column;
            padding: 10px 0;
          }

          .navItem {
            text-align: center;
            margin: 10px 0;
          }
        }
      `}</style>
      <ToastContainer />
    </motion.div>
  );
};

export default NavBar;
