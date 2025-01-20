# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gNH8sbl2SsRc2WT7C7RA6V47BROvaJcS
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# Load the dataset from JSON file
df = pd.read_json("loan_approval_dataset.json")

# Show first 5 rows
df.head()

# Check for missing values
print(df.isnull().sum())  # No null values in your case

# Drop the 'Id' column as it is not useful for the analysis
df.drop(columns=['Id'], inplace=True)

# Get basic statistics for numerical columns
df.describe()

# Identify and separate numeric and categorical columns
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = df.select_dtypes(include=['object']).columns

# Visualize distribution for numeric columns
fig, axs = plt.subplots(len(numeric_cols), figsize=(5, 5 * len(numeric_cols)))
for i, col in enumerate(numeric_cols):
    sns.histplot(df[col], ax=axs[i], kde=True)
    axs[i].set_title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Boxplot for numeric columns to check for outliers
fig, axs = plt.subplots(len(numeric_cols), figsize=(5, 5 * len(numeric_cols)))
for i, col in enumerate(numeric_cols):
    sns.boxplot(df[col], ax=axs[i])
    axs[i].set_title(f'Boxplot of {col}')
plt.tight_layout()
plt.show()

# Visualizing categorical columns
for col in categorical_cols:
    print(f"{col} value counts:")
    print(df[col].value_counts())
    print("__" * 20)

# Encode categorical columns using One-Hot Encoding
df_encoded = pd.get_dummies(df, drop_first=True, dtype=int)

# Separate target (Risk_Flag) from the features
X = df_encoded.drop(columns=['Risk_Flag'])
y = df_encoded['Risk_Flag']



numeric = X.select_dtypes("int","float").columns

# Standardize numerical features using StandardScaler
scaler = StandardScaler()
X[numeric] = scaler.fit_transform(X[numeric])

# Apply Label Encoding to the target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split data into train and test sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize Logistic Regression model
log_reg = LogisticRegression(max_iter=500)

# Train the model
log_reg.fit(X_train, y_train)

# Make predictions
y_pred = log_reg.predict(X_test)

# Evaluate model performance
print(f"Logistic Regression - F1 Score: {f1_score(y_test, y_pred)}")
print(f"Logistic Regression - Recall: {recall_score(y_test, y_pred)}")
print(f"Logistic Regression - Precision: {precision_score(y_test, y_pred)}")
print(f"Logistic Regression - Accuracy: {accuracy_score(y_test, y_pred)}")

# Classification report for Logistic Regression
print("Classification Report for Logistic Regression:")
print(classification_report(y_test, y_pred))

# Initialize Decision Tree model
dt = DecisionTreeClassifier(ccp_alpha=0.1, max_depth=50)

# Train the Decision Tree model
dt.fit(X_train, y_train)

# Make predictions
y_pred = dt.predict(X_test)

# Evaluate model performance
print(f"Decision Tree - Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report for Decision Tree:")
print(classification_report(y_test, y_pred))

# Initialize Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the Random Forest model
rf.fit(X_train, y_train)

# Make predictions
y_pred_rf = rf.predict(X_test)

# Evaluate model performance
print(f"Random Forest - Accuracy: {accuracy_score(y_test, y_pred_rf)}")
print("Classification Report for Random Forest:")
print(classification_report(y_test, y_pred_rf))

# Initialize AdaBoost model
ab = AdaBoostClassifier(n_estimators=50, random_state=42)

# Train the AdaBoost model
ab.fit(X_train, y_train)

# Make predictions
y_pred_ab = ab.predict(X_test)

# Evaluate model performance
print(f"AdaBoost - Accuracy: {accuracy_score(y_test, y_pred_ab)}")
print("Classification Report for AdaBoost:")
print(classification_report(y_test, y_pred_ab))
# Initialize Gradient Boosting model
gb = GradientBoostingClassifier(n_estimators=100, random_state=42)

# Train the Gradient Boosting model
gb.fit(X_train, y_train)

# Make predictions
y_pred_gb = gb.predict(X_test)

# Evaluate model performance
print(f"Gradient Boosting - Accuracy: {accuracy_score(y_test, y_pred_gb)}")
print("Classification Report for Gradient Boosting:")
print(classification_report(y_test, y_pred_gb))

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Train Logistic Regression on resampled data
log_reg.fit(X_train_resampled, y_train_resampled)

# Make predictions on the test set
y_pred_smote = log_reg.predict(X_test)

# Evaluate model performance after SMOTE
print("Classification Report After Using SMOTE for Logistic Regression:")
print(classification_report(y_test, y_pred_smote))

# Train Decision Tree on resampled data
dt.fit(X_train_resampled, y_train_resampled)

# Make predictions with Decision Tree
y_pred_smote_dt = dt.predict(X_test)

# Evaluate Decision Tree performance after SMOTE
print(f"Decision Tree - Accuracy After SMOTE: {accuracy_score(y_test, y_pred_smote_dt)}")

# Train Random Forest on resampled data
rf.fit(X_train_resampled, y_train_resampled)
y_pred_smote_rf = rf.predict(X_test)

# Evaluate Random Forest after SMOTE
print(f"Random Forest - Accuracy After SMOTE: {accuracy_score(y_test, y_pred_smote_rf)}")
print(classification_report(y_test, y_pred_smote_rf))

# Train AdaBoost on resampled data
ab.fit(X_train_resampled, y_train_resampled)
y_pred_smote_ab = ab.predict(X_test)

# Evaluate AdaBoost after SMOTE
print(f"AdaBoost - Accuracy After SMOTE: {accuracy_score(y_test, y_pred_smote_ab)}")
print(classification_report(y_test, y_pred_smote_ab))

# Train Gradient Boosting on resampled data
gb.fit(X_train_resampled, y_train_resampled)
y_pred_smote_gb = gb.predict(X_test)

# Evaluate Gradient Boosting after SMOTE
print(f"Gradient Boosting - Accuracy After SMOTE: {accuracy_score(y_test, y_pred_smote_gb)}")
print(classification_report(y_test, y_pred_smote_gb))