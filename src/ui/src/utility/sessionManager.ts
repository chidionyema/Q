// utility/sessionManager.ts

// Define a function to get the session token
export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('jwt');
  }
  return null;
}

// Define a function to set the session token
export function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('jwt', token);
  }
}

// Define a function to clear the session token
export function clearToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('jwt');
  }
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
  if (typeof window !== 'undefined') {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
  }
  return null;
}

// Define a function to set a cookie with a specified expiration (in days)
export function setCookie(name: string, value: string, days: number = 7): void {
  if (typeof window !== 'undefined') {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value};${expires};path=/`;
  }
}

// Define a function to clear a cookie by name
export function clearCookie(name: string): void {
  if (typeof window !== 'undefined') {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}
