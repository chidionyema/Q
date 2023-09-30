import React, { useState } from 'react';

const LeaderboardPage: React.FC = () => {
  const [timeFrame, setTimeFrame] = useState<'day' | 'week' | 'month'>('day');

  const leaderboardData = [
    { rank: 1, username: 'Alice', performance: 90.5, dayPerformance: 1.2, badges: ['🏆', '🌟'] },
    { rank: 2, username: 'Bob', performance: 85.2, dayPerformance: -0.5, badges: ['🌟'] },
    { rank: 3, username: 'Duy', performance: 80, dayPerformance: 1, badges: [] },
  ];

  const toggleButtons = ['day', 'week', 'month'].map((frame) => (
    <button
      key={frame}
      style={{
        backgroundColor: timeFrame === frame ? '#3498db' : '#e7e7e7',
        color: timeFrame === frame ? '#ffffff' : '#333',
        padding: '10px 20px',
        margin: '0 5px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s',
      }}
      onClick={() => setTimeFrame(frame)}
      onMouseOver={(e) => {
        if (frame !== timeFrame) {
          e.currentTarget.style.backgroundColor = '#d6d6d6';
        }
      }}
      onMouseOut={(e) => {
        if (frame !== timeFrame) {
          e.currentTarget.style.backgroundColor = '#e7e7e7';
        }
      }}
    >
      {frame.charAt(0).toUpperCase() + frame.slice(1)}
    </button>
  ));

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', backgroundColor: '#f8f8f8' }}>
      <h2 style={{ textAlign: 'center', color: '#2c3e50' }}>Leaderboard</h2>
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '20px' }}>
        {toggleButtons}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

        {leaderboardData.map((data, index) => (
          <div key={index} style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            width: '80%', 
            backgroundColor: '#ffffff', 
            padding: '10px',
            borderRadius: '8px',
            marginTop: '10px',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
          }}>
            <div style={{ fontWeight: 'bold', color: '#34495e' }}>
              #{data.rank} - {data.username}
            </div>
            <div style={{ color: '#7f8c8d' }}>
              {timeFrame === 'day' ? `Day Performance: ${data.dayPerformance}%` : `Performance: ${data.performance}%`}
            </div>
            <div>
              {data.badges.map((badge, index) => (
                <span key={index} style={{ marginLeft: '5px', fontSize: '18px' }}>{badge}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LeaderboardPage;
