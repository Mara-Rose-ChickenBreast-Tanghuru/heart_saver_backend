from joblib import load
import lightgbm as lgb
import numpy as np
import pandas as pd


def predict(data):
    # Load model and scaler
    loaded_model = load('lgbm_model.joblib')
    scaler = load('standard_scaler.joblib')

    # Convert input data to a DataFrame
    X_test = pd.DataFrame(data, index=[0])

    # Age, PP, Temp, RMSSD log scaling
    X_test_log = X_test.copy()
    for col in ['Age', 'PP', 'Temp', 'RMSSD']:
        X_test_log[col] = np.log(X_test_log[col] + 1)

    # Standard scaling
    numeric_columns = X_test_log.columns.drop(['Gender'])
    X_test_ss = scaler.transform(X_test_log[numeric_columns])
    X_test_ss = pd.DataFrame(X_test_ss, columns=numeric_columns, index=X_test.index)
    X_test_ss['Gender'] = X_test['Gender'].values

    # VA prediction
    y_pred = loaded_model.predict(X_test_ss)
    
    return y_pred[0]
