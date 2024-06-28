import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import matplotlib.pyplot as plt

# 1. Load and prepare data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['ds'] = pd.to_datetime(df['ds'])  # Ensure date column is datetime
    return df

# 2. Create and fit the model
def create_and_fit_model(df, additional_regressors=None):
    model = Prophet()
    
    # Add additional regressors if provided
    if additional_regressors:
        for regressor in additional_regressors:
            model.add_regressor(regressor)
    
    model.fit(df)
    return model

# 3. Make future dataframe
def make_future_dataframe(model, periods, freq='D'):
    return model.make_future_dataframe(periods=periods, freq=freq)

# 4. Make predictions
def make_predictions(model, future_df):
    return model.predict(future_df)

# 5. Visualize results
def visualize_results(model, forecast):
    # Plot forecast
    fig1 = model.plot(forecast)
    plt.title('Forecast')
    plt.show()
    
    # Plot components
    fig2 = model.plot_components(forecast)
    plt.title('Forecast Components')
    plt.show()

# 6. Evaluate model
def evaluate_model(forecast, actual):
    # Calculate metrics (e.g., MAPE)
    mape = np.mean(np.abs((actual - forecast) / actual)) * 100
    return mape

# 7. Main workflow
def prophet_workflow(file_path, forecast_periods=365, additional_regressors=None):
    # Load data
    df = load_data(file_path)
    
    # Create and fit model
    model = create_and_fit_model(df, additional_regressors)
    
    # Make future dataframe
    future_df = make_future_dataframe(model, forecast_periods)
    
    # Make predictions
    forecast = make_predictions(model, future_df)
    
    # Visualize results
    visualize_results(model, forecast)
    
    # Evaluate model (if actual data is available)
    if 'y' in df.columns:
        mape = evaluate_model(forecast['yhat'][:len(df)], df['y'])
        print(f"MAPE: {mape:.2f}%")
    
    return model, forecast

# Example usage
if __name__ == "__main__":
    file_path = "your_time_series_data.csv"
    model, forecast = prophet_workflow(file_path, forecast_periods=365)