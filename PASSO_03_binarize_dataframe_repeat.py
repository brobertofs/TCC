'''
Created on 14 de mai de 2018

@author: Bruno Roberto
'''

def main():
    # abrindo e lendo a planilha original e salvando em 'data_leads'
    # como uma lista das linhas da planilha
    leads_csv = open('tabela_final_passo_02.csv', 'r')
    data_leads = leads_csv.readlines()
    leads_csv.close()

    # todos os dados da planilha, com a excecao da primeira linha
    # (títulos: colunas eventos e estagio)
    body = data_leads[1:]
    body = [line.replace('\n','').replace('\r','') for line in body]

    # inicializando as listas que representam o título
    # e os dados da nova planilha a ser gerada
    new_title = []
    new_lines = []  # tambem poderia ser 'new_body'

    # inicializando o dicionario de eventos e o contador de eventos
    events = {}
    # excluindo eventos desnecessários
    events_block = ['members_export_51d7db9b76', 'cadastro-pro']
    cont = 0

    # percorrendo cada linha/usuario dos dados da planilha original
    for line in body:
        # pegando os eventos (coluna 1) e o estágio (coluna 2)
        # de cada linha/usuario, separados por ','
        events_by_user = line.split(',')[0]
        estagio = line.split(',')[1]
        

        # inicializando a nova linha (binarizada) a ser escrita na nova planilha, 
        # começando com as 39 colunas de eventos do usuario iniciadas com o valor '0'
        # mais a coluna estagio que já está pronta binarizada
        new_line = ([0] * 39) + [estagio] 

        # salvando os eventos de cada linha/usuario em uma lista,
        # separados por '/'
        list_events_by_user = events_by_user.split(' / ')

        # percorrendo cada evento da linha/usuario por vez
        for event in list_events_by_user:
            # ignora eventos não desejados
            if event.strip() in events_block:
                continue
            # retirando os espacos vazios do inicio e final, por
            # exemplo, ' Experimente - site ' fica 'Experimente - site'
            event = event.strip()
#             print(event)

            # se o evento nao existir no dicionario
            if event not in events:
                # incrementando o contador e salvando o novo evento com a
                # chave igual ao nome do evento e o valor do contador              
                events[event] = cont
                cont += 1
                
                # adicionando no novo titulo o novo evento encontrado,
                # com o valor igual a 'e_x' sendo x o valor do contador
                new_title.append('e'+str(cont))
                # print('new_title', new_title)

            # resgatando a posicao do evento atual na ordem em que os
            # eventos foram encontrados (e adicionados na linha do titulo)
            position = events[event]
            # inserindo na nova linha binarizada o valor 1 para cada evento
            # encontrado de cada usuario, na posicao resgatada em 'position'
            new_line[position] += 1

        # ao percorrer todos os eventos da linha/usuario, transforma a
        # lista 'new_line' em uma string, separando os elementos por ','
        # e adicionado uma quebra de linha '\n' ao final
        new_line = [str(x) for x in new_line]
        new_line_string = ','.join(new_line) + '\n'
        # print('new_line', new_line_string)

        # adiciona a nova linha em formato de string na lista de novas
        # linhas binarizadas, ou seja, o novo 'body' da planilha
        new_lines.append(new_line_string)

    # criando e escrevendo em um novo arquivo a nova planilha, com as
    # listas 'new_title' e 'new_lines' com os valores das colunas de eventos somados pelo contador
    # e com 38 colunas (39 eventos  + 24 eventos existentes)
    print("Os eventos são: ")
    print(events, '\n')
    new_title = new_title + ['estagio']
    new_leads_csv = open('tabela_final_passo_03.csv', 'w')
    new_leads_csv.write(','.join(new_title)+'\n')
    new_leads_csv.writelines(new_lines)
    new_leads_csv.close()
    print("Planilha salva em: tabela_final_passo_03.csv")

if __name__ == "__main__":
    main()
