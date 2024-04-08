import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Step 1: Load the dataset
# Assuming you have downloaded the Pima Indians Diabetes Database and it's saved as 'diabetes.csv'.
data = pd.read_csv('app/diabetes_ai/diabetes.csv')

# Step 2: Prepare the data
X = data.drop('Outcome', axis=1)  # Features
y = data['Outcome']  # Target variable (0 - non-diabetic, 1 - diabetic)

# Step 3: Preprocess the data (scaling)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Create the Neural Network model
model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(X_scaled.shape[1],)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Step 5: Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Step 6: Train the model
model.fit(X_scaled, y, epochs=100, batch_size=32, verbose=0)  # Setting verbose to 0

# Function to make prediction for user input
def predict_diabetes(input_data):
    # Preprocess user input
    user_input = np.array([list(input_data.values())])
    user_input_scaled = scaler.transform(user_input)
    # Make prediction
    prediction = model.predict(user_input_scaled)
    # Convert prediction to percentage
    prediction_percentage = prediction[0][0] * 100
    return prediction_percentage
