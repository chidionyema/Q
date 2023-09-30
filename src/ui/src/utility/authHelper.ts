import { getToken, getCookie, clearToken, clearCookie } from '../utility/sessionManager';

export function fetchUserAuthenticationStatus(): boolean {
    try {
      // Check for the session cookie that you previously set in the Callback component
      const cookieToken = getCookie('auth_cook');
      const localToken = getToken()
  
      if (cookieToken && localToken && cookieToken === localToken) {
        // If the cookie exists, consider the user as authenticated
        return true;
      } else {
        // If the cookie is missing, consider the user as not authenticated
        clearToken(); 
        clearCookie('auth_cook')// Clear any invalid or expired tokens from the utility
        return false;
      }
    } catch (error) {
      // Handle any errors that occur during cookie retrieval
      console.error('Error checking authentication status:', error);
      return false;
    }
  }
  