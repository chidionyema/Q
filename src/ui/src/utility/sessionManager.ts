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

export function setCookie(name: string, value: string, hours : number = 1, secure = true) {
  if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
    const date = new Date();
    date.setTime(date.getTime() + hours * 60 * 60 * 1000); // Set expiration time to one hour
    const expires = `expires=${date.toUTCString()}`;
    const secureAttribute = secure ? 'Secure;' : ''; // Add the 'Secure' attribute if secure is true
    document.cookie = `${name}=${value};${expires};path=/;${secureAttribute}`;
  }
}


// Define a function to clear a cookie by name
export function clearCookie(name: string): void {
  if (typeof window !== 'undefined') {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}
