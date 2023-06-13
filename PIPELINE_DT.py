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
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

leads = pd.read_csv('tabela_new_leads_com_repeticoes2.csv')
print ('== TAMANHO ORIGINAL ==')
print(leads.estagio.value_counts())

# gerando os dados de teste e treinamento
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
    test_size = .5,
    random_state=42
)

# aplicando os SMOTE nos dados do segundo conjunto
smote = SMOTE(random_state=42, ratio = 1)
training_x_smote, training_y_smote = smote.fit_sample(training_x, training_y)

# salvando o resultado do SMOTE em um nova planilha
lines =[]
for position, value in enumerate(training_y_smote):
    new_line_x = [str(number) for number in training_x_smote[position].tolist()]
    new_line_y = str(training_y_smote[position])
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


# aplicando o RandomForest nos dados pós-smote
random_forest = RandomForestClassifier(n_estimators=25, random_state=43)
random_forest.fit(training_x_smote, training_y_smote)


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

