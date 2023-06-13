'''
Created on 23 de maio de 2018
@author: Bruno Roberto
'''
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
from imblearn.under_sampling import RandomUnderSampler

leads = pd.read_csv('tabela_new_leads_com_repeticoes2.csv')
print ('== TAMANHO ORIGINAL ==')
print(leads.estagio.value_counts())


x = leads.drop('estagio',axis=1)
y = leads['estagio']

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=.9)

smote = SMOTE(random_state = 42, ratio = 1)
x_train, y_train = smote.fit_sample(x_train, y_train)



# # aplicando os SMOTE nos dados do segundo conjunto
# smote = SMOTETomek(ratio='auto')
# training_x_smote, training_y_smote = smote.fit_sample(training_x, training_y)
# 
# 
#salvando o resultado do SMOTE em um nova planilha
lines =[]
for position, value in enumerate(y_train):
    new_line_x = [str(number) for number in x_train[position].tolist()]
    new_line_y = str(y_train[position])
    new_line = new_line_x + [new_line_y]
    new_line_string = ','.join(new_line) + '\n'
    lines.append(new_line_string)
new_leads_csv = open('tabela_new_leads_com_smote.csv', 'w')
new_leads_csv.write(','.join(leads.columns)+'\n')
new_leads_csv.writelines(lines)
new_leads_csv.close()
print ('\n\n Dataframe salvo em "tabela_new_leads_com_smote.csv"')
 
new_leads = pd.read_csv('tabela_new_leads_com_smote.csv')
print ('\n\n== TAMANHO PÓS-SMOTE ==')
print(new_leads.estagio.value_counts())
# 
# 
# aplicando o RandomForest nos dados pós-smote
random_forest = RandomForestClassifier(n_estimators=25, random_state=43)
random_forest.fit(x_train, y_train)
 
 
print ('\n\n== PRECISÃO DO SMOTE ==')
#A sobreamostragem é feita somente nos dados de treinamento, 
#nenhuma das informações nos dados de validação está sendo usada 
#para criar observações sintéticas
print ('\nValidation Results')
print (random_forest.score(x_train, y_train))
# Quanto mais próximo o resultado dos dados de validação com treinamento
# for dos dados de teste, melhor a presição do SMOTE
print ('\nTest Results')
print (random_forest.score(x_test, y_test))

