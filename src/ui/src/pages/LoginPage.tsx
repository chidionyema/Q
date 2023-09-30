import { NextPage } from 'next';
import { setToken, setCookie, setUsername } from '../utility/sessionManager';
import { APIProxy } from '../utility/apiProxy';
import { useApiCall } from '../hooks/useApiCall';
import React, { useState, FormEvent } from 'react';
import { useRouter } from 'next/router';

// Create a single instance of APIProxy
const apiProxyInstance = new APIProxy();

const LoginPage: NextPage = () => {
    const handleGoogleLogin = () => {
        window.location.href = 'https://api.dev.io:5000/login/google';
    };
    const [message, setMessage] = useState('');
    const [credentials, setCredentials] = useState({ email: '', password: '' });
    const loginApi = useApiCall(apiProxyInstance.fetchEndpoint);
    const router = useRouter();

    const handleCustomLogin = async (e: FormEvent) => {
        e.preventDefault();
    
        // Validation and error handling code here
    
        setMessage('Validation successful. Making API call to login endpoint...');
    
        try {
          // Make the API call
          const response = await loginApi.call('/login', {
            method: 'POST',
            body: JSON.stringify(credentials),
            credentials: 'include',
          });
    
          if (response && response.token) {
            // Login successful, use the session management functions
            setToken(response.token);
            setUsername(credentials.email);
           // setIsAuthenticated(true);
            setCookie('auth_cook', response.token as string, 30);
            setMessage('Login successful! Redirecting to the home page in 3 seconds...');
            setTimeout(() => {
              router.push('/');
            }, 3000);
          } else if (response && response.error) {
            // Handle errors from the API response
            setMessage(`Error: ${response.error}`);
          } else {
            setMessage('Login failed. Please try again.');
          }
        } catch (error) {
          console.error('Error during login:', error);
          setMessage('Login failed. Please try again.');
        }
      };

    return (
        <div style={{ 
            fontFamily: 'Arial, sans-serif', 
            padding: '20px', 
            backgroundColor: '#f8f8f8', 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            height: '100vh', 
        }}>
            <h4 style={{ margin: '10px 0', color: '#2c3e50' }}>Login</h4>

            <form onSubmit={handleCustomLogin} style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                width: '80%', 
                backgroundColor: '#ffffff', 
                padding: '20px',
                borderRadius: '8px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' 
            }}>
                <input 
                    type="email"
                    required
                    placeholder="Email Address"
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '4px', border: '1px solid #d6d6d6' }}
                />
                <input 
                    type="password"
                    required
                    placeholder="Password"
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '4px', border: '1px solid #d6d6d6' }}
                />
                <button 
                    type="submit" 
                    style={{ 
                        backgroundColor: '#3498db', 
                        color: '#ffffff', 
                        padding: '10px 20px', 
                        border: 'none', 
                        borderRadius: '5px', 
                        cursor: 'pointer', 
                        transition: 'background-color 0.3s', 
                        width: '100%', 
                        margin: '10px 0'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#2980b9'}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#3498db'}
                >
                    Login
                </button>
            </form>
            
            <div style={{ margin: '20px 0', width: '80%', height: '1px', backgroundColor: '#e0e0e0' }}></div>

            <button 
                style={{ 
                    backgroundColor: '#db4437', 
                    border: '1px solid #d23f31', 
                    color: '#ffffff', 
                    padding: '10px 20px', 
                    borderRadius: '5px', 
                    cursor: 'pointer', 
                    transition: 'background-color 0.3s', 
                    width: '80%', 
                    margin: '10px 0'
                }}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#c53929'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#db4437'}
                onClick={handleGoogleLogin}
            >
                Login with Google
            </button>
            
            <a href="/register" style={{ marginTop: '10px', color: '#3f51b5', textDecoration: 'none', cursor: 'pointer' }}>Not a member? Register here.</a>
        </div>
    );
}

export default LoginPage;
