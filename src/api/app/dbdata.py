
from app import db, app
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import  MetaData, Table

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)  # It's good to ensure this is securely hashed if you use it
    name = db.Column(db.String(120), nullable=True)
    provider = db.Column(db.String(50), nullable=True)
    provider_id = db.Column(db.String(120), unique=True, nullable=True)
    access_token = db.Column(db.String(500), nullable=True)
    refresh_token = db.Column(db.String(500), nullable=True)
    first_login = db.Column(db.Boolean, default=True, nullable=True)
    is_active = db.Column(db.Boolean, default=False) 

    def __repr__(self):
            return f"<User {self.email}>"    


class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, token, user_id, expiration_time):
        self.token = token
        self.user_id = user_id
        self.expiration_time = expiration_time

class TaskResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    task_id = db.Column(db.String, unique=True, nullable=False)
    result = db.Column(db.JSON, nullable=False)

def create_all():
    with app.app_context():
        db.create_all()


class ModelCategory(db.Model):
    __tablename__ = 'model_categories'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), unique=True, nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    models = db.relationship('MLModel', backref='category', lazy=True)

class MLModel(db.Model):
    __tablename__ = 'ml_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.String(512), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('model_categories.id'), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)

class EnsembleStrategy(db.Model):
    __tablename__ = 'ensemble_strategies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(512), nullable=True)
    code = db.Column(db.String(3), unique=True, nullable=False)

class ModelOptimizer(db.Model):
    __tablename__ = 'model_optimizers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(512), nullable=True)
    code = db.Column(db.String(3), unique=True, nullable=False)

def generate_unique_code(name):
    # Convert a name to a 3-character base36 string
    ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_value = abs(hash(name))  # Make sure it's non-negative
    code = hash_value % (36 ** 3)  # Limit to 3 base36 characters

    result = ''
    while code:
        code, rem = divmod(code, 36)
        result = ALPHABET[rem] + result

    return result.rjust(3, '0')

import hashlib


from sqlalchemy import create_engine, MetaData, Table

def get_existing_codes(table_name):
    """
    Retrieve existing codes from a specific table in the database.
    """
    with app.app_context():
        metadata = MetaData()
        metadata.reflect(bind=db.engine, only=[table_name])  # Reflect only the table we're interested in

        table = metadata.tables[table_name]

        # Query the 'code' column
        codes = db.session.query(table.c.code).all()

        # Convert the result to a set and return
        return {code[0] for code in codes}



def generate_unique_code(name, table_name):
    """
    Generate a unique 3-character code based on hashing the name.
    Check against existing codes in the given table.
    If the generated code already exists, modify the name slightly and try again.
    """
    existing_codes = get_existing_codes(table_name)
    base_name = name
    attempt = 0

    while True:
        # Generate a hash of the name
        name_hash = hashlib.sha256(name.encode()).hexdigest()
        code = name_hash[:3].upper()  # Use the first 3 characters of the hash

        if code not in existing_codes:
            return code

        # If code exists, modify the name and try again
        attempt += 1
        name = base_name + str(attempt)



def populate_model_categories():
    categories = [
        "Regression",  "Classification"  "Clustering", "Dimensionality Reduction", "Time Series",
        # ... other categories
    ]
    with app.app_context():
        for category_name in categories:
            existing_category = ModelCategory.query.filter_by(category=category_name).first()
            if not existing_category:
                new_category = ModelCategory(category=category_name)
                new_category.code = generate_unique_code(new_category.category, "model_categories")
                db.session.add(new_category)
                db.session.flush()  # To generate the new category's ID          
                db.session.commit()  # Commit after each category to ensure the code is set before the next flush.



def populate_ml_models():
    models = [
        {"name": "RandomForestRegressor", "category": "Regression", "description": "Random Forest algorithm for regression tasks."},
        {"name": "PrincipalComponentAnalysis", "category": "Dimensionality Reduction", "description": "Linear dimensionality reduction using Singular Value Decomposition."},
        {"name": "KMeans", "category": "Clustering", "description": "Partitioning data into k distinct clusters based on mean."},
        {"name": "SupportVectorRegressor", "category": "Regression", "description": "Support Vector Machines for regression tasks."},
        {"name": "LinearRegression", "category": "Regression", "description": "Ordinary least squares linear regression."},
        {"name": "KNeighborsRegressor", "category": "Regression", "description": "Regression based on k-nearest neighbors."},
        {"name": "DecisionTreeRegressor", "category": "Regression", "description": "Decision tree-based regression model."},
        {"name": "AdaBoostRegressor", "category": "Regression", "description": "AdaBoost regressor is a meta-estimator that begins by fitting a regressor on the original dataset and then fits additional copies of the regressor on the same dataset."},
        {"name": "GradientBoostingRegressor", "category": "Regression", "description": "Boosting technique which builds an additive model in a forward stage-wise fashion."},
        {"name": "RidgeRegression", "category": "Regression", "description": "Linear regression with L2 regularization."},
        {"name": "LassoRegression", "category": "Regression", "description": "Linear regression with L1 regularization."},
        {"name": "ElasticNetRegression", "category": "Regression", "description": "Linear regression with combined L1 and L2 regularizers."},
        {"name": "BayesianRidgeRegression", "category": "Regression", "description": "Bayesian ridge regression."},
        {"name": "ARDRegression", "category": "Regression", "description": "Automatic Relevance Determination Regression."},
        {"name": "SGDRegressor", "category": "Regression", "description": "Stochastic Gradient Descent regressor."},
        {"name": "PassiveAggressiveRegressor", "category": "Regression", "description": "Passive Aggressive algorithm for regression tasks."},
        {"name": "HuberRegressor", "category": "Regression", "description": "Linear regression model that is robust to outliers."},
        {"name": "TheilSenRegressor", "category": "Regression", "description": "Theil-Sen Estimator: robust multivariate regression model."},
        {"name": "RANSACRegressor", "category": "Regression", "description": "RANdom SAmple Consensus (RANSAC) algorithm for robust regression."},
        {"name": "OrthogonalMatchingPursuit", "category": "Regression", "description": "Orthogonal Matching Pursuit model (OMP) for approximating the fit of a linear model."},
        {"name": "Lars", "category": "Regression", "description": "Least Angle Regression model."},
        {"name": "LassoLars", "category": "Regression", "description": "Lasso model implemented using the LARS algorithm."},
        {"name": "TweedieRegressor", "category": "Regression", "description": "Generalized Linear Model with a Tweedie distribution."},
        {"name": "PoissonRegressor", "category": "Regression", "description": "Generalized Linear Model with a Poisson distribution."},
        {"name": "GammaRegressor", "category": "Regression", "description": "Generalized Linear Model with a Gamma distribution."},
        {"name": "LogisticRegressionClassifier", "category": "Classification", "description": "Logistic regression classifier suitable for binary classification tasks."},
        {"name": "GaussianNaiveBayes", "category": "Classification", "description": "Naive Bayes classifier for Gaussian-distributed data."},
        {"name": "RandomForestClassifier", "category": "Classification", "description": "Random Forest algorithm for classification tasks."},
        {"name": "SupportVectorClassifier", "category": "Classification", "description": "Support Vector Machines for classification tasks."},
        {"name": "DecisionTreeClassifier", "category": "Classification", "description": "Decision tree-based classifier."},
        {"name": "AdaBoostClassifier", "category": "Classification", "description": "AdaBoost classifier is a meta-estimator that starts by fitting a base classifier and then fits additional copies of the classifier on the same dataset."},
        {"name": "GradientBoostingClassifier", "category": "Classification", "description": "Boosting technique for classification which builds an additive model in a forward stage-wise fashion."},
        {"name": "KMeansClustering", "category": "Clustering", "description": "Partitioning data into k distinct clusters based on mean."},
        {"name": "PCA", "category": "Dimensionality Reduction", "description": "Principal Component Analysis for linear dimensionality reduction."},
        {"name": "GaussianHMM", "category": "Probabilistic and Statistical Models", "description": "Hidden Markov Models with Gaussian emissions."},
        {"name": "ARIMA", "category": "Time Series", "description": "AutoRegressive Integrated Moving Average model for time series forecasting."},
        # Add more models here if necessary
    ]

    
    with app.app_context():
        for model_data in models:
            existing_model = MLModel.query.filter_by(name=model_data["name"]).first()
            category = ModelCategory.query.filter_by(category=model_data["category"]).first()
            if not existing_model and category:
                new_model = MLModel(name=model_data["name"], description=model_data["description"], category_id=category.id)
                new_model.code = generate_unique_code(new_model.name, "ml_models")
                db.session.add(new_model)
                db.session.flush()  # To generate the new model's ID
             
        db.session.commit()

def populate_ensemble_strategies():
    strategies = [
        {"name": "ThresholdVotingStrategy", "description": "Threshold-based ensemble strategy for binary classification."},
        {"name": "BordaCountStrategy", "description": "Borda Count-based ensemble strategy."},
        {"name": "SoftVotingStrategy", "description": "Soft Voting ensemble strategy for classification."},
        {"name": "MaxVotingStrategy", "description": "Max Voting ensemble strategy for classification."},
        {"name": "MinVotingStrategy", "description": "Min Voting ensemble strategy for classification."},
        {"name": "ProductStrategy", "description": "Product-based ensemble strategy for classification."},
        {"name": "RankAveragingStrategy", "description": "Rank Averaging ensemble strategy for classification."},
        {"name": "MajorityVoteStrategy", "description": "Majority Voting ensemble strategy for classification."},
        {"name": "AverageStrategy", "description": "Average ensemble strategy for continuous values."},
        {"name": "WeightedAverageStrategy", "description": "Weighted Average ensemble strategy for continuous values with weights."},
        {"name": "BaggingStrategy", "description": "Bagging ensemble strategy using scikit-learn's BaggingClassifier."},
        {"name": "RandomForestStrategy", "description": "Random Forest ensemble strategy using scikit-learn's RandomForestClassifier."},
        {"name": "AdaBoostStrategy", "description": "AdaBoost ensemble strategy using scikit-learn's AdaBoostClassifier."},
        {"name": "GradientBoostingStrategy", "description": "Gradient Boosting ensemble strategy using scikit-learn's GradientBoostingClassifier."},
        {"name": "XGBoostStrategy", "description": "XGBoost ensemble strategy using XGBoost's XGBClassifier."},
        {"name": "LightGBMStrategy", "description": "LightGBM ensemble strategy using LightGBM's LGBMClassifier."},
        # Add more strategies here if necessary
    ]

    with app.app_context():
        for strategy_data in strategies:
            existing_strategy = EnsembleStrategy.query.filter_by(name=strategy_data["name"]).first()
            if not existing_strategy:
                new_strategy = EnsembleStrategy(name=strategy_data["name"], description=strategy_data["description"])
                new_strategy.code = generate_unique_code(new_strategy.name, "ensemble_strategies")
                db.session.add(new_strategy)
                db.session.flush()  # To generate the new strategy's ID
                
        db.session.commit()



def populate_optimizers():
    optimizers = {
        "RandomSearch": "Random search optimization algorithm.",
        "BayesianOptimizer": "Bayesian optimization using Gaussian Processes.",
        "NelderMead": "The Nelder-Mead method (also downhill simplex method) for optimization.",
        "ParticleSwarm": "Particle Swarm Optimization (PSO).",
        "SimulatedAnnealing": "Simulated Annealing optimization algorithm.",
        "GridSearch": "Grid search optimization using scikit-learn's GridSearchCV.",
        "DifferentialEvolution": "Differential Evolution optimization algorithm.",
        "GeneticAlgorithm": "Genetic Algorithm optimization.",
        "AntColony": "Ant Colony Optimization (ACO).",
        "CMA_ES": "CMA-ES (Covariance Matrix Adaptation Evolution Strategy) optimization.",
        "DEAPGA": "Differential Evolution using DEAP library.",
        "OptunaCMAES": "Optuna optimization using CMA-ES sampler.",
        "GridSearchCV": "Grid Search optimization using scikit-learn's GridSearchCV.",
        "REINFORCE": "REINFORCE (Monte Carlo Policy Gradient) reinforcement learning optimizer.",
        "RLHyperparameter": "Reinforcement Learning-based Hyperparameter Optimization using Ray Tune.",
        "GeneticProgramming": "Genetic Programming-based optimizer.",
        "HillClimbing": "Hill Climbing-based optimizer.",
        # ... other optimizers
    }
    with app.app_context():
        for optimizer_name, description in optimizers.items():
            existing_optimizer = ModelOptimizer.query.filter_by(name=optimizer_name).first()
            if not existing_optimizer:
                new_optimizer = ModelOptimizer(name=optimizer_name, description=description)
                new_optimizer.code = generate_unique_code(new_optimizer.name, "model_optimizers")
                db.session.add(new_optimizer)
                db.session.flush()  
        db.session.commit()





with app.app_context():
    db.create_all()


# Run the functions
populate_model_categories()
populate_ml_models()
populate_optimizers()
populate_ensemble_strategies()