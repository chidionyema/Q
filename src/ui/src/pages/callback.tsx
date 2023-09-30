import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import { setToken, getToken, clearToken, setCookie, clearCookie } from '../utility/sessionManager';
import { useAuth } from '../contexts/authContext';

const Callback = () => {
  const router = useRouter();
  const { setIsAuthenticated } = useAuth();

  useEffect(() => {
    const token = router.query.token;

    if (token) {
      setToken(token as string); // Store the token in the utility
      setCookie('auth_cook', token as string, 30); // Store the token in a session cookie
      setIsAuthenticated(true);
      // On successful login from the server
      router.push('/');
    } else {
      console.error("Token missing from callback");
      clearToken(); 
      clearCookie('auth_cook')
    }
  }, [router, setIsAuthenticated]);

  return (
    <div>
      Processing login...
    </div>
  );
};

export default Callback;
