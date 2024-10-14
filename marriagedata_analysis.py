# -*- coding: utf-8 -*-
"""MarriageData Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/197mmaUcQpCytaGr6bFVMG0YiSTNIHSo3
"""

import pandas as pd
df=pd.read_csv('/content/marriage.csv')
df.head()

# Data cleansing and Data transformation
df_cleaned = df.drop(0).reset_index(drop=True)
df_cleaned.columns = [
    "Area_Name",
    "Total",
    "Educational_Level",
    "Age_at_Marriage",
    "Married_Males",
    "Married_Females"
]
df_cleaned["Married_Males"] = pd.to_numeric(df_cleaned["Married_Males"], errors='coerce')
df_cleaned["Married_Females"] = pd.to_numeric(df_cleaned["Married_Females"], errors='coerce')


df_cleaned_info = df_cleaned.info()
df_cleaned_head = df_cleaned.head()

df_cleaned_info, df_cleaned_head

#Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.barplot(data=df_cleaned, x='Age_at_Marriage', y='Married_Males', color='blue', label='Males')
sns.barplot(data=df_cleaned, x='Age_at_Marriage', y='Married_Females', color='pink', label='Females')
plt.xticks(rotation=45)
plt.xlabel('Age at Marriage')
plt.ylabel('Number of Ever Married Persons')
plt.legend()
plt.title('Distribution of Married Males and Females by Age Range')
plt.show()

df_cleaned['Total_Married'] = df_cleaned['Married_Males'] + df_cleaned['Married_Females']
plt.figure(figsize=(10, 6))
sns.barplot(data=df_cleaned, x='Educational_Level', y='Total_Married', palette='viridis')
plt.xticks(rotation=45)
plt.xlabel('Educational Level')
plt.ylabel('Total Married Individuals')
plt.title('Total Married Individuals by Educational Level')
plt.show()

plt.figure(figsize=(6, 4))
sns.heatmap(df_cleaned[['Married_Males', 'Married_Females', 'Total_Married']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

df_age_grouped = df_cleaned.groupby('Age_at_Marriage')[['Married_Males', 'Married_Females']].sum().reset_index()
df_age_grouped.plot(kind='bar', x='Age_at_Marriage', stacked=True, color=['blue', 'pink'], figsize=(10, 6))
plt.xlabel('Age at Marriage')
plt.ylabel('Total Married Persons')
plt.title('Total Married Persons by Age and Gender (Stacked)')
plt.xticks(rotation=45)
plt.legend(['Males', 'Females'])
plt.show()

total_males = df_cleaned['Married_Males'].sum()
total_females = df_cleaned['Married_Females'].sum()
plt.figure(figsize=(6, 6))
plt.pie([total_males, total_females], labels=['Males', 'Females'], autopct='%1.1f%%', colors=['blue', 'pink'])
plt.title('Percentage of Married Males vs. Females')
plt.show()

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_cleaned, x='Age_at_Marriage', y='Total_Married', palette='Set2')
plt.xticks(rotation=45)
plt.xlabel('Age at Marriage')
plt.ylabel('Total Married Individuals')
plt.title('Violin Plot of Total Married Individuals by Age Group')
plt.show()

df_age_trend = df_cleaned.groupby('Age_at_Marriage')[['Married_Males', 'Married_Females']].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_age_trend, x='Age_at_Marriage', y='Married_Males', marker='o', color='blue', label='Males')
sns.lineplot(data=df_age_trend, x='Age_at_Marriage', y='Married_Females', marker='o', color='pink', label='Females')
plt.xticks(rotation=45)
plt.xlabel('Age at Marriage')
plt.ylabel('Number of Married Individuals')
plt.title('Trend of Married Individuals Across Age Ranges')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['Married_Males'], bins=20, color='blue', alpha=0.5, label='Males', log_scale=True)
sns.histplot(df_cleaned['Married_Females'], bins=20, color='pink', alpha=0.5, label='Females', log_scale=True)
plt.xlabel('Number of Married Individuals')
plt.ylabel('Frequency (Log Scale)')
plt.title('Histogram of Married Males and Females')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cleaned, x='Married_Males', y='Married_Females', hue='Area_Name', palette='Set3', s=100)
plt.xlabel('Married Males')
plt.ylabel('Married Females')
plt.title('Scatter Plot Comparing Married Males and Females by Area')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()



from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
le_education = LabelEncoder()
le_area = LabelEncoder()
df_cleaned['Educational_Level_Encoded'] = le_education.fit_transform(df_cleaned['Educational_Level'])
df_cleaned['Area_Name_Encoded'] = le_area.fit_transform(df_cleaned['Area_Name'])
df_ml = df_cleaned.drop(columns=['Area_Name', 'Total', 'Educational_Level', 'Age_at_Marriage'])
missing_values = df_ml.isnull().sum()
df_ml.head(), missing_values

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
X = df_ml[['Married_Females', 'Educational_Level_Encoded', 'Area_Name_Encoded']]
y = df_ml['Married_Males']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
reg_model = LinearRegression()
reg_model.fit(X_train, y_train)
y_pred = reg_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
r2 = r2_score(y_test, y_pred)  # R² Score
print(f"Mean Squared Error (MSE): {mse}")
print(f"R² Score: {r2}")