// pages/auth-verification.tsx

import { useEffect } from 'react';
import { GetServerSideProps } from 'next';
import { useRouter } from 'next/router';
import { getCookie, setUsername } from '../utility/sessionManager';
import { parse } from 'cookie';

const AuthVerification = ({ isAuthenticated, username }: { isAuthenticated: boolean; username: string }) => {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
        // Authentication succeeded, redirect to the homepage with query parameters

        localStorage.setItem('username', username);
        router.push({
          pathname: '/',
          query: {
            isAuthenticated: true, // Include any other query parameters you need
            username: username,
          },
        });
      }
      
  }, [isAuthenticated, router]);


   // Log the values for debugging
   console.log('Client-Side Rendering (AuthVerification):');
   console.log('isAuthenticated:', isAuthenticated);
   console.log('username:', username);
 

  return (
    <div>
      {isAuthenticated ? (
        <p>Welcome, {username}! Authentication succeeded. You are now logged in.</p>
      ) : (
        <p>Authentication failed. Please try again.</p>
      )}
    </div>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
    const username = context.query.username as string || '';
    const token = context.query.token as string || '';

    console.log('token:', token);
    console.log('username:', username);
    
    // Get the 'auth_cook' cookie value from headers
    const authCookieHeader = context.req.headers.cookie || '';
      
    // Parse the 'auth_cook' cookie to get its value
    const authCookies = parse(authCookieHeader);
    const authCook = authCookies['auth_cook'] || ''; // Retrieve the 'auth_cook' cookie by name
  
    let isAuthenticated = false;
  
    if (authCook || token) {
        // If either 'auth_cook' cookie or 'token' exists, create a secure cookie
        const maxAge = 3600; // Set the appropriate expiration time in seconds
        const cookieValue = authCook || token; // Use 'auth_cook' if available, otherwise use 'token'
        
        context.res.setHeader(
          'Set-Cookie',
          `auth_tok=${cookieValue}; Max-Age=${maxAge}; Secure; SameSite=None`
        );
      
        isAuthenticated = true;
      }
      
  
    // Log the values for debugging
    console.log('Server-Side Rendering (getServerSideProps):');
    console.log('isAuthenticated:', isAuthenticated);
    console.log('username:', username);
    console.log('authCook:', authCook);
  
    return {
      props: {
        isAuthenticated,
        username,
      },
    };
  };
  
  
  export default AuthVerification;