import { User } from '../types';

export async function fetchUser(): Promise<User> {
  const response = await fetch('/api/user');  // adjust the endpoint as per your backend
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  const user: User = await response.json();
  return user;
}
