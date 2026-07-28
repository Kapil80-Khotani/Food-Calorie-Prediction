# 🍽️ Food Calorie Prediction using Machine Learning & NLP

A Machine Learning and Natural Language Processing (NLP) project that predicts the calorie content of recipes from their titles and ingredients. The project combines text preprocessing, TF-IDF vectorization, feature engineering, and multiple regression models to estimate recipe calories.

---

## Project Overview

Estimating the calorie content of recipes manually requires nutritional databases and can be time-consuming. This project automates calorie prediction by learning patterns from recipe titles and ingredient lists.

The workflow includes:

- Data cleaning
- NLP preprocessing
- Feature engineering
- TF-IDF vectorization
- Machine Learning model training
- Model evaluation
- Model serialization for future predictions

---

## Features

- Recipe data preprocessing
- Text cleaning using Regular Expressions
- Stopword removal
- Lemmatization
- Word-level TF-IDF
- Character-level TF-IDF
- Feature engineering
- Multiple regression models
- Model comparison
- Prediction visualization
- Saved trained model

---

## Dataset

The dataset contains recipes scraped from recipe websites.

Features include:

- Recipe Title
- Ingredients
- Calories

Example:

| Recipe | Calories |
|---------|----------|
| Garlic Chicken | 420 |
| Vegetable Soup | 165 |
| Apple Pie | 315 |

---

## Workflow

```
Recipe Dataset
      │
      ▼
Data Cleaning
      │
      ▼
NLP Preprocessing
(Lowercase → Regex → Stopwords → Lemmatization)
      │
      ▼
Feature Engineering
      │
      ├── Ingredient Count
      ├── Quantity Count
      ├── High-Calorie Ingredients
      ├── Cooking Methods
      └── Food Categories
      │
      ▼
TF-IDF Vectorization
      │
      ├── Word TF-IDF
      └── Character TF-IDF
      │
      ▼
Feature Combination
      │
      ▼
Train/Test Split
      │
      ▼
Regression Models
      │
      ▼
Evaluation
```

---

## Models Evaluated

| Model | Purpose |
|--------|---------|
| Linear Regression | Baseline |
| Ridge Regression | Final Model |
| Elastic Net | Regularized Regression |
| XGBoost | Gradient Boosting |

---

## Final Model Performance

| Metric | Score |
|---------|-------|
| MAE | **111.76** |
| RMSE | **152.14** |
| R² Score | **0.458** |

Among the evaluated models, **Ridge Regression** was selected because it provided the best balance between prediction accuracy, training speed, and generalization.

---

## Visualizations

The project includes the following visualizations:

- Calories Distribution
- Ingredient Count Distribution
- Ingredient Count vs Calories
- Actual vs Predicted Calories
- Residual Plot

---

## Example Predictions

| Recipe | Actual | Predicted |
|---------|--------|-----------|
| Dairy-Free Pumpkin Pie | 153 | 152.95 |
| Spicy Turkey Tacos | 246 | 246.07 |
| My Favorite Chicken Salad | 287 | 286.89 |

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- SciPy
- NLTK
- XGBoost
- Joblib

---

## Project Structure

```
Food-Calorie-Prediction/
│
├── data/
│   └── recipes_dataset.csv
│
├── models/
│   ├── ridge_calorie_model.pkl
│   ├── word_tfidf.pkl
│   └── char_tfidf.pkl
│
├── notebook/
│   └── Food_Calorie_Prediction.ipynb
│
├── outputs/
│   ├── actual_vs_predicted.png
│   ├── residual_plot.png
│   ├── model_comparison.csv
│   └── prediction_results.csv
│
├── src/
│   └── scrape_recipe.py
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Kapil80-Khotani/Food-Calorie-Prediction.git
```

Move into the project folder:

```bash
cd Food-Calorie-Prediction
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```
notebook/Food_Calorie_Prediction.ipynb
```

---

## Future Improvements

- BERT-based calorie prediction
- Nutrition API integration
- Recipe recommendation system
- Streamlit web application
- FastAPI deployment

---

## Author

**Kapil Khotani**

Machine Learning • Data Science • Natural Language Processing

GitHub: https://github.com/Kapil80-Khotani

---

## Acknowledgements

This project uses the following open-source libraries:

- Scikit-learn
- NLTK
- XGBoost
- Pandas
- NumPy
- Matplotlib
- SciPy

---

If you found this project useful, consider giving it a ⭐ on GitHub.
