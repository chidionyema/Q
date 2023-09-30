const MODEL_CLASSES_EXTENDED = [
    {
        id: 1,
        code: "CNN",
        name: "Convolutional Neural Network (CNN)",
        requirements: {
            dataType: ["image", "grid-like"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["GeneticAlgorithm"],
            ensembles: []
        },
        commonApplications: ["image classification", "object detection"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "low",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 2,
        code: "RNN",
        name: "Recurrent Neural Network (RNN)",
        requirements: {
            dataType: ["sequential", "time-series", "natural language"],
            datasetSize: ["medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["Adam", "RMSprop"],
        preferredEnsembles: ["Stacking"],
        incompatibilities: {
            optimizers: ["SGD"],
            ensembles: []
        },
        commonApplications: ["sequence prediction", "language modeling"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 3,
        code: "LinearSVM",
        name: "Linear Support Vector Machine (LinearSVM)",
        requirements: {
            dataType: ["tabular", "text"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Liblinear"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["Adam"],
            ensembles: []
        },
        commonApplications: ["classification", "text analysis"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 4,
        code: "PCA",
        name: "Principal Component Analysis (PCA)",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["dimensionality reduction", "data visualization"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "low",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 5,
        code: "DecisionTree",
        name: "Decision Tree",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging", "Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 6,
        code: "LogisticRegression",
        name: "Logistic Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 7,
        code: "RandomForest",
        name: "Random Forest",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 8,
        code: "LinearRegression",
        name: "Linear Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 9,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 10,
        code: "GradientBoosting",
        name: "Gradient Boosting",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 11,
        code: "PCA",
        name: "Principal Component Analysis (PCA)",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["dimensionality reduction", "data visualization"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "low",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 12,
        code: "LogisticRegression",
        name: "Logistic Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 13,
        code: "DecisionTree",
        name: "Decision Tree",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging", "Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 14,
        code: "LinearRegression",
        name: "Linear Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 15,
        code: "RandomForest",
        name: "Random Forest",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 16,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 17,
        code: "GradientBoosting",
        name: "Gradient Boosting",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 18,
        code: "SVM",
        name: "Support Vector Machine (SVM)",
        requirements: {
            dataType: ["tabular", "image"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Libsvm"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["Adam", "RMSprop"],
            ensembles: []
        },
        commonApplications: ["classification", "image classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 19,
        code: "BayesianNetworks",
        name: "Bayesian Networks",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["probabilistic reasoning", "causal inference"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 20,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 21,
        code: "",
        name: "Long Short-Term Memory ()",
        requirements: {
            dataType: ["sequential", "time-series", "natural language"],
            datasetSize: ["medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["Adam", "RMSprop"],
        preferredEnsembles: ["Stacking"],
        incompatibilities: {
            optimizers: ["SGD"],
            ensembles: []
        },
        commonApplications: ["sequence prediction", "language modeling"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 22,
        code: "NaiveBayes",
        name: "Naive Bayes",
        requirements: {
            dataType: ["tabular", "text"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "text classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 23,
        code: "DBSCAN",
        name: "Density-Based Spatial Clustering of Applications with Noise (DBSCAN)",
        requirements: {
            dataType: ["tabular", "geospatial"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["spatial clustering", "anomaly detection"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 24,
        code: "ARIMA",
        name: "Autoregressive Integrated Moving Average (ARIMA)",
        requirements: {
            dataType: ["time-series"],
            datasetSize: ["small", "medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["time series forecasting"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 25,
        code: "CNN",
        name: "Convolutional Neural Network (CNN)",
        requirements: {
            dataType: ["image", "grid-like"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["GeneticAlgorithm"],
            ensembles: []
        },
        commonApplications: ["image classification", "object detection"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "low",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 26,
        code: "RNN",
        name: "Recurrent Neural Network (RNN)",
        requirements: {
            dataType: ["sequential", "time-series", "natural language"],
            datasetSize: ["medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["Adam", "RMSprop"],
        preferredEnsembles: ["Stacking"],
        incompatibilities: {
            optimizers: ["SGD"],
            ensembles: []
        },
        commonApplications: ["sequence prediction", "language modeling"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 27,
        code: "LinearSVM",
        name: "Linear Support Vector Machine (LinearSVM)",
        requirements: {
            dataType: ["tabular", "image"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Libsvm"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["Adam", "RMSprop"],
            ensembles: []
        },
        commonApplications: ["classification", "image classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 28,
        code: "PCA",
        name: "Principal Component Analysis (PCA)",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["dimensionality reduction", "data visualization"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "low",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 29,
        code: "DecisionTree",
        name: "Decision Tree",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging", "Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 30,
        code: "LinearRegression",
        name: "Linear Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 31,
        code: "RandomForest",
        name: "Random Forest",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 32,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 33,
        code: "GradientBoosting",
        name: "Gradient Boosting",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 34,
        code: "PCA",
        name: "Principal Component Analysis (PCA)",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["dimensionality reduction", "data visualization"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "low",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 35,
        code: "LogisticRegression",
        name: "Logistic Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 36,
        code: "DecisionTree",
        name: "Decision Tree",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging", "Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 37,
        code: "LinearRegression",
        name: "Linear Regression",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["None"],
            ensembles: ["Bagging", "Boosting"]
        },
        commonApplications: ["regression"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 38,
        code: "RandomForest",
        name: "Random Forest",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 39,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 40,
        code: "GradientBoosting",
        name: "Gradient Boosting",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 41,
        code: "SVM",
        name: "Support Vector Machine (SVM)",
        requirements: {
            dataType: ["tabular", "image"],
            datasetSize: ["small", "medium"],
            sequential: false
        },
        preferredOptimizers: ["SGD", "Libsvm"],
        preferredEnsembles: ["Bagging"],
        incompatibilities: {
            optimizers: ["Adam", "RMSprop"],
            ensembles: []
        },
        commonApplications: ["classification", "image classification"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 42,
        code: "BayesianNetworks",
        name: "Bayesian Networks",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["probabilistic reasoning", "causal inference"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 43,
        code: "K-Means",
        name: "K-Means Clustering",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 44,
        code: "",
        name: "Long Short-Term Memory ()",
        requirements: {
            dataType: ["sequential", "time-series", "natural language"],
            datasetSize: ["medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["Adam", "RMSprop"],
        preferredEnsembles: ["Stacking"],
        incompatibilities: {
            optimizers: ["SGD"],
            ensembles: []
        },
        commonApplications: ["sequence prediction", "language modeling"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: true
    },
    {
        id: 45,
        code: "NaiveBayes",
        name: "Naive Bayes",
        requirements: {
            dataType: ["tabular", "text"],
            datasetSize: ["small", "medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["text classification", "spam detection"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "high",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 46,
        code: "DBSCAN",
        name: "Density-Based Spatial Clustering of Applications with Noise (DBSCAN)",
        requirements: {
            dataType: ["tabular", "spatial"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["spatial clustering"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    },
    {
        id: 47,
        code: "ARIMA",
        name: "Autoregressive Integrated Moving Average (ARIMA)",
        requirements: {
            dataType: ["sequential", "time-series"],
            datasetSize: ["medium", "large"],
            sequential: true
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["None"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["time series forecasting"],
        trainingTime: "medium",
        memoryUsage: "medium",
        scalability: false,
        interpretability: "medium",
        sensitivity: "high",
        parallelization: false,
        onlineLearning: false,
        nonStationarityHandling: true,
        regularization: false
    },
    {
        id: 48,
        code: "XGBoost",
        name: "Extreme Gradient Boosting (XGBoost)",
        requirements: {
            dataType: ["tabular"],
            datasetSize: ["medium", "large"],
            sequential: false
        },
        preferredOptimizers: ["None"],
        preferredEnsembles: ["Boosting"],
        incompatibilities: {
            optimizers: ["SGD", "Adam", "RMSprop", "Liblinear"],
            ensembles: []
        },
        commonApplications: ["classification", "regression"],
        trainingTime: "long",
        memoryUsage: "high",
        scalability: true,
        interpretability: "medium",
        sensitivity: "medium",
        parallelization: true,
        onlineLearning: false,
        nonStationarityHandling: false,
        regularization: false
    }
    ];
    


// You now have the detailed data for all 48 models in the list.
