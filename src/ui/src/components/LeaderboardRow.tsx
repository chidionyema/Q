// components/LeaderboardRow.tsx
interface LeaderboardRowProps {
    rank: number;
    username: string;
    performance: number;
    dayPerformance: number;
    badges: string[];
  }
  
  const LeaderboardRow: React.FC<LeaderboardRowProps> = ({ rank, username, performance, dayPerformance, badges }) => {
    return (
      <div className="leaderboard-row">
        <div className="rank">{rank}</div>
        <div className="username">{username}</div>
        <div className="performance">{performance}%</div>
        <div className="day-performance">{dayPerformance}%</div>
        <div className="badges">{badges.map((badge, index) => <img key={index} src={badge} alt="badge" />)}</div>
      </div>
    );
  };
  
  export default LeaderboardRow;
  