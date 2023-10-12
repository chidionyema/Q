// utility/sessionManager.ts
import { parse } from 'cookie';

export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    // Get the 'auth_tok' cookie value from document.cookie
    const cookies = parse(document.cookie);
    const authToken = cookies['auth_tok']; // Retrieve the 'auth_tok' cookie by name

    if (authToken) {
      return authToken; // Return the token if found
    }
  }
  return null; // Return null if the token is not found or if window is undefined
}

// Define a function to get the logged-in username
export function getUsername(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('loggedInUsername');
  }
  return null;
}

// Define a function to set the logged-in username
export function setUsername(username: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('loggedInUsername', username);
  }
}

// Define a function to clear the logged-in username
export function clearUsername(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('loggedInUsername');
  }
}

// Define a function to get a cookie by name
export function getCookie(name: string): string | null {
  console.log("getCookie called for:", name); // Debugging line
  if (typeof window !== 'undefined') {
    const cookies = parse(document.cookie);
    const cookieValue = cookies[name];
    console.log("Parsed cookies:", cookies); // Debugging line
    if (cookieValue !== undefined) {
      return cookieValue;
    }
  }
  return null;
}


// Define a function to clear a cookie by name
export function clearCookie(name: string): void {
  if (typeof window !== 'undefined') {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}
