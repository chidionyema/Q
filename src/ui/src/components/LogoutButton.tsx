import { apiProxy } from '../utility/apiProxy; 
import { useRouter } from 'next/router';

const Logout = () => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      // Specify the logout API endpoint and method (e.g., POST or GET)
      const response = await apiProxy('/logout', 'POST');

      // Handle the response as needed
      if (response.success) {
        // Logout was successful, clear any local session or cookies
        router.push('/login'); // Redirect to the login page or another page
      } else {
        // Handle logout failure or error
        console.error('Logout failed:', response.message);
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return (
    <div>
      <h1>Logout</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;
