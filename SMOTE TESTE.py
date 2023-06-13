'''
Created on 23 de maio de 2018
@author: Bruno Roberto
'''
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

leads = pd.read_csv('tabela_new_leads_com_smote.csv')
print ('== TAMANHO COM BOOTSTRAP==')
print(leads.estagio.value_counts())



(
    training_features, # tabela de treinamento para outras colunas
    test_features, # tabela de teste para outras colunas
    training_target, # tabela de treinamento para coluna estagio
    test_target # tabela de teste para coluna estagio
) = train_test_split(
        leads.drop(['estagio'], axis=1), # tabela sem a coluna estagio
        leads['estagio'], # apenas a coluna estagio
#         test_size = .2,
#         random_state=42
)

training_x, test_x, training_y, test_y = train_test_split(
    training_features,
    training_target,
    test_size = .48,
    #random_state = 42
)


rus = RandomUnderSampler(random_state=0, replacement=True, ratio=1)
training_x_rus, training_y_rus = rus.fit_resample(training_x, training_y)
print("\n",np.vstack({tuple(row) for row in training_x_rus}).shape)
# 
# 
# 
# print('Original dataset shape %s' % Counter(training_y))
# 
# smote = SMOTE(random_state = 42, ratio = 1)
# training_x_smote, training_y_smote = smote.fit_sample(training_x, training_y)
# 
# print('Resampled dataset shape %s' % Counter(training_y_smote))
# 
# print("\n")

# salvando o resultado do SMOTE em um nova planilha
lines =[]
for position, value in enumerate(training_y_rus):
    new_line_x = [str(number) for number in training_x_rus[position].tolist()]
    new_line_y = str(training_y_rus[position])
    new_line = new_line_x + [new_line_y]
    new_line_string = ','.join(new_line) + '\n'
    lines.append(new_line_string)
new_leads_csv = open('tabela_new_leads_balanceado.csv', 'w')
new_leads_csv.write(','.join(leads.columns)+'\n')
new_leads_csv.writelines(lines)
new_leads_csv.close()
print ('\n\n Dataframe salvo em "tabela_new_leads_balanceado.csv"')

new_leads = pd.read_csv('tabela_new_leads_balanceado.csv')
print ('\n\n== TAMANHO PÓS-SMOTE ==')
print(new_leads.estagio.value_counts())


# aplicando o RandomForest nos dados pós-smote
random_forest = RandomForestClassifier(n_estimators=25, random_state=42)
random_forest.fit(training_x_rus, training_y_rus)


print ('\n\n== PRECISÃO DO SMOTE ==')
#A sobreamostragem é feita somente nos dados de treinamento, 
#nenhuma das informações nos dados de validação está sendo usada 
#para criar observações sintéticas
print ('\nValidation Results')
print (random_forest.score(test_x, test_y))
# Quanto mais próximo o resultado dos dados de validação com treinamento
# for dos dados de teste, melhor a presição do SMOTE
print ('\nTest Results')
print (random_forest.score(test_features, test_target))

