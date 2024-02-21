# Example of using the predict function in another Python file

from predict import predict

# Data from HealthConnect API
data = {
    'Age': 19,
    'SBP': 126,
    'DBP': 74,
    'PP': 52,
    'Pulse': 92,
    'Blood_saturation': 100,
    'Temp': 37.3,
    'RMSSD': 13.92,
    'Gender': 1  # M->1, F->0
}

# Prediction
y_pred = predict(data)

print("예측된 VA:", y_pred)
