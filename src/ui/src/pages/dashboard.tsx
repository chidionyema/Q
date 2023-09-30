import { GetServerSideProps } from 'next';
import { getSession } from 'next-auth/react';

const Dashboard: React.FC = () => {
  return <div>Your protected content here</div>;
};

export default Dashboard;

export const getServerSideProps: GetServerSideProps = async (context) => {
  const session = await getSession(context);

  if (!session) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }

  return { props: {} };
};
