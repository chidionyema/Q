const MODEL_CLASSES = [
    {
        name: "Random Forest",
        strengths: ["robustness to noise", "capability to handle diverse data types"],
        bestUsedFor: "datasets with high dimensionality and missing values",
        analogies: {
            Pets: {
                description: "Multiple trainers teaching a pet different tricks.",
                reason: "Each tree (trainer) in the forest focuses on a subset of the data or features (tricks)."
            },
            Cars: {
                description: "A team of mechanics each specializing in a specific car part.",
                reason: "Each tree (mechanic) focuses on understanding and fixing a particular subset of the car's issues."
            },
            Cooking: {
                description: "Cooking with multiple chefs each focused on a particular dish in a multi-course meal.",
                reason: "Each tree (chef) focuses on perfecting a particular dish, leading to a well-rounded meal."
            }
        },
        compatibleWith: {
            "Grid Search": "Given its defined hyperparameters range, Grid Search is suitable for Random Forest.",
            "Majority Voting": "Ensemble strategy that can be used with Random Forest.",
            "Bagging": "Ensemble strategy that can be used with Random Forest.",
            "Stacking": "Ensemble strategy that can be used with Random Forest.",
            "Boosting + Grid Search": "Boosting combined with Grid Search can enhance Random Forest's performance.",
            "Blending + Grid Search": "Blending combined with Grid Search can enhance Random Forest's performance.",
            "Bootstrapped Ensembles + Grid Search": "Bootstrapped Ensembles combined with Grid Search can enhance Random Forest's performance.",
            "Gradient Boosted Trees + Grid Search": "Gradient Boosted Trees combined with Grid Search can enhance Random Forest's performance.",
            "Random Forest of Neural Networks + Grid Search": "Random Forest of Neural Networks combined with Grid Search can enhance Random Forest's performance.",
            "Time Series Averaging + Grid Search": "Time Series Averaging combined with Grid Search can enhance Random Forest's performance.",
            "Dynamic Weighted Ensemble + Grid Search": "Dynamic Weighted Ensemble combined with Grid Search can enhance Random Forest's performance."
        }
    },
    {
        name: "Gradient Boosting",
        strengths: ["boosting", "handles complex relationships in data"],
        bestUsedFor: "classification and regression problems with structured data",
        analogies: {
            Pets: {
                description: "Training a pet with gradual improvements and corrections.",
                reason: "Gradient Boosting corrects the errors of previous models in a gradual manner."
            },
            Cars: {
                description: "Repairing a car part by part with each part compensating for the flaws of the previous one.",
                reason: "Each boosting iteration corrects the errors of the previous iteration."
            },
            Cooking: {
                description: "Cooking a dish by adjusting the seasoning at each step based on previous taste tests.",
                reason: "Gradient Boosting adjusts the model at each stage based on previous errors."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Gradient Boosting.",
            "Random Search": "Optimization technique that can be used with Gradient Boosting.",
            "Majority Voting": "Ensemble strategy that can be used with Gradient Boosting.",
            "Bagging": "Ensemble strategy that can be used with Gradient Boosting.",
            "Stacking": "Ensemble strategy that can be used with Gradient Boosting.",
            "Boosting + Grid Search": "Boosting combined with Grid Search can enhance Gradient Boosting's performance.",
            "Blending + Grid Search": "Blending combined with Grid Search can enhance Gradient Boosting's performance.",
            "Bootstrapped Ensembles + Grid Search": "Bootstrapped Ensembles combined with Grid Search can enhance Gradient Boosting's performance.",
            "Gradient Boosted Trees + Grid Search": "Gradient Boosted Trees combined with Grid Search can enhance Gradient Boosting's performance.",
            "Random Forest of Neural Networks + Grid Search": "Random Forest of Neural Networks combined with Grid Search can enhance Gradient Boosting's performance.",
            "Time Series Averaging + Grid Search": "Time Series Averaging combined with Grid Search can enhance Gradient Boosting's performance.",
            "Dynamic Weighted Ensemble + Grid Search": "Dynamic Weighted Ensemble combined with Grid Search can enhance Gradient Boosting's performance."
        }
    },
    {
        name: "LSTM",
        strengths: ["sequential data modeling", "memory of past observations"],
        bestUsedFor: "time series forecasting, natural language processing",
        analogies: {
            Pets: {
                description: "Teaching a pet based on its previous behaviors and responses.",
                reason: "LSTM models sequential data and remembers past observations to make predictions."
            },
            Cars: {
                description: "Diagnosing a car's issues by considering its historical performance data.",
                reason: "LSTM can model time series data and consider past observations for better predictions."
            },
            Cooking: {
                description: "Cooking a dish using a recipe that specifies the order of adding ingredients.",
                reason: "LSTM models sequences and remembers the sequence of events or data points."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with LSTM.",
            "Random Search": "Optimization technique that can be used with LSTM.",
            "Stacking": "Ensemble strategy that can be used with LSTM.",
            "Blending": "Ensemble strategy that can be used with LSTM.",
            "Bootstrapped Ensembles": "Ensemble strategy that can be used with LSTM.",
            "Boosting": "Ensemble strategy that can be used with LSTM.",
            "Random Forest": "Ensemble strategy that can be used with LSTM.",
            "Gradient Boosting": "Ensemble strategy that can be used with LSTM.",
            "Time Series Averaging": "Ensemble strategy that can be used with LSTM.",
            "Dynamic Weighted Ensemble": "Ensemble strategy that can be used with LSTM."
        }
    },
    {
        name: "ARIMA",
        strengths: ["time series forecasting", "simplicity and interpretability"],
        bestUsedFor: "univariate time series data with a clear trend and seasonality",
        analogies: {
            Pets: {
                description: "Using historical pet behavior patterns to predict future behavior.",
                reason: "ARIMA analyzes time series data and makes predictions based on past observations."
            },
            Cars: {
                description: "Predicting future car part failures based on historical maintenance records.",
                reason: "ARIMA is suitable for time series forecasting with clear patterns."
            },
            Cooking: {
                description: "Estimating future demand for ingredients based on past recipe orders.",
                reason: "ARIMA models time series data with clear trends and seasonality."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with ARIMA.",
            "Random Search": "Optimization technique that can be used with ARIMA.",
            "Time Series Averaging": "Ensemble strategy that can be used with ARIMA."
        }
    },
    {
        name: "Reinforcement Learning",
        strengths: ["sequential decision making", "interaction with environment"],
        bestUsedFor: "problems where an agent learns to make decisions by interacting with an environment",
        analogies: {
            Pets: {
                description: "Training a pet to perform tasks through rewards and punishments.",
                reason: "Reinforcement Learning involves an agent learning optimal actions through interaction with an environment."
            },
            Cars: {
                description: "Teaching a self-driving car to navigate roads based on rewards for safe driving.",
                reason: "Reinforcement Learning is used for training agents to make decisions in dynamic environments."
            },
            Cooking: {
                description: "Optimizing a cooking process by tasting and adjusting ingredients based on feedback.",
                reason: "Reinforcement Learning involves agents learning through trial and error in various tasks."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Reinforcement Learning.",
            "Random Search": "Optimization technique that can be used with Reinforcement Learning.",
            "Dynamic Weighted Ensemble": "Ensemble strategy that can be used with Reinforcement Learning."
        }
    },
    {
        name: "Prophet",
        strengths: ["time series forecasting", "holiday effects modeling"],
        bestUsedFor: "forecasting time series data with holidays and special events",
        analogies: {
            Pets: {
                description: "Predicting pet adoption rates, considering holiday adoption trends.",
                reason: "Prophet models time series data with holiday effects and special events."
            },
            Cars: {
                description: "Forecasting car sales, accounting for holiday sales promotions.",
                reason: "Prophet is suitable for time series data affected by holidays and events."
            },
            Cooking: {
                description: "Predicting restaurant customer counts, considering holiday reservations.",
                reason: "Prophet models time series data with holiday-related variations."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Prophet.",
            "Random Search": "Optimization technique that can be used with Prophet.",
            "Time Series Averaging": "Ensemble strategy that can be used with Prophet."
        }
    },
    {
        name: "Gaussian Processes",
        strengths: ["probabilistic modeling", "uncertainty quantification"],
        bestUsedFor: "regression and uncertainty estimation in small to medium-sized datasets",
        analogies: {
            Pets: {
                description: "Predicting pet lifespans with confidence intervals based on health data.",
                reason: "Gaussian Processes provide probabilistic regression and uncertainty estimates."
            },
            Cars: {
                description: "Estimating car prices with uncertainty levels based on historical data.",
                reason: "Gaussian Processes are useful for regression tasks with uncertainty quantification."
            },
            Cooking: {
                description: "Predicting cooking time with confidence intervals based on recipe data.",
                reason: "Gaussian Processes offer probabilistic modeling for regression tasks."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Gaussian Processes.",
            "Random Search": "Optimization technique that can be used with Gaussian Processes."
        }
    },
    {
        name: "Deep Learning",
        strengths: ["complex feature learning", "state-of-the-art performance"],
        bestUsedFor: "tasks with large datasets and complex patterns, such as image and speech recognition",
        analogies: {
            Pets: {
                description: "Training a pet to recognize complex commands with deep learning techniques.",
                reason: "Deep Learning excels in learning intricate patterns in data."
            },
            Cars: {
                description: "Teaching a car to identify various objects on the road using deep neural networks.",
                reason: "Deep Learning is suitable for tasks requiring complex feature learning."
            },
            Cooking: {
                description: "Developing a deep learning model to classify and recommend recipes based on images.",
                reason: "Deep Learning can handle tasks involving large datasets and intricate patterns."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Deep Learning.",
            "Random Search": "Optimization technique that can be used with Deep Learning.",
            "Stacking": "Ensemble strategy that can be used with Deep Learning.",
            "Blending": "Ensemble strategy that can be used with Deep Learning.",
            "Bootstrapped Ensembles": "Ensemble strategy that can be used with Deep Learning.",
            "Boosting": "Ensemble strategy that can be used with Deep Learning.",
            "Random Forest": "Ensemble strategy that can be used with Deep Learning.",
            "Gradient Boosting": "Ensemble strategy that can be used with Deep Learning.",
            "Time Series Averaging": "Ensemble strategy that can be used with Deep Learning.",
            "Dynamic Weighted Ensemble": "Ensemble strategy that can be used with Deep Learning."
        }
    },
    {
        name: "KNN",
        strengths: ["instance-based learning", "simple and intuitive"],
        bestUsedFor: "classification and regression tasks with small to medium-sized datasets",
        analogies: {
            Pets: {
                description: "Classifying pets based on similarity to known pet categories.",
                reason: "KNN is an instance-based learning method that classifies based on similarity."
            },
            Cars: {
                description: "Predicting car prices by comparing them to similar historical sales.",
                reason: "KNN uses similarity measures for regression and classification tasks."
            },
            Cooking: {
                description: "Categorizing recipes by comparing ingredients to known recipe categories.",
                reason: "KNN is intuitive and simple for classification tasks."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with KNN."
        }
    },
    {
        name: "SVM",
        strengths: ["effective in high-dimensional spaces", "works well with clear margin of separation"],
        bestUsedFor: "classification tasks with well-defined class boundaries",
        analogies: {
            Pets: {
                description: "Classifying pets into categories with distinct features.",
                reason: "SVM is effective when classes have clear boundaries."
            },
            Cars: {
                description: "Detecting defects in car parts with distinct defect characteristics.",
                reason: "SVM works well when there's a clear margin of separation between classes."
            },
            Cooking: {
                description: "Categorizing recipes based on clear ingredient distinctions.",
                reason: "SVM is suitable for classification tasks with well-defined features."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with SVM."
        }
    },
    {
        name: "Decision Trees",
        strengths: ["interpretable", "easy to visualize"],
        bestUsedFor: "classification and regression tasks where interpretability is important",
        analogies: {
            Pets: {
                description: "Creating a decision tree to classify pets based on simple, interpretable criteria.",
                reason: "Decision Trees are known for their interpretability and ease of visualization."
            },
            Cars: {
                description: "Using a decision tree to diagnose car issues based on observable symptoms.",
                reason: "Decision Trees are suitable for tasks where transparency is crucial."
            },
            Cooking: {
                description: "Building a decision tree to recommend recipes based on user preferences.",
                reason: "Decision Trees provide interpretable recommendations."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with Decision Trees."
        }
    },
    {
        name: "XGBoost",
        strengths: ["highly efficient", "handles missing data"],
        bestUsedFor: "classification and regression tasks, especially in structured data",
        analogies: {
            Pets: {
                description: "Boosting the performance of pet classification models through careful adjustments.",
                reason: "XGBoost is known for its efficient boosting algorithms."
            },
            Cars: {
                description: "Boosting the accuracy of car price prediction models through iterative improvements.",
                reason: "XGBoost is effective for boosting in regression and classification tasks."
            },
            Cooking: {
                description: "Improving recipe recommendation models through iterative enhancements.",
                reason: "XGBoost is well-suited for boosting-based ensemble methods."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with XGBoost."
        }
    },
    {
        name: "CatBoost",
        strengths: ["handles categorical features well", "robust to overfitting"],
        bestUsedFor: "classification and regression tasks with categorical data",
        analogies: {
            Pets: {
                description: "Teaching a pet to perform tricks by considering the pet's unique characteristics.",
                reason: "CatBoost is designed to handle categorical features effectively."
            },
            Cars: {
                description: "Predicting car prices by considering the unique features of each car model.",
                reason: "CatBoost is robust to overfitting and can handle categorical data."
            },
            Cooking: {
                description: "Customizing recipe recommendations based on individual cooking preferences.",
                reason: "CatBoost is suitable for tasks with categorical data and individual variations."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with CatBoost."
        }
    },
    {
        name: "LightGBM",
        strengths: ["fast and efficient", "handles large datasets"],
        bestUsedFor: "classification and regression tasks with large datasets",
        analogies: {
            Pets: {
                description: "Training pet models quickly and efficiently to handle a large number of pet categories.",
                reason: "LightGBM is known for its speed and efficiency, making it suitable for large datasets."
            },
            Cars: {
                description: "Predicting car prices for a large inventory of cars in a short time.",
                reason: "LightGBM is efficient and can handle large datasets effectively."
            },
            Cooking: {
                description: "Providing recipe recommendations for a vast database of recipes without delays.",
                reason: "LightGBM is fast and suitable for tasks with extensive data."
            }
        },
        compatibleWith: {
            "Grid Search": "Optimization technique that can be used with LightGBM."
        }
    },
    // ... Similarly structured data for other models
];

const OPTIMIZERS = [
    {
        name: "Grid Search",
        strengths: ["systematic search", "guaranteed to find the best parameter if it exists in the grid"],
        bestUsedFor: "models with fewer hyperparameters and when computational resources are abundant",
        analogies: {
            Pets: {
                description: "Training a pet by trying every possible command combination to get a trick right.",
                reason: "Grid Search exhaustively tries out predefined hyperparameters to find the best combination."
            },
            Cars: {
                description: "Testing every single part of a car to find out the faulty component.",
                reason: "Grid Search examines all provided parameters systematically."
            },
            Cooking: {
                description: "Testing every spice combination to perfect a dish.",
                reason: "Grid Search explores every ingredient combination to find the best taste."
            }
        },
        compatibleWith: {
            "Random Forest": "Optimization technique that can be used with Random Forest.",
            "Gradient Boosting": "Optimization technique that can be used with Gradient Boosting.",
            "LSTM": "Optimization technique that can be used with LSTM.",
            "ARIMA": "Optimization technique that can be used with ARIMA.",
            "Reinforcement Learning": "Optimization technique that can be used with Reinforcement Learning.",
            "Prophet": "Optimization technique that can be used with Prophet.",
            "Gaussian Processes": "Optimization technique that can be used with Gaussian Processes.",
            "Deep Learning": "Optimization technique that can be used with Deep Learning.",
            "KNN": "Optimization technique that can be used with KNN.",
            "SVM": "Optimization technique that can be used with SVM.",
            "Decision Trees": "Optimization technique that can be used with Decision Trees.",
            "XGBoost": "Optimization technique that can be used with XGBoost.",
            "CatBoost": "Optimization technique that can be used with CatBoost.",
            "LightGBM": "Optimization technique that can be used with LightGBM."
        }
    },
    {
        name: "Random Search",
        strengths: ["random exploration of hyperparameter space", "can find good solutions faster than Grid Search"],
        bestUsedFor: "models with a large hyperparameter space and limited computational resources",
        analogies: {
            Pets: {
                description: "Training a pet by trying random command combinations to discover effective tricks.",
                reason: "Random Search explores hyperparameters randomly, finding good solutions faster."
            },
            Cars: {
                description: "Experimenting with various car part adjustments in random order to identify issues.",
                reason: "Random Search explores hyperparameters in a more randomized manner."
            },
            Cooking: {
                description: "Experimenting with spice combinations in a random sequence to discover new flavors.",
                reason: "Random Search explores hyperparameters in a less systematic way."
            }
        },
        compatibleWith: {
            "Random Forest": "Optimization technique that can be used with Random Forest.",
            "Gradient Boosting": "Optimization technique that can be used with Gradient Boosting.",
            "LSTM": "Optimization technique that can be used with LSTM.",
            "ARIMA": "Optimization technique that can be used with ARIMA.",
            "Reinforcement Learning": "Optimization technique that can be used with Reinforcement Learning.",
            "Prophet": "Optimization technique that can be used with Prophet.",
            "Gaussian Processes": "Optimization technique that can be used with Gaussian Processes.",
            "Deep Learning": "Optimization technique that can be used with Deep Learning.",
            "KNN": "Optimization technique that can be used with KNN.",
            "SVM": "Optimization technique that can be used with SVM.",
            "Decision Trees": "Optimization technique that can be used with Decision Trees.",
            "XGBoost": "Optimization technique that can be used with XGBoost.",
            "CatBoost": "Optimization technique that can be used with CatBoost.",
            "LightGBM": "Optimization technique that can be used with LightGBM."
        }
    },
    {
        name: "Majority Voting",
        strengths: ["reducing overfitting", "leveraging multiple model outputs"],
        bestUsedFor: "scenarios where individual model variances need to be averaged out",
        analogies: {
            Pets: {
                description: "If multiple trainers agree on the best method to teach a trick, then that method is chosen.",
                reason: "Predictions from multiple models are taken, and the most common prediction is chosen."
            },
            Cars: {
                description: "If multiple mechanics agree on a diagnosis, that is the one adopted.",
                reason: "Ensures reliability in model predictions by aggregating multiple opinions."
            },
            Cooking: {
                description: "If most chefs agree on a specific recipe, it's adopted for the restaurant menu.",
                reason: "By consolidating different chefs' inputs, a well-accepted dish is prepared."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "ARIMA": "Ensemble strategy that can be used with ARIMA.",
            "Reinforcement Learning": "Ensemble strategy that can be used with Reinforcement Learning.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "KNN": "Ensemble strategy that can be used with KNN.",
            "SVM": "Ensemble strategy that can be used with SVM.",
            "Decision Trees": "Ensemble strategy that can be used with Decision Trees.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Bagging",
        strengths: ["reduces variance", "improves model stability"],
        bestUsedFor: "complex models that are prone to overfitting",
        analogies: {
            Pets: {
                description: "Using multiple pet trainers to collectively improve a pet's overall behavior.",
                reason: "Bagging reduces model variance by averaging predictions from multiple models."
            },
            Cars: {
                description: "Seeking input from multiple mechanics to diagnose and repair a car.",
                reason: "Improves model stability and reduces overfitting by combining multiple model outputs."
            },
            Cooking: {
                description: "Collaborating with multiple chefs to create a diverse and balanced menu.",
                reason: "Bagging results in a more stable and reliable model by combining multiple predictions."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "ARIMA": "Ensemble strategy that can be used with ARIMA.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "KNN": "Ensemble strategy that can be used with KNN.",
            "SVM": "Ensemble strategy that can be used with SVM.",
            "Decision Trees": "Ensemble strategy that can be used with Decision Trees.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Stacking",
        strengths: ["model combination flexibility", "improves prediction accuracy"],
        bestUsedFor: "leveraging diverse models to make accurate predictions",
        analogies: {
            Pets: {
                description: "Combining the expertise of multiple pet trainers to teach advanced tricks.",
                reason: "Stacking allows flexible combination of diverse models for improved accuracy."
            },
            Cars: {
                description: "Integrating insights from multiple car mechanics to make a comprehensive diagnosis.",
                reason: "Stacking leverages the strengths of various models to enhance predictions."
            },
            Cooking: {
                description: "Creating a gourmet dish by using the expertise of multiple chefs with different specialties.",
                reason: "Stacking combines diverse models to achieve more accurate and robust predictions."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "ARIMA": "Ensemble strategy that can be used with ARIMA.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "KNN": "Ensemble strategy that can be used with KNN.",
            "SVM": "Ensemble strategy that can be used with SVM.",
            "Decision Trees": "Ensemble strategy that can be used with Decision Trees.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Boosting",
        strengths: ["combats bias", "improves model performance"],
        bestUsedFor: "boosting the performance of weak learners",
        analogies: {
            Pets: {
                description: "Boosting the confidence of pet trainers in their ability to teach complex tricks.",
                reason: "Boosting enhances model performance, especially when dealing with weak learners."
            },
            Cars: {
                description: "Boosting the diagnostic skills of car mechanics for challenging cases.",
                reason: "Boosting is effective in improving the accuracy of models with low performance."
            },
            Cooking: {
                description: "Boosting the culinary skills of chefs to create exceptional dishes.",
                reason: "Boosting elevates the performance of individual models to produce better predictions."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Blending",
        strengths: ["simple yet effective", "reduces overfitting"],
        bestUsedFor: "combining multiple models to improve generalization",
        analogies: {
            Pets: {
                description: "Blending the training techniques of multiple pet trainers to enhance pet skills.",
                reason: "Blending is a straightforward method to combine models effectively."
            },
            Cars: {
                description: "Blending the diagnostic expertise of multiple mechanics to improve diagnosis accuracy.",
                reason: "Blending helps reduce overfitting and improve model generalization."
            },
            Cooking: {
                description: "Blending the culinary knowledge of different chefs to create unique and appealing dishes.",
                reason: "Blending combines diverse models for better predictions."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Bootstrapped Ensembles",
        strengths: ["bootstrap sampling", "diverse base learners"],
        bestUsedFor: "creating ensembles with diverse models",
        analogies: {
            Pets: {
                description: "Training multiple pets using different training methods and selecting the best.",
                reason: "Bootstrapped Ensembles leverage bootstrap sampling to create diverse subsets of data."
            },
            Cars: {
                description: "Diagnosing cars with various combinations of diagnostic tools to identify issues.",
                reason: "Creates diversity in base learners by using different subsets of data for training."
            },
            Cooking: {
                description: "Preparing dishes by experimenting with different combinations of ingredients.",
                reason: "Utilizes diverse subsets of data to create varied base learners in the ensemble."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Gradient Boosted Trees",
        strengths: ["boosting technique", "sequential model improvement"],
        bestUsedFor: "improving model performance through boosting",
        analogies: {
            Pets: {
                description: "Training a pet to perform complex tricks by breaking them down into simpler steps.",
                reason: "Gradient Boosted Trees iteratively improve model performance by correcting errors."
            },
            Cars: {
                description: "Diagnosing car issues step by step, improving accuracy with each step.",
                reason: "Gradient Boosted Trees sequentially enhance model accuracy through boosting."
            },
            Cooking: {
                description: "Developing a recipe step by step, refining it with each iteration.",
                reason: "Gradient Boosted Trees progressively improve model predictions through boosting."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    },
    {
        name: "Random Forest of Neural Networks",
        strengths: ["combining neural networks", "ensemble of deep learning models"],
        bestUsedFor: "leveraging multiple neural networks for improved predictions",
        analogies: {
            Pets: {
                description: "Training pets using various trainers, each specializing in different tricks.",
                reason: "Random Forest of Neural Networks combines diverse neural networks for better predictions."
            },
            Cars: {
                description: "Diagnosing car issues using multiple diagnostic tools, each focusing on a specific aspect.",
                reason: "Utilizes a collection of neural networks, each specialized in different features or patterns."
            },
            Cooking: {
                description: "Creating a diverse menu by collaborating with chefs, each with their own culinary expertise.",
                reason: "Leverages multiple neural networks with unique capabilities to improve predictions."
            }
        },
        compatibleWith: {
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning."
        }
    },
    {
        name: "Time Series Averaging",
        strengths: ["ensemble technique for time series data", "reduces noise and improves predictions"],
        bestUsedFor: "improving time series forecasts by combining multiple models",
        analogies: {
            Pets: {
                description: "Predicting pet behaviors by averaging predictions from multiple pet trainers.",
                reason: "Time Series Averaging reduces noise in time series predictions."
            },
            Cars: {
                description: "Forecasting car sales by averaging predictions from different forecasting methods.",
                reason: "Improves the stability and accuracy of time series predictions."
            },
            Cooking: {
                description: "Estimating restaurant customer counts by averaging predictions from various models.",
                reason: "Time Series Averaging provides more reliable predictions for time series data."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "ARIMA": "Ensemble strategy that can be used with ARIMA.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes."
        }
    },
    {
        name: "Dynamic Weighted Ensemble",
        strengths: ["adaptive weighting of models", "improved accuracy with dynamic adjustments"],
        bestUsedFor: "optimizing ensemble performance by dynamically adjusting model weights",
        analogies: {
            Pets: {
                description: "Training pets by adjusting training methods based on the pet's progress and capabilities.",
                reason: "Dynamic Weighted Ensemble adapts model weights based on their performance."
            },
            Cars: {
                description: "Diagnosing car issues by giving more weight to diagnostic tools with higher accuracy.",
                reason: "Optimizes ensemble accuracy by dynamically adjusting model weights."
            },
            Cooking: {
                description: "Creating dishes by adjusting the contribution of each chef based on their expertise.",
                reason: "Dynamic Weighted Ensemble improves predictions by dynamically adjusting model weights."
            }
        },
        compatibleWith: {
            "Random Forest": "Ensemble strategy that can be used with Random Forest.",
            "Gradient Boosting": "Ensemble strategy that can be used with Gradient Boosting.",
            "LSTM": "Ensemble strategy that can be used with LSTM.",
            "ARIMA": "Ensemble strategy that can be used with ARIMA.",
            "Reinforcement Learning": "Ensemble strategy that can be used with Reinforcement Learning.",
            "Prophet": "Ensemble strategy that can be used with Prophet.",
            "Gaussian Processes": "Ensemble strategy that can be used with Gaussian Processes.",
            "Deep Learning": "Ensemble strategy that can be used with Deep Learning.",
            "KNN": "Ensemble strategy that can be used with KNN.",
            "SVM": "Ensemble strategy that can be used with SVM.",
            "Decision Trees": "Ensemble strategy that can be used with Decision Trees.",
            "XGBoost": "Ensemble strategy that can be used with XGBoost.",
            "CatBoost": "Ensemble strategy that can be used with CatBoost.",
            "LightGBM": "Ensemble strategy that can be used with LightGBM."
        }
    }
];
