import React, { useState, FormEvent } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../contexts/authContext';
import { setToken, setCookie, setUsername } from '../utility/sessionManager';
import { APIProxy } from '../utility/apiProxy';
import { useApiCall } from '../hooks/useApiCall';

// Create a single instance of APIProxy
const apiProxyInstance = new APIProxy();

const Register: React.FC = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [message, setMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const { setIsAuthenticated, setLoggedInUsername } = useAuth();
  const registerApi = useApiCall(apiProxyInstance.fetchEndpoint);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(credentials.email)) {
      setMessage('Invalid email format!');
      return;
    }

    if (credentials.password.length < 8) {
      setMessage('Password should be at least 8 characters!');
      return;
    }

    setMessage('Validation successful. Making API call to register endpoint...');

    try {
      // Make the API call
      const response = await registerApi.call('/register', {
        method: 'POST',
        body: JSON.stringify(credentials),
        credentials: 'include',
      });

      // Check if 'token' exists in the response data
      if (response && response.token) {
        // Registration successful, use the session management functions
        setToken(response.token);
        setUsername(credentials.email);
       // setIsAuthenticated(true);
        setCookie('auth_cook', response.token as string, 30);
        setLoggedInUsername(credentials.email);

        setMessage('Registration successful! Redirecting to the home page in 3 seconds...');
        setTimeout(() => {
          router.push('/');
        }, 3000);
      } else if (response && response.error) {
        // Handle errors from the API response
        setMessage(`Error: ${response.error}`);
      } else {
        setMessage('Registration failed. Please try again.');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      setMessage('Registration failed. Please try again.');
    }
  };

  
  
  


  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', backgroundColor: '#f8f8f8', display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh' }}>
      <h4 style={{ margin: '10px 0', color: '#2c3e50' }}>Register</h4>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: '80%', backgroundColor: '#ffffff', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)' }}>
        <input
          type="email"
          required
          placeholder="Email"
          value={credentials.email}
          onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
          style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '4px', border: '1px solid #d6d6d6' }}
        />
        <div style={{ position: 'relative' }}>
          <input
            type={showPassword ? "text" : "password"}
            required
            placeholder="Password"
            value={credentials.password}
            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
            style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '4px', border: '1px solid #d6d6d6' }}
          />
          <span onClick={() => setShowPassword(!showPassword)} style={{ position: 'absolute', right: '10px', top: '15px', cursor: 'pointer' }}>
            {showPassword ? "Hide" : "Show"}
          </span>
        </div>
        <button
          type="submit"
          style={{ backgroundColor: '#3498db', color: '#ffffff', padding: '10px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer', transition: 'background-color 0.3s', width: '100%', margin: '10px 0' }}
          onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#2980b9'}
          onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#3498db'}
        >
          {registerApi.loading ? "Loading..." : "Register"}
        </button>
      </form>

      {message && <p style={{ color: 'red' }}>{message}</p>}
    </div>
  );
};

export default Register;
