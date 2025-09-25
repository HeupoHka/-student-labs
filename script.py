import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score

# Загрузка данных
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

# 1. Инжиниринг признаков (пример)
train_df['BMI'] = train_df['weight(kg)'] / (train_df['height(cm)'] / 100) ** 2
test_df['BMI'] = test_df['weight(kg)'] / (test_df['height(cm)'] / 100) ** 2

# 2. Разделение на признаки и целевую переменную
X = train_df.drop(['id', 'smoking'], axis=1)
y = train_df['smoking']
X_test = test_df.drop('id', axis=1)

# 3. Масштабирование признаков
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_test_scaled = scaler.transform(X_test)

# 4. Кросс-валидация и оценка моделей
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    'LightGBM': LGBMClassifier(n_estimators=100, class_weight='balanced', random_state=42)
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    cv_scores = cross_val_score(model, X_scaled, y, cv=skf, scoring='roc_auc')
    print(f"{name} - Mean ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# 5. Обучение лучшей модели на всех данных и создание сабмита
best_model = LGBMClassifier(n_estimators=100, class_weight='balanced', random_state=42)
best_model.fit(X_scaled, y)
predictions = best_model.predict_proba(X_test_scaled)[:, 1] # Берем вероятность класса 1

# 6. Формирование файла для отправки
submission = pd.DataFrame({'id': test_df['id'], 'smoking': predictions})
submission.to_csv('my_submission.csv', index=False)