import React, { useState } from 'react';
import { AuthContext } from './authContext';
import { getToken, getUsername } from '../utility/sessionManager';

type AuthProviderProps = {
  children: React.ReactNode;
};

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!getToken());
  const [loggedInUsername, setLoggedInUsername] = useState<string | null>(getUsername());

  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, loggedInUsername, setLoggedInUsername }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
