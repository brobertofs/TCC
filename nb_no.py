'''Created on 28 de dezembro de 2018
@author: Bruno Roberto'''

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from imblearn.over_sampling import SMOTE
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report,confusion_matrix

leads = pd.read_csv('tabela_new_leads_com_smote.csv')
print ('== TAMANHO ORIGINAL ==')
print(leads.estagio.value_counts())



def processaTexto(texto):
    #remove pontuação caractere a caractere
    nopunc = [char for char in texto if char not in string.punctuation]
    #junta os caracteres em palavras novamente
    nopunc = ''.join(nopunc)
    
    #nopunc.split() separa cada frase em palavras, retirando as que estão dentro de stopwords
    #word.lower() torna todas as letras minúsculas
    #essa linha remove as stopwords, retornando apenas as palavras relevantes para a análise
    cleanWords = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]
        
    return cleanWords


leads = pd.read_csv('tabela_new_leads_com_smote.csv')
print ('== TAMANHO ORIGINAL ==')
print(leads.estagio.value_counts())

#aplica a função len em cada mensagem de texto analisada
leads['length'] = leads['estagio'].apply(len)

#divide os conjuntos em treinamento e teste
#msg_train e msg_test são os conjuntos de treinamento e teste da base de dados de mensagens
#class_train e class_test são, respectivamente, os rótulos dos sets de teste e treinamento 
#por parâmetro são passados os conjuntos de mensagens e o conjunto de rótulos (tipo), bem como o tamanho da base de teste
msg_train, msg_test, class_train, class_test = train_test_split(leads['estagio'], leads['eventos'], test_size=0.1)

#pipeline de transformação com estimador. sequencialmente aplica uma lista de transformações
#a primeira converte documentos de texto em uma matriz com contagem de tokens, ou seja, conta 
#a ocorrência de cada palavra no vocabulário a segunda normaliza a contagem (term frequency times 
#inverse document frequency) este escala para baixo o impacto de tokens que ocorrem frequentemente 
#e que sejam empiricamente menos informativos do que features que ocorrem em uma pequena fração 
#do treinamento a última linha treina esses vetores no classificador naive bayes
pipeline = Pipeline([
    ('bow',CountVectorizer()), # converts strings to integer counts
    ('tfidf',TfidfTransformer()), # converts integer counts to weighted TF-IDF scores
    ('classifier',MultinomialNB()) # train on TF-IDF vectors with Naive Bayes classifier
])

#treina o modelo
pipeline.fit(msg_train,class_train)

#testa o modelo
predictions = pipeline.predict(msg_test)
