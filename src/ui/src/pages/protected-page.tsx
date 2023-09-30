import { useSession } from "next-auth/react";

const ProtectedComponent: React.FC = () => {
  const { data: session } = useSession();

  if (!session) {
    return <p>You must be logged in to view this content.</p>;
  }

  return <p>Protected content here.</p>;
};

export default ProtectedComponent;
