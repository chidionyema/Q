// pages/auth/success.tsx

import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Cookies from 'cookie-js';
import { useAuthStore } from '../stores/authStore';

const AuthSuccess: NextPage = () => {
  const router = useRouter();
  const setToken = useAuthStore((state) => state.setToken);
  const setUser = useAuthStore((state) => state.setUser);

  useEffect(() => {
    const token = Cookies.get('auth_token');

    if (token) {
      console.log('Token acquired:', token);
      setToken(token);
      // TODO: Use the token to fetch user data from your backend and set the user data
      // e.g., setUser({ name: "John Doe", email: "john.doe@example.com" });
      router.push('/dashboard');
    } else {
      console.error('No token found!');
      router.push('/login');
    }
  }, []);

  return <div>Processing...</div>;
}

export default AuthSuccess;
