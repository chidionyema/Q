import React, { useState } from 'react';
import Link from 'next/link';

const Faq = () => {
  const [activeFAQ, setActiveFAQ] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setActiveFAQ(activeFAQ === index ? null : index);
  };

  const faqItems = [
    {
      question: 'What is this application for?',
      answer: 'This application is for training trading models.',
    },
    {
      question: 'How do I get started?',
      answer: 'Go to the Training page to start configuring your model.',
    },
    {
      question: 'Is this free to use?',
      answer: 'Yes, it is completely free to use.',
    },
  ];

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '40px', backgroundColor: '#fafafa', maxWidth: '800px', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '40px' }}>Frequently Asked Questions</h2>
      {faqItems.map((item, index) => (
        <div 
          key={index} 
          onClick={() => toggleFAQ(index)}
          style={{ 
            background: 'linear-gradient(135deg, #ecf0f1, #fff)',
            padding: '20px', 
            borderRadius: '10px', 
            marginBottom: '20px', 
            boxShadow: '0 5px 15px rgba(0, 0, 0, 0.1)',
            transition: 'all 0.3s',
            cursor: 'pointer',
            transform: activeFAQ === index ? 'scale(1.02)' : 'none'
          }}
          onMouseOver={(e) => e.currentTarget.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.15)'}
          onMouseOut={(e) => e.currentTarget.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)'}
        >
          <h3 style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            fontWeight: 'bold',
            color: '#2c3e50'
          }}>
            {item.question}
            <span>{activeFAQ === index ? '−' : '+'}</span>
          </h3>
          <div style={{ overflow: 'hidden', transition: 'max-height 0.5s ease', maxHeight: activeFAQ === index ? '150px' : '0' }}>
            <p style={{ marginTop: '20px', color: '#7f8c8d' }}>{item.answer}</p>
          </div>
        </div>
      ))}
      <p style={{ textAlign: 'center', marginTop: '30px' }}>
        Ready to start? 
      

      </p>
    </div>
  );
};

export default Faq;



 