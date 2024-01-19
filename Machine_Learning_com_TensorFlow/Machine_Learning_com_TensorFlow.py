from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Carregar dados
iris = load_iris()
X, y = iris.data, iris.target

# Definir modelo
modelo = RandomForestClassifier()

# Definir grade de hiperparâmetros
param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10]}

# Realizar busca em grade
grid_search = GridSearchCV(modelo, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X, y)

# Melhores hiperparâmetros
melhores_parametros = grid_search.best_params_
print(f'Melhores Hiperparâmetros: {melhores_parametros}')
