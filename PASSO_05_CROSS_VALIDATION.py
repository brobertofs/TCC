# '''
# Created on 28 de dezembro de 2018
# @author: Bruno Roberto
# '''
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# 
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import classification_report,confusion_matrix
# 
# #Importando bibliotecas para visualização da árvore
# from IPython.display import Image  
# from sklearn.externals.six import StringIO  
# from sklearn.tree import export_graphviz
# import pydot

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cross_decomposition import train_test_split
from sklearn.metrics import mean_absolute_error
