# -*- coding: utf-8 -*-
"""saparupuHW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12Du8ioajaT7MWplpcFEqPnWavHIPRYjA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ALS Implementation
def als(matrix, num_latent_factors, num_epochs, learning_rate, lambda_reg):
    N, M = matrix.shape
    P = np.random.rand(N, num_latent_factors)
    Q = np.random.rand(M, num_latent_factors)

    loss_values_als = []

    for epoch in range(num_epochs):
        for i in range(N):
            for j in range(M):
                if matrix.iloc[i, j] > 0:
                    eij = matrix.iloc[i, j] - np.dot(P[i, :], Q[j, :].T)
                    for k in range(num_latent_factors):
                        P[i, k] = P[i, k] + learning_rate * (2 * eij * Q[j, k] - lambda_reg * P[i, k])
                        Q[j, k] = Q[j, k] + learning_rate * (2 * eij * P[i, k] - lambda_reg * Q[j, k])

        # Calculate the reconstruction error
        reconstructed_matrix = np.dot(P, Q.T)
        loss = np.sum((matrix.values - reconstructed_matrix)**2)
        loss_values_als.append(loss)

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{num_epochs}, ALS Loss: {loss}")

    return P, Q, loss_values_als

# Load your training data
df_train = pd.read_csv('train.csv')
df_train.drop_duplicates(inplace=True)

# Pivot the table and fill NaN values with 0
user_movie_matrix_train = df_train.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Set hyperparameters for ALS training
num_latent_factors_als = 10
num_epochs_als = 50
learning_rate_als = 0.01
lambda_reg_als = 0.1

# Train ALS model and obtain user and item factors
user_factors_als, item_factors_als, loss_values_als = als(user_movie_matrix_train, num_latent_factors_als, num_epochs_als, learning_rate_als, lambda_reg_als)

# Display or plot ALS training loss
plt.plot(loss_values_als, label='ALS Loss', color='red')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Convergence of Loss Function (ALS)')
plt.legend()
plt.grid(True)
plt.show()

# Load test data
df_test = pd.read_csv('test.csv')

# Pivot the table and fill NaN values with 0
user_movie_matrix_test = df_test.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Make predictions for the test set
test_predictions_als = np.dot(user_factors_als, item_factors_als.T)

# Extract predictions for the test set
test_user_ids_als = df_test['user-id'].values
test_movie_ids_als = df_test['movie-id'].values
test_predictions_als = test_predictions_als[test_user_ids_als - 1, test_movie_ids_als - 1]  # Adjust for 0-based indexing

# Clip predictions to the valid range (0 to 5)
test_predictions_als = np.clip(test_predictions_als, a_min=0, a_max=5)

# Create a DataFrame with the test predictions
test_predictions_df_als = pd.DataFrame({'user-id': test_user_ids_als, 'movie-id': test_movie_ids_als, 'prediction': test_predictions_als})

# Save the predictions to a CSV file
test_predictions_df_als.to_csv('test_predictions_als.csv', index=False)

# Display or further analyze the predictions
print(test_predictions_df_als.head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Gradient Descent Implementation
def gradient_descent(matrix, num_latent_factors, num_epochs, learning_rate):
    N, M = matrix.shape
    P = np.random.rand(N, num_latent_factors)
    Q = np.random.rand(M, num_latent_factors)

    loss_values_gd = []

    for epoch in range(num_epochs):
        for i in range(N):
            for j in range(M):
                if matrix.iloc[i, j] > 0:
                    eij = matrix.iloc[i, j] - np.dot(P[i, :], Q[j, :].T)
                    for k in range(num_latent_factors):
                        P[i, k] = P[i, k] - learning_rate * (-2 * eij * Q[j, k])
                        Q[j, k] = Q[j, k] - learning_rate * (-2 * eij * P[i, k])

        # Calculate the reconstruction error
        reconstructed_matrix = np.dot(P, Q.T)
        loss = np.sum((matrix.values - reconstructed_matrix)**2)
        loss_values_gd.append(loss)

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{num_epochs}, GD Loss: {loss}")

    return P, Q, loss_values_gd

# Load your training data
df_train = pd.read_csv('train.csv')
df_train.drop_duplicates(inplace=True)

# Pivot the table and fill NaN values with 0
user_movie_matrix_train = df_train.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Set hyperparameters for GD training
num_latent_factors_gd = 10
num_epochs_gd = 50
learning_rate_gd = 0.01

# Train GD model and obtain user and item factors
user_factors_gd, item_factors_gd, loss_values_gd = gradient_descent(user_movie_matrix_train, num_latent_factors_gd, num_epochs_gd, learning_rate_gd)

# Display or plot GD training loss
plt.plot(loss_values_gd, label='GD Loss', color='blue')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Convergence of Loss Function (GD)')
plt.legend()
plt.grid(True)
plt.show()


# Load test data
df_test = pd.read_csv('test.csv')

# Pivot the table and fill NaN values with 0
user_movie_matrix_test = df_test.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Make predictions for the test set
test_predictions_gd = np.dot(user_factors_gd, item_factors_gd.T)

# Extract predictions for the test set
test_user_ids_gd = df_test['user-id'].values
test_movie_ids_gd = df_test['movie-id'].values
test_predictions_gd = test_predictions_gd[test_user_ids_gd - 1, test_movie_ids_gd - 1]  # Adjust for 0-based indexing

# Clip predictions to the valid range (0 to 5)
test_predictions_gd = np.clip(test_predictions_gd, a_min=0, a_max=5)

# Create a DataFrame with the test predictions
test_predictions_df_gd = pd.DataFrame({'user-id': test_user_ids_gd, 'movie-id': test_movie_ids_gd, 'prediction': test_predictions_gd})

# Save the predictions to a CSV file
test_predictions_df_gd.to_csv('test_predictions_gd.csv', index=False)

# Display or further analyze the predictions
print(test_predictions_df_gd.head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SGD Implementation with MSE Calculation
def stochastic_gradient_descent(matrix, num_latent_factors, num_epochs, learning_rate, lambda_reg):
    N, M = matrix.shape
    P = np.random.rand(N, num_latent_factors)
    Q = np.random.rand(M, num_latent_factors)

    mse_values_sgd = []

    for epoch in range(num_epochs):
        for i in range(N):
            for j in range(M):
                if matrix.iloc[i, j] > 0:
                    eij = matrix.iloc[i, j] - np.dot(P[i, :], Q[j, :].T)
                    for k in range(num_latent_factors):
                        P[i, k] = P[i, k] + learning_rate * (2 * eij * Q[j, k] - lambda_reg * P[i, k])
                        Q[j, k] = Q[j, k] + learning_rate * (2 * eij * P[i, k] - lambda_reg * Q[j, k])

        # Calculate the reconstruction error (MSE)
        reconstructed_matrix = np.dot(P, Q.T)
        mse = np.sum((matrix.values - reconstructed_matrix) ** 2) / np.sum(matrix.values > 0)
        mse_values_sgd.append(mse)

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{num_epochs}, SGD MSE: {mse}")

    return P, Q, mse_values_sgd

# Load your training data
df_train = pd.read_csv('train.csv')
df_train.drop_duplicates(inplace=True)

# Pivot the table and fill NaN values with 0
user_movie_matrix_train = df_train.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Set hyperparameters for SGD training
num_latent_factors_sgd = 10
num_epochs_sgd = 50
learning_rate_sgd = 0.01
lambda_reg_sgd = 0.1

# Train SGD model and obtain user and item factors
user_factors_sgd, item_factors_sgd, mse_values_sgd = stochastic_gradient_descent(user_movie_matrix_train, num_latent_factors_sgd, num_epochs_sgd, learning_rate_sgd, lambda_reg_sgd)

# Display or plot SGD training MSE
plt.plot(mse_values_sgd, label='SGD MSE', color='green')
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Convergence of MSE (SGD)')
plt.legend()
plt.grid(True)
plt.show()

# Load test data
df_test = pd.read_csv('test.csv')

# Pivot the table and fill NaN values with 0
user_movie_matrix_test = df_test.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Make predictions for the test set using SGD
test_predictions_sgd = np.dot(user_factors_sgd, item_factors_sgd.T)

# Extract predictions for the test set
test_user_ids_sgd = df_test['user-id'].values
test_movie_ids_sgd = df_test['movie-id'].values
test_predictions_sgd = test_predictions_sgd[test_user_ids_sgd - 1, test_movie_ids_sgd - 1]  # Adjust for 0-based indexing

# Clip predictions to the valid range (0 to 5)
test_predictions_sgd = np.clip(test_predictions_sgd, a_min=0, a_max=5)

# Create a DataFrame with the test predictions
test_predictions_df_sgd = pd.DataFrame({'user-id': test_user_ids_sgd, 'movie-id': test_movie_ids_sgd, 'prediction': test_predictions_sgd})

# Save the predictions to a CSV file
test_predictions_df_sgd.to_csv('test_predictions_sgd.csv', index=False)

# Display or further analyze the predictions
print(test_predictions_df_sgd.head())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ALS Implementation with MSE Calculation
def als(matrix, num_latent_factors, num_epochs, learning_rate, lambda_reg):
    N, M = matrix.shape
    P = np.random.rand(N, num_latent_factors)
    Q = np.random.rand(M, num_latent_factors)

    mse_values_als = []

    for epoch in range(num_epochs):
        for i in range(N):
            for j in range(M):
                if matrix.iloc[i, j] > 0:
                    eij = matrix.iloc[i, j] - np.dot(P[i, :], Q[j, :].T)
                    for k in range(num_latent_factors):
                        P[i, k] = P[i, k] + learning_rate * (2 * eij * Q[j, k] - lambda_reg * P[i, k])
                        Q[j, k] = Q[j, k] + learning_rate * (2 * eij * P[i, k] - lambda_reg * Q[j, k])

        # Calculate the reconstruction error (MSE)
        reconstructed_matrix = np.dot(P, Q.T)
        mse = np.sum((matrix.values - reconstructed_matrix) ** 2) / np.sum(matrix.values > 0)
        mse_values_als.append(mse)

        if epoch % 10 == 0:
            print(f"Epoch {epoch}/{num_epochs}, ALS MSE: {mse}")

    return P, Q, mse_values_als

# Load your training data
df_train = pd.read_csv('train.csv')
df_train.drop_duplicates(inplace=True)

# Pivot the table and fill NaN values with 0
user_movie_matrix_train = df_train.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Set hyperparameters for ALS training
num_latent_factors_als = 10
num_epochs_als = 50
learning_rate_als = 0.01
lambda_reg_als = 0.1

# Train ALS model and obtain user and item factors
user_factors_als, item_factors_als, mse_values_als = als(user_movie_matrix_train, num_latent_factors_als, num_epochs_als, learning_rate_als, lambda_reg_als)

# Display or plot ALS training MSE
plt.plot(mse_values_als, label='ALS MSE', color='red')
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Convergence of MSE (ALS)')
plt.legend()
plt.grid(True)
plt.show()

# Load test data
df_test = pd.read_csv('test.csv')

# Pivot the table and fill NaN values with 0
user_movie_matrix_test = df_test.pivot_table(index='user-id', columns='movie-id', values='recommendation-score').fillna(0)

# Make predictions for the test set using ALS
test_predictions_als = np.dot(user_factors_als, item_factors_als.T)

# Extract predictions for the test set
test_user_ids_als = df_test['user-id'].values
test_movie_ids_als = df_test['movie-id'].values
test_predictions_als = test_predictions_als[test_user_ids_als - 1, test_movie_ids_als - 1]  # Adjust for 0-based indexing

# Clip predictions to the valid range (0 to 5)
test_predictions_als = np.clip(test_predictions_als, a_min=0, a_max=5)

# Create a DataFrame with the test predictions
test_predictions_df_als = pd.DataFrame({'user-id': test_user_ids_als, 'movie-id': test_movie_ids_als, 'prediction': test_predictions_als})

# Save the predictions to a CSV file
test_predictions_df_als.to_csv('test_predictions_als.csv', index=False)

# Display or further analyze the predictions
print(test_predictions_df_als.head())