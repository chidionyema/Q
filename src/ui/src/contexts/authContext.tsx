import React, { useContext } from 'react';

// Define the context's types
type AuthContextType = {
  isAuthenticated: boolean;
  setIsAuthenticated: React.Dispatch<React.SetStateAction<boolean>>;
  loggedInUsername: string | null;
  setLoggedInUsername: React.Dispatch<React.SetStateAction<string | null>>;
};

// Create the context with the type and default value as undefined
export const AuthContext = React.createContext<AuthContextType | undefined>(undefined);

// Custom hook for easier context access
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
