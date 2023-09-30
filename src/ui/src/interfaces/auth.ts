// interfaces/auth.ts

export interface UserCredentials {
    email: string;
    password: string;
}

export interface RegisterResponse {
    message: string;
}

// interfaces/auth.ts (add to the existing file)

export interface LoginResponse {
    message: string;
    token?: string;
}