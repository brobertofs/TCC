'''
Created on 28 de dezembro de 2018
@author: Bruno Roberto
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report,confusion_matrix

#Importando bibliotecas para visualização da árvore
from IPython.display import Image  
from sklearn.externals.six import StringIO  
from sklearn.tree import export_graphviz
import pydot


leads = pd.read_csv('tabela_new_leads_com_smote.csv')

x = leads.drop('estagio',axis=1)
y = leads['estagio']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

dtree = DecisionTreeClassifier()
dtree.fit(x_train,y_train)


predictions = dtree.predict(x_test)
print(classification_report(y_test,predictions))
print("\n")
print(confusion_matrix(y_test,predictions))
print("\n")

###Visualização da árvore
features = list(leads.columns[:43])
print(features)
 
dot_data = StringIO()  
export_graphviz(dtree, out_file=dot_data,feature_names=features,filled=True,rounded=True)
 
graph = pydot.graph_from_dot_data(dot_data.getvalue())  
Image(graph[0].create_png()) 