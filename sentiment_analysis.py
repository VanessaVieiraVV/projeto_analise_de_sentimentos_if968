###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:   Vanessa Vieira da Conceicao
#
# Email:    vvc@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#            Copyright(c) 2016 Vanessa Vieira da Conceicao
#
###############################################################################

import sys
import re

stop_words = open("stop_words.txt", "r")
lista_stop_words = stop_words.readlines() #copia as stop_words para uma lista


def split_on_separators(original, separators):
    ''' Retorna uma versao da string 's' na qual todas as letras sao
        convertidas para minusculas e caracteres de pontuacao sao removidos
        de ambos os extremos. A pontuacao presente no interior da string
        e' mantida intacta.
    '''  
    return filter(lambda x: x != '',re.split('[{0}]'.format(separators),original))    
def clean_up(s):
    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    ''' 
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result
for word in lista_stop_words :
    word2 = clean_up(lista_stop_words.pop(0)) #remove a primeira palavra da lista e guarda na variável word2
    lista_stop_words.append(word2) #adiciona palavra removida do començo da lista de stop words no final da mesma lista
    
def readTrainingSet(fname):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    words = dict()
    trainSet = open(fname,"r")
    lista_trainSet = trainSet.readlines()
    intervalo = [x for x in range(0,5)] #intervalo == [0,1,2,3,4] (possíveis valores de comentários)
    lista_de_palavras = []
    for linha in lista_trainSet:
        palavras_separadas = list(split_on_separators(linha[2:]," ")) 
        for palavra in palavras_separadas:
            palavra = clean_up(palavra) #transformando cada item da lista em palavra minuscula e removendo os sinais de pontuação
            if palavra != '' and palavra not in lista_stop_words:
                lista_de_palavras.append(palavra) 
                lista_de_palavras.append(int(linha[0])) #[palavra, escore, palavra2, escore2,...]
    del palavras_separadas #deletando listas inúteis para não consumir muita memória
    for palavra in lista_de_palavras : 
        if palavra in lista_de_palavras : #verifica se o item já estava na lista
            if palavra not in intervalo: #serve para receber só as palavras, e não os valores dos sentimentos
                lista_de_escores = [] #zera a lista a cada iteração
                frequencia = lista_de_palavras.count(palavra) #conta todas as ocorrÊncias da plavra na lista
                i=0
                while i < frequencia: 
                    sentimento = lista_de_palavras[(lista_de_palavras.index(palavra)+1)] #guarda o valor do index sucessor da palavra, já que lista_de_palavras == [palavra, escore, palavra2, escore2...]
                    lista_de_escores.append(sentimento)
                    lista_de_palavras.remove(palavra) #garante que quando entrar no laço novamente, a ocorrência analisada será a proxima da lista, e não a primeira
                    i = i+1
                escore = sum(lista_de_escores)/frequencia #divide a soma de todos os sentimentos da plavra pela frequencia
                words[palavra] = (frequencia, escore) #words == {palavra: (frequencia, escore), palavra2: (frequencia2, escore2)}
            sentimento = 0
            frequencia = 0
    del lista_de_palavras   
    return words

def readTestSet(fname):
    ''' Esta funcao le o arquivo contendo o conjunto de teste
	    retorna um vetor/lista de pares (escore,texto) dos
	    comentarios presentes no arquivo.
    '''    
    reviews = None
    comentario = []
    testSet = open(fname,"r")
    lista_testSet = testSet.readlines()
    reviews2 = [] #[(3 --> escore, 'Frase maiuscula e com sinais de pontuacao .\t\n'), (1, 'Blabla .\t\n'), ...]
    reviews = [] # [(3, ['frase, 'minuscula', 'e', 'sem', 'sinais', 'de', 'pontuacao', '', '']), (1, ['Blabla', '', ''])]
    for linha in lista_testSet :
        reviews2.append((int(linha[0]), linha[2:])) #guarda o escore (posicao 0) e o comentario na lista
    for tupla in reviews2 :
        palavras_separadas = list(split_on_separators(tupla[1]," ")) #
        for palavra in palavras_separadas:
            palavra = clean_up(palavra)
            if palavra != '' :
                comentario.append(palavra)
        reviews.append((int(tupla[0]), comentario))
        comentario = []
    return reviews
def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario é a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore é 2.
        Review é a parte textual de um comentario.
        Words é o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    score = 0.0
    count = 0
    lista_de_escores = []
    frase = review[1] #recebe a parte textual do review
    count = len(review[1])
    for palavra in frase : 
        if palavra not in words.keys() : #verifica se palavra estava no conjunto de treinamento
            escore = 2 
            lista_de_escores.append(escore) #adiciona esse escore numa lista
        else :
            escore = words[palavra][1] # words['palavra'] == (frequencia, escore <-- posicao1) . Recebe o escore do conj de treinamento
            lista_de_escores.append(escore) 
    score = sum(lista_de_escores) #soma todos os escores da lista de escores desse comentario

    return score/count

def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario é obtido com a
        funcao computeSentiment. 
        Reviews é um vetor de pares (escore,texto)
        Words é um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    ''' 
    sse = 0 #escrito pelo professor
    total_diferenca = 0
    for comentario in reviews :
        sentimento = computeSentiment(comentario, words)#chama a função que retorna o sentimento do comentario
        escore_real = comentario[0] #guarda o escore real do comentário do conj de teste
        diferenca = sentimento - escore_real
        quadrado_dos_erros = diferenca*diferenca
        total_diferenca = total_diferenca + quadrado_dos_erros
    total_comentarios = len(reviews)
    sse = total_diferenca/total_comentarios
    return sse

def main():
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    words = readTrainingSet(sys.argv[1])

    reviews = readTestSet(sys.argv[2])
    
    sse = computeSumSquaredErrors(reviews,words)
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()
    
