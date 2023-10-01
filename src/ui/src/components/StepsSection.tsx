import React from 'react';
import Link from 'next/link';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrain, faVial, faLightbulb, faStar, faPlayCircle, faTrophy } from '@fortawesome/free-solid-svg-icons';

const steps = [
    { name: 'Train', icon: faTrain },
    { name: 'Test', icon: faVial },
    { name: 'Predict', icon: faLightbulb },
    { name: 'Evaluate', icon: faStar },
    { name: 'Simulate', icon: faPlayCircle },
    { name: 'Leaderboard', icon: faTrophy }
];

const StepsSection: React.FC = () => (
    <section className="steps-section">
        <div className="container">
            <ul className="steps-list">
                {steps.map((step, idx) => (
                    <li key={idx} className="step-item">
                        <Link href={`#${step.name.toLowerCase()}`}>
                            <span className="step-link">
                                <FontAwesomeIcon icon={step.icon} className="step-icon" />
                                <span className="step-name">{step.name}</span>
                            </span>
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
        <style jsx>{`
            .steps-section {
                background-color: #f9f9f9;
                padding: 2em 0;
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

            .step-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                position: relative;
                margin-right: 40px;
            }

            .step-item:last-child {
                margin-right: 0;
            }

            .step-item:not(:last-child)::after {
                content: '';
                position: absolute;
                right: -20px;
                top: 50%;
                width: 10px;
                height: 10px;
                background: #333;
                clip-path: polygon(100% 50%, 0 0, 0 100%);
                transform: translateY(-50%);
            }

            .step-item:not(:last-child)::before {
                content: '';
                position: absolute;
                right: -30px;
                top: 50%;
                width: 20px;
                height: 2px;
                background: #333;
                transform: translateY(-50%);
            }

            .step-link {
                display: flex;
                flex-direction: column;
                align-items: center;
                background: linear-gradient(145deg, #e6e6e6, #ffffff);
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 6px 6px 12px #b8b8b8, -6px -6px 12px #ffffff;
                transition: transform 0.3s;
                text-decoration: none;
                color: #333;
            }

            .step-link:hover {
                transform: translateY(-5px);
            }

            .step-icon {
                font-size: 2.5em;
                color: #333;
                margin-bottom: 0.5rem;
            }

            .step-name {
                font-weight: 500;
            }

            @media (max-width: 1024px) {
                .step-item {
                    margin-right: 20px;
                }

                .step-icon {
                    font-size: 2em;
                }
            }

            @media (max-width: 768px) {
                .step-icon {
                    font-size: 1.8em;
                }

                .step-name {
                    font-size: 0.9em;
                }
            }
        `}</style>
    </section>
);

export default StepsSection;
