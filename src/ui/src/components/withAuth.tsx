import { useEffect } from 'react';
import { useRouter } from 'next/router';

const withAuth = (WrappedComponent) => {
    return (props) => {
        const router = useRouter();
        const jwtToken = localStorage.getItem('jwt');
        useEffect(() => {
            if (!jwtToken) {
                router.push('/login');
            }
        }, []);
        return <WrappedComponent {...props} />;
    };
};

export default withAuth;
