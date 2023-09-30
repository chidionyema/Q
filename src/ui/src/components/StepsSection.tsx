import React from 'react';
import Link from 'next/link';

const StepsSection: React.FC = () => {
    return (
        <section className="steps-section">
            <div className="container">
                <ul className="steps-list">
                    <li className="step">Train</li>
                    <li className="step">Test</li>
                    <li className="step">Predict</li>
                    <li className="step">Evaluate</li>
                    <li className="step">Simulate</li>
                    <li className="step">Paper Trade</li>
                    <li className="step">Leaderboard</li>
                </ul>
            </div>

            <style jsx>{`
                .steps-section {
                    background-color: #f9f9f9;
                    padding: 2em 0;
                    text-align: center;
                }

                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                }

                .steps-list {
                    list-style: none;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0;
                }

                .step {
                    background-color: #fff;
                    border-radius: 20px;
                    padding: 10px 20px;
                    font-size: 1em;
                    color: #555;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    transition: background-color 0.3s, transform 0.3s;
                }

                .step:hover {
                    background-color: #007bff;
                    color: #fff;
                    transform: scale(1.05);
                }
            `}</style>
        </section>
    );
};

export default StepsSection;
