import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from xgboost import XGBClassifier, XGBRegressor

# 1. Load and prepare data
def load_data(file_path):
    data = pd.read_csv(file_path)
    X = data.drop('target_column', axis=1)
    y = data['target_column']
    return X, y

# 2. Split data
def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# 3. Initialize model
def init_model(task='classification', **kwargs):
    if task == 'classification':
        return XGBClassifier(**kwargs)
    elif task == 'regression':
        return XGBRegressor(**kwargs)
    else:
        raise ValueError("Task must be 'classification' or 'regression'")

# 4. Train model
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

# 5. Make predictions
def make_predictions(model, X_test):
    return model.predict(X_test)

# 6. Evaluate model
def evaluate_model(y_true, y_pred, task='classification'):
    if task == 'classification':
        return accuracy_score(y_true, y_pred)
    elif task == 'regression':
        return mean_squared_error(y_true, y_pred, squared=False)
    else:
        raise ValueError("Task must be 'classification' or 'regression'")

# 7. Main workflow
def xgboost_workflow(file_path, task='classification'):
    # Load data
    X, y = load_data(file_path)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Initialize model
    model = init_model(task=task, random_state=42)
    
    # Train model
    trained_model = train_model(model, X_train, y_train)
    
    # Make predictions
    predictions = make_predictions(trained_model, X_test)
    
    # Evaluate model
    performance = evaluate_model(y_test, predictions, task=task)
    
    print(f"Model performance: {performance}")
    
    return trained_model, performance

# Example usage
if __name__ == "__main__":
    file_path = "your_data.csv"
    model, performance = xgboost_workflow(file_path, task='classification')