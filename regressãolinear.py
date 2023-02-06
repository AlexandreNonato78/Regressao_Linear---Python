# -*- coding: utf-8 -*-
"""RegressãoLinear.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v5GSBnrMnT3p1fZZS22dPA-on6_60mke
"""

# Importação das bibliotecas
# ---- Basics
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# ---- Cronometrar o tempo do colab
import time

# ---- Pré-processamento
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler

# ---- Possíveis Modelos utilizados

from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LassoCV, ElasticNet, ElasticNetCV, HuberRegressor, LassoLars, BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, ExtraTreesRegressor

# ---- Cálculo das Métricas
from sklearn import metrics

car = pd.read_csv('Car.csv', sep=";")

car.head()

car.info()

car = pd.get_dummies(data=car, columns=['CarName','fueltype','aspiration','doornumber','carbody'])

car.head()

car.dtypes

X = car[car.columns[(car.columns != 'price') & (car.columns != 'car_ID')]]
y =car['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 123)

print(len(X_train))

car.columns

scaler = StandardScaler()
colunas_scaler =['symboling','wheelbase','carlength','carwidth','carheight',
                 'curbweight','enginesize','boreratio','stroke','compressionratio','horsepower','peakrpm','citympg','highwaympg']
                 
scaler.fit(X_train[colunas_scaler])
X_train = X_train.reset_index().drop('index',axis=1)
X_test = X_test.reset_index().drop('index',axis=1)
y_train = y_train.reset_index().drop('index',axis=1)
y_test = y_test.reset_index().drop('index',axis=1)


X_train[colunas_scaler] = pd.DataFrame(scaler.transform(X_train[colunas_scaler]),columns=colunas_scaler)
X_train.head()

X_test[colunas_scaler] = pd.DataFrame(scaler.transform(X_train[colunas_scaler]),columns=colunas_scaler)
X_test.head()

# Treinamento e validação dos Modelos

models = {
    'LinearReg': LinearRegression(),
    'RidgeReg': Ridge(),
    'LassoReg': Lasso(),
    'ElasticNetReg': ElasticNet(),
    'HuberReg': HuberRegressor(),
    'LassoCV': LassoCV(),
    'ElasticNetCV': ElasticNetCV(),
    'LassoLars': LassoLars(),
    'BayesianRidge': BayesianRidge(),
    'DecisionTreeRegressor': DecisionTreeRegressor(),
    'SVM_RBF':SVR(kernel='rbf'),
    'SVM_POLY':SVR(kernel='poly'),
    'SVM_LINEAR':SVR(kernel='linear',max_iter=10**4),
    'SVM_SIG':SVR(kernel='sigmoid'),
    'SGDRegressor':SGDRegressor(),
    'RandomForestRegressor':RandomForestRegressor(),
    'AdaBoostRegressor':AdaBoostRegressor(),
    'GradientBoostingRegressor':GradientBoostingRegressor(),
    'ExtraTreesRegressor':ExtraTreesRegressor()
}

for model in models.values():
    model.fit(X_train, y_train);

eval = []
nome = []
r2 = []
MAE = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    nome.append(name)
    eval.append(metrics.mean_squared_error(y_test,y_pred))
    r2.append(metrics.r2_score(y_test,y_pred))
    MAE.append(metrics.mean_absolute_error(y_test,y_pred))
    print('-------------------------')
    print(name + ":\n R² : {:.4f}\n MSE: {:.4F}\n MAE: {:.4F}".format(metrics.r2_score(y_test,y_pred),metrics.mean_squared_error(y_test,y_pred),metrics.mean_absolute_error(y_test,y_pred)))
    print('-------------------------')

# Tabela de Métricas por Modelo

teste = pd.DataFrame({'Modelo': nome, 'MSE': eval, 'R2': r2, 'MAE':MAE})
teste.nsmallest(18,['MAE'])

GBR = GradientBoostingRegressor()
parameters = {'learning_rate': [0.01,0.02,0.03,0.04],
                  'subsample'    : [0.9, 0.5, 0.2, 0.1],
                  'n_estimators' : [100,500,1000, 1500],
                  'max_depth'    : [4,6,8,10]
                 }

reg = GridSearchCV(estimator=GBR, param_grid = parameters, cv = 2, n_jobs=-1)
reg.fit(X_train, y_train)

Reg_Best = reg.best_estimator_
Reg_Best

# Cálculo das Melhores métricas atingidas no Mini-Case

Reg_Best.fit(X_train,y_train)
y_pred = Reg_Best.predict(X_test)
print('-------------------------')
print(name + ":\n R² : {:.4f}\n MSE: {:.4F}\n MAE: {:.4F}".format(metrics.r2_score(y_test,y_pred),metrics.mean_squared_error(y_test,y_pred),metrics.mean_absolute_error(y_test,y_pred)))
print('-------------------------')

# Criando uma tabela com todos os valores e seus preditores

df_total_final = car.copy()
car[colunas_scaler] = pd.DataFrame(scaler.transform(car[colunas_scaler]),columns=colunas_scaler)
df_total_final['previsto'] = Reg_Best.predict(car[car.columns[(car.columns != 'price') & (car.columns != 'car_ID')]])
df_total_final[['price','previsto']]

