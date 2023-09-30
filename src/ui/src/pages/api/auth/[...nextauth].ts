


// src/pages/api/auth/[nextauth].ts
import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import axios from 'axios';
import CredentialsProvider from "next-auth/providers/credentials";

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    CredentialsProvider({
      id: "credentials-login-register",
      name: "Email and Password",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
        isRegistration: { label: "Registration", type: "hidden" } // Additional field to determine if the flow is for registration
      },
      authorize: async (credentials) => {
        try {
          let user;
          
          // Check if it's a registration flow based on the `isRegistration` field
          if (credentials.isRegistration) {
            const registrationResponse = await axios.post(`${process.env.BACKEND_URL}/register`, {
                email: credentials.email,
                password: credentials.password
            });
            user = registrationResponse.data;
          } else {
            const loginResponse = await axios.post(`${process.env.BACKEND_URL}/login`, {
                email: credentials.email,
                password: credentials.password
            });
            user = loginResponse.data;
          }

          if (user && user.email) {
            return { email: user.email, id: user.id, name: user.name || "User" };
          } else {
            throw new Error('Invalid data or registration/login failed');
          }
        } catch (error) {
          console.error(error.message);
          throw new Error('Server error during login/registration');
        }
      }
    })
  ],

  jwt: {
    secret: process.env.SECRET,
  },
  session: {
    jwt: true,
  },
  callbacks: {
    async signIn(user, account, profile) {

      return true;
    },
    async jwt(token, user, account, profile, isNewUser) {
      console.log("User:", user);
      console.log("Profile:", profile);
      return token;
  },
  
  async session(session, token) {
    console.log("session" + session);
    console.log("token" + token);
    return session;
},


  }
});
