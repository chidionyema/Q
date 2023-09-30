

const ENSEMBLE_STRATEGY_DICTIONARY = {
    1: {
        code: "MAJ_VOTING",
        name: "Majority Voting"
    },
    2: {
        code: "STACKING",
        name: "Stacking"
    },
    3: {
        code: "BAGGING",
        name: "Bagging (Bootstrap Aggregating)"
    },
    4: {
        code: "RAND_FOREST",
        name: "Random Forests"
    },
    5: {
        code: "BOOSTING",
        name: "Boosting"
    },
    6: {
        code: "ADABOOST",
        name: "Adaptive Boosting (AdaBoost)"
    },
    7: {
        code: "GRAD_BOOST",
        name: "Gradient Boosting"
    },
    8: {
        code: "XGBOOST",
        name: "XGBoost (Extreme Gradient Boosting)"
    },
    9: {
        code: "LIGHTGBM",
        name: "LightGBM"
    },
    10: {
        code: "CATBOOST",
        name: "CatBoost"
    },
    11: {
        code: "VOTING_CLASSIFIER",
        name: "Voting Classifier"
    },
    12: {
        code: "BLENDING",
        name: "Blending"
    },
    13: {
        code: "ISOL_FOREST",
        name: "Isolation Forest"
    },
    14: {
        code: "RUSBOOST",
        name: "RUSBoost"
    }
};



const ENSEMBLE_STRATEGIES = [
    {
        id: 1,
        code: "MAJ_VOTING",
        name: "Majority Voting",
        description: {
            text: "Each model in the ensemble votes for a class, and the class with the majority of votes becomes the predicted class.",
            analogies: {
                cooking: "Chefs voting on the primary ingredient for a dish.",
                carBuilding: "Engineers voting on the best material for a car's exterior.",
                petTraining: "Trainers voting on the most effective command for obedience."
            }
        },
        strengths: {
            points: ["reducing overfitting", "leveraging multiple model outputs"],
            analogies: {
                cooking: "Multiple chefs fine-tuning a dish for optimal flavor.",
                carBuilding: "Incorporating feedback from multiple test drivers to improve car design.",
                petTraining: "Several trainers ensuring a pet's behavior is well-rounded."
            }
        },
        weaknesses: {
            points: ["limited diversity if models are similar", "bias if majority models are biased"],
            analogies: {
                cooking: "If all chefs come from the same culinary school, the dish might lack diversity.",
                carBuilding: "Using car parts from only one supplier might lead to limited functionality.",
                petTraining: "If all trainers rely on the same technique, the pet's training might be one-dimensional."
            }
        },
        bestUsedFor: {
            text: "When individual model variances need to be balanced.",
            analogies: {
                cooking: "Creating a well-balanced dish from different chef's contributions.",
                carBuilding: "Producing a car that captures the strengths of various design inputs.",
                petTraining: "Achieving comprehensive pet training by blending techniques."
            }
        }
    },
    {
        id: 2,
        code: "STACKING",
        name: "Stacking",
        description: {
            text: "Multiple models make predictions, and a meta-model combines these predictions for the final output.",
            analogies: {
                cooking: "Chefs making individual dishes that are combined into a tasting menu.",
                carBuilding: "Engineers designing parts separately, then integrating for the final car model.",
                petTraining: "Different trainers teaching tricks, with a head trainer integrating for a routine."
            }
        },
        strengths: {
            points: ["model diversity", "higher predictive power"],
            analogies: {
                cooking: "A tasting menu offering diverse flavors and experiences.",
                carBuilding: "A car design benefiting from specialized engineering expertise.",
                petTraining: "A pet showcasing a range of skills in a cohesive performance."
            }
        },
        weaknesses: {
            points: ["potential overfitting", "model selection complexity"],
            analogies: {
                cooking: "A tasting menu being overwhelming if not curated well.",
                carBuilding: "Complexity in ensuring all car parts fit seamlessly.",
                petTraining: "A pet being confused if training methods clash."
            }
        },
        bestUsedFor: {
            text: "Combining diverse model types for improved predictions.",
            analogies: {
                cooking: "Bringing together different culinary styles for a fusion dish.",
                carBuilding: "Blending classic design with modern technology.",
                petTraining: "A showcase event featuring diverse pet talents."
            }
        }
    },
    {
        id: 3,
        code: "BAGGING",
        name: "Bagging (Bootstrap Aggregating)",
        description: {
            text: "Involves training multiple models on different subsets of the dataset and aggregating their predictions.",
            analogies: {
                cooking: "Chefs creating variations of a dish and blending the best elements.",
                carBuilding: "Test driving cars on different terrains and combining feedback.",
                petTraining: "Trainers working with a pet in different environments for comprehensive learning."
            }
        },
        strengths: {
            points: ["reducing variance", "preventing overfitting"],
            analogies: {
                cooking: "Multiple taste tests ensuring a dish's consistency.",
                carBuilding: "Feedback from diverse test drives enhancing overall design.",
                petTraining: "Consistent behavior of a pet in various situations."
            }
        },
        weaknesses: {
            points: ["bias remains if present in original data", "requires multiple model training"],
            analogies: {
                cooking: "If an ingredient is off, all variations of the dish might be affected.",
                carBuilding: "If a foundational design flaw exists, multiple iterations might not help.",
                petTraining: "If a pet has a foundational behavior issue, different environments might not address it."
            }
        },
        bestUsedFor: {
            text: "When individual models have high variance.",
            analogies: {
                cooking: "Ensuring consistency in a dish served at a large banquet.",
                carBuilding: "Designing a car model that needs to cater to diverse markets.",
                petTraining: "Training a pet that will be exposed to various scenarios."
            }
        }
    },
    {
        id: 5,
        code: "BOOSTING",
        name: "Boosting",
        description: {
            text: "An iterative technique that adjusts the weight of an observation based on the last classification. If an observation was classified incorrectly, it tries to increase the weight of this observation.",
            analogies: {
                cooking: "Adjusting the recipe based on feedback from tasters.",
                carBuilding: "Refining parts of a car based on testing results.",
                petTraining: "Emphasizing training where the pet is weak until it learns."
            }
        },
        strengths: {
            points: ["increased accuracy", "converts weak learners to strong learners"],
            analogies: {
                cooking: "Iterative taste tests ensuring dish perfection.",
                carBuilding: "Continuous improvement based on rigorous testing.",
                petTraining: "Ensuring a pet is well-rounded by addressing its weaknesses."
            }
        },
        weaknesses: {
            points: ["can overfit", "sensitive to noisy data and outliers"],
            analogies: {
                cooking: "Over-refining a dish can make it lose its original essence.",
                carBuilding: "Making too many tweaks can drift away from the car's design philosophy.",
                petTraining: "Overtraining in one aspect might cause the pet to lose proficiency in others."
            }
        },
        bestUsedFor: {
            text: "When the ensemble of weak learners underfits the data.",
            analogies: {
                cooking: "Improving a bland or under-seasoned dish.",
                carBuilding: "Enhancing a basic car model with additional features.",
                petTraining: "Intensive training for a pet that's slow to learn certain commands."
            }
        }
    },
    {
        id: 6,
        code: "ADABOOST",
        name: "Adaptive Boosting (AdaBoost)",
        description: {
            text: "Focuses on classifying misclassified data points by adjusting weights. Each new model compensates for its predecessor's shortcomings.",
            analogies: {
                cooking: "Iteratively improving a dish by focusing on ingredients that were underrepresented in earlier versions.",
                carBuilding: "Adjusting car parts that caused issues in earlier test drives.",
                petTraining: "Prioritizing commands the pet hasn't mastered in successive training sessions."
            }
        },
        strengths: {
            points: ["fast", "less prone to overfitting"],
            analogies: {
                cooking: "Quick iterations on a dish based on immediate feedback.",
                carBuilding: "Rapid prototyping for quicker car design iterations.",
                petTraining: "Quick training sessions focusing on pet's immediate needs."
            }
        },
        weaknesses: {
            points: ["sensitive to noisy data", "performance depends on data and weak learner choice"],
            analogies: {
                cooking: "Overadjusting to a single critic's feedback might not suit all.",
                carBuilding: "Relying heavily on one kind of test can miss other important issues.",
                petTraining: "Focusing too much on one trainer's methods can neglect other important skills."
            }
        },
        bestUsedFor: {
            text: "Binary classification problems.",
            analogies: {
                cooking: "Deciding between two primary flavors for a dish.",
                carBuilding: "Choosing between two primary designs.",
                petTraining: "Deciding if a pet should be indoor or outdoor trained."
            }
        }
    },
    {
        id: 7,
        code: "GRAD_BOOST",
        name: "Gradient Boosting",
        description: {
            text: "Builds an additive model in a forward stage-wise manner, introducing models to correct the errors of existing ensemble.",
            analogies: {
                cooking: "Perfecting a dish by sequentially adding ingredients.",
                carBuilding: "Enhancing a car's design by building upon existing models.",
                petTraining: "Sequentially teaching a pet more advanced tricks."
            }
        },
        strengths: {
            points: ["handles missing data", "good for heterogeneous features"],
            analogies: {
                cooking: "Adapting a recipe even when some ingredients are unavailable.",
                carBuilding: "Modifying car design to handle various terrains.",
                petTraining: "Training pets for varied tasks even with distractions."
            }
        },
        weaknesses: {
            points: ["needs careful tuning", "can be slower due to sequential building"],
            analogies: {
                cooking: "Requires meticulous taste tests for perfection.",
                carBuilding: "Refinement stages might delay production.",
                petTraining: "Step-by-step training can be time-consuming."
            }
        },
        bestUsedFor: {
            text: "Regression and classification problems when speed is not primary.",
            analogies: {
                cooking: "Creating dishes that require careful layering of flavors.",
                carBuilding: "Designing luxury cars where time isn't the main constraint.",
                petTraining: "Training for advanced pet shows or competitions."
            }
        }
    },
    {
        id: 8,
        code: "XGBOOST",
        name: "XGBoost (Extreme Gradient Boosting)",
        description: {
            text: "An optimized distributed gradient boosting library designed to be efficient and flexible.",
            analogies: {
                cooking: "Using advanced kitchen equipment to perfect a dish in record time.",
                carBuilding: "Implementing cutting-edge technology for faster and efficient car production.",
                petTraining: "Utilizing advanced techniques to quickly train pets for complex tasks."
            }
        },
        strengths: {
            points: ["scalability", "parallel processing capabilities"],
            analogies: {
                cooking: "Preparing multiple dishes simultaneously without compromising quality.",
                carBuilding: "Producing multiple car parts at once to speed up assembly.",
                petTraining: "Training a pet on multiple commands at once efficiently."
            }
        },
        weaknesses: {
            points: ["more parameters to tune", "can overfit if not careful"],
            analogies: {
                cooking: "Too many kitchen gadgets can complicate a dish if not used correctly.",
                carBuilding: "Too much automation in car design can miss human touch nuances.",
                petTraining: "Using too many training tools at once can confuse a pet."
            }
        },
        bestUsedFor: {
            text: "Large datasets where performance and speed are crucial.",
            analogies: {
                cooking: "Serving a large banquet where dishes need to be prepared for many guests quickly.",
                carBuilding: "Mass-producing a popular car model efficiently.",
                petTraining: "Preparing pets for a large-scale show with limited preparation time."
            }
        }
    },
    {
        id: 9,
        code: "LIGHTGBM",
        name: "LightGBM",
        description: {
            text: "A gradient boosting framework that uses tree-based algorithms and follows leaf-wise approach.",
            analogies: {
                cooking: "Optimizing ingredient use for maximum flavor with minimum waste.",
                carBuilding: "Designing cars that deliver maximum efficiency with fewer resources.",
                petTraining: "Using efficient methods to get the best behavior from pets in shorter sessions."
            }
        },
        strengths: {
            points: ["faster training speed", "lower memory usage"],
            analogies: {
                cooking: "Using techniques that cut down cooking time without compromising taste.",
                carBuilding: "Innovations that allow faster car assembly with less energy.",
                petTraining: "Quick yet effective training sessions that pets find engaging."
            }
        },
        weaknesses: {
            points: ["can be sensitive to overfitting", "less interpretable due to leaf-wise approach"],
            analogies: {
                cooking: "Speed cooking might miss subtle flavors.",
                carBuilding: "Too much optimization can make it hard to retrofit or modify cars.",
                petTraining: "Too much focus on quick tricks might miss foundational behaviors."
            }
        },
        bestUsedFor: {
            text: "Large datasets focusing on efficiency and scalability.",
            analogies: {
                cooking: "High-demand restaurant kitchens that need to serve many dishes quickly.",
                carBuilding: "Factories producing large volumes of a particular car model.",
                petTraining: "Training academies that need to prepare many pets for shows or competitions."
            }
        }
    },
    {
        id: 10,
        code: "CATBOOST",
        name: "CatBoost",
        description: {
            text: "A gradient boosting library that can naturally handle categorical features without the need for manual encoding.",
            analogies: {
                cooking: "Preparing dishes that blend multiple cuisines without needing adjustments.",
                carBuilding: "Integrating car parts from various suppliers without additional modifications.",
                petTraining: "Training diverse breeds with a universal technique."
            }
        },
        strengths: {
            points: ["handles categorical variables", "robust to overfitting"],
            analogies: {
                cooking: "Adapting recipes to available ingredients without compromising taste.",
                carBuilding: "Ensuring a car model is versatile regardless of the parts' origin.",
                petTraining: "Ensuring consistent training outcomes regardless of a pet's background."
            }
        },
        weaknesses: {
            points: ["slower training times compared to other boosting algorithms", "less community support compared to older algorithms"],
            analogies: {
                cooking: "A dish that takes longer to prepare but is worth the wait.",
                carBuilding: "A newer car model that mechanics are less familiar with.",
                petTraining: "A newer training method that isn't as widely adopted among trainers."
            }
        },
        bestUsedFor: {
            text: "Datasets with many categorical features.",
            analogies: {
                cooking: "A recipe with diverse ingredients from various cuisines.",
                carBuilding: "A car design that merges various international designs.",
                petTraining: "Training sessions tailored to pets with varied backgrounds."
            }
        }
    },
    {
        id: 11,
        code: "VOTING_CLASSIFIER",
        name: "Voting Classifier",
        description: {
            text: "An ensemble technique that takes the predictions from multiple models and uses votes to produce a final output.",
            analogies: {
                cooking: "Chefs collaborating to finalize a dish based on individual expertise.",
                carBuilding: "Engineers collectively deciding on the best design approach for a feature.",
                petTraining: "Trainers deciding on the best method after individual assessments."
            }
        },
        strengths: {
            points: ["combines different machine learning classifiers", "improves generalization"],
            analogies: {
                cooking: "Merging culinary techniques for a unique dish.",
                carBuilding: "Integrating diverse engineering solutions for a better car model.",
                petTraining: "Combining various training techniques for a well-rounded pet behavior."
            }
        },
        weaknesses: {
            points: ["limited diversity if models are too similar", "performance is capped at the best-performing model"],
            analogies: {
                cooking: "If all chefs have the same style, the dish might lack uniqueness.",
                carBuilding: "If all engineers have the same background, innovations might be limited.",
                petTraining: "If all trainers follow the same method, the pet might not learn new tricks."
            }
        },
        bestUsedFor: {
            text: "When you have multiple algorithms and you want to capitalize on their strengths.",
            analogies: {
                cooking: "Creating a fusion dish with inputs from specialists of each cuisine.",
                carBuilding: "A car model that blends various engineering breakthroughs.",
                petTraining: "An advanced training regime that draws from various methods."
            }
        }
    },
    {
        id: 12,
        code: "BLENDING",
        name: "Blending",
        description: {
            text: "Similar to stacking but uses a holdout set to make predictions, which are then used as input for final predictions.",
            analogies: {
                cooking: "Blending ingredients based on taste tests to finalize a dish.",
                carBuilding: "Merging designs based on test drives to finalize a car model.",
                petTraining: "Combining training techniques based on observed pet responses."
            }
        },
        strengths: {
            points: ["simpler than stacking", "less risk of data leakage compared to stacking"],
            analogies: {
                cooking: "Direct tasting leads to quicker adjustments for the dish.",
                carBuilding: "Immediate feedback from test drives speeds up design refinement.",
                petTraining: "Quick feedback from pets allows trainers to adjust techniques."
            }
        },
        weaknesses: {
            points: ["relies on a single holdout set", "not as robust as stacking in some scenarios"],
            analogies: {
                cooking: "Relying too much on feedback from one tasting might not suit everyone.",
                carBuilding: "Depending too much on a single test drive might miss nuances.",
                petTraining: "Over-reliance on a single feedback session might not capture all pet needs."
            }
        },
        bestUsedFor: {
            text: "When a simpler alternative to stacking is preferred, with reduced complexity.",
            analogies: {
                cooking: "Perfecting a homestyle dish without the intricacies of gourmet recipes.",
                carBuilding: "Opting for a classic car design without too many modern complexities.",
                petTraining: "When basic obedience and behavior are the focus over complex tricks."
            }
        }
    },
    {
        id: 13,
        code: "ISOL_FOREST",
        name: "Isolation Forest",
        description: {
            text: "An algorithm to detect outliers by partitioning data with random cuts, anomalies get isolated with fewer cuts.",
            analogies: {
                cooking: "Spotting the ingredient that doesn't belong in a recipe.",
                carBuilding: "Identifying a car part that doesn't fit the overall design.",
                petTraining: "Noticing a behavior that's out of the norm for a pet."
            }
        },
        strengths: {
            points: ["efficient with large datasets", "can handle high-dimensional data"],
            analogies: {
                cooking: "Quickly spotting a misplaced ingredient even in complex recipes.",
                carBuilding: "Efficient quality checks in large production lines.",
                petTraining: "Quickly addressing any odd behavior in pets before it becomes a habit."
            }
        },
        weaknesses: {
            points: ["random forest nature might introduce some randomness", "may not perform as well with very small datasets"],
            analogies: {
                cooking: "Might occasionally miss a subtle off-flavor in a dish.",
                carBuilding: "Might not spot defects in bespoke, limited edition models.",
                petTraining: "Might not capture unique quirks in rare breeds."
            }
        },
        bestUsedFor: {
            text: "Anomaly detection especially in larger datasets.",
            analogies: {
                cooking: "Ensuring consistency in dishes served to a large crowd.",
                carBuilding: "Quality control in mass-produced car models.",
                petTraining: "Ensuring general behavior norms in a large group of pets."
            }
        }
    },
    {
        id: 14,
        code: "RUSBOOST",
        name: "RUSBoost",
        description: {
            text: "Combines boosting with random undersampling to tackle class imbalance problems.",
            analogies: {
                cooking: "Adjusting the quantity of an overpowering ingredient to balance a dish.",
                carBuilding: "Balancing the weight in various car parts for optimal performance.",
                petTraining: "Balancing training focus between a pet's strengths and weaknesses."
            }
        },
        strengths: {
            points: ["deals with imbalanced datasets", "combines random undersampling with boosting"],
            analogies: {
                cooking: "Achieving a harmonious flavor profile in a dish.",
                carBuilding: "Ensuring all parts of a car work in harmony.",
                petTraining: "Ensuring a pet is well-rounded and not over-trained in one area."
            }
        },
        weaknesses: {
            points: ["undersampling can lead to information loss", "overfitting if not tuned properly"],
            analogies: {
                cooking: "Leaving out an ingredient can alter the intended taste of a dish.",
                carBuilding: "Removing a car feature can compromise its overall functionality.",
                petTraining: "Neglecting a training area can lead to incomplete pet behavior."
            }
        },
        bestUsedFor: {
            text: "Addressing class imbalances in datasets.",
            analogies: {
                cooking: "Perfecting recipes that started off imbalanced.",
                carBuilding: "Optimizing designs that initially had weight imbalances.",
                petTraining: "Balancing a pet's training regimen to address all areas equally."
            }
        }
    }
];
