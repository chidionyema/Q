// pages/api/users.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { apiProxy } from '../../utility/apiProxy';

export default async (
  req: NextApiRequest,
  res: NextApiResponse<any>
) => {
  try {
    if (req.method === 'GET') {
      // Use apiProxy to fetch data from the Python backend
      const users = await apiProxy('/fetch-optimizers', 'GET');

      // Return the data from the Python backend
      res.status(200).json(users);
    } else {
      // Handle unsupported methods
      res.status(405).json({ error: 'Method not allowed' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
