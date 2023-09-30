// components/Footer.js
import React from 'react';
import Link from 'next/link';
const Footer = () => {
  return (
    <footer>
      {/* Add your footer content here */}
      <p>&copy; 2023 Your Company</p>
      <Link href="/features">Features</Link> | <Link href="/pricing">Pricing</Link> | <Link href="/about">About Us</Link>
    </footer>
  );
};

export default Footer;
