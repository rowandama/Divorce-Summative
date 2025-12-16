## Divorce Predictor

This project explores the predictors of divorce using a simulated dataset of 5,000 observations. The main goal is to assess whether internal relationship factors (e.g., communication, infidelity, trust) or structural factors (e.g., age at marriage, education, income) are stronger predictors of divorce.
The analysis includes:
- Descriptive statistics of internal and structural variables
- Multiple logistic regression models for internal, structural, and combined factors
- Interpretation of significant predictors and model performance
- Interactive Shiny dashboard for exploring predicted probabilities of divorce based on user-defined profiles
  
This project provides insights into the role of individual agency versus structural constraints in influencing divorce outcomes.

**This repository consists of these files:**
- divorce_df.csv – The cleaned dataset used for analysis
- notebook.ipynb – Jupyter notebook with full data analysis, model building, and interpretation
- app.py – Shiny app script for interactive prediction and visualization
- requirements.txt – Python environment dependencies
- README.md – Project documentation

**Methodology**

***Data Exploration & Descriptive Statistics***
Summary statistics for internal and structural variables
Identification of distributions, ranges, and key characteristics

***Multiple Logistic Regression (MLR)***
Internal factors model, structural factors model, and combined model
Assessment of significance of predictors
Comparison of model fit using pseudo R² and chi-squared tests
***Interpretation***

Internal factors generally show stronger predictive power for divorce
Highlights the importance of relationship dynamics and individual agency over structural constraints
***Interactive Dashboard***

Built using Python Shiny
Allows users to input personal or hypothetical relationship profiles
Displays predicted probabilities of divorce 
