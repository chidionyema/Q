// pages/reset-password.tsx

import { useState, FormEvent } from 'react';

const ResetPassword: React.FC = () => {
    const [email, setEmail] = useState<string>('');
    const [message, setMessage] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await apiProxy('/request-password-reset', 'POST', { email });
            setMessage('Password reset link sent. Check your email.');
            setLoading(false);
        } catch (error) {
            setMessage('Failed to send reset link. Please try again.');
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Reset Password</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    Send Reset Link
                </button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default ResetPassword;
