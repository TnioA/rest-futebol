# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/futebol/serie-a/tabela', methods=['GET'])
def tabela_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a')
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    data = []
    lista_numeros = []
    for dataBox in soup.find_all('tr', class_="expand-trigger"):
        posObj = dataBox.find('b', class_='m-l-10')
        if '{}'.format('sobe' in str(posObj)) == 'True':
            result = 'sobe'
        elif '{}'.format('desce' in str(posObj)) == 'True':
            result = 'desce'
        else:
            result = 'mantem'
        imgObj = dataBox.find('img', class_='icon escudo m-r-10')
        timeObj = dataBox.find('span', class_='hidden-xs')
        ptsObj = dataBox.find('th', scope='row')
        lista_numeros = dataBox.find_all('td')
        for loop in range(4):
            jogObj = lista_numeros[1]
            vitObj = lista_numeros[2]
            empObj = lista_numeros[3]
            derObj = lista_numeros[4]

        data.append({'posicao' : posObj.text.strip(),
                    'result' : result,
                    'escudo' : imgObj['src'],
                    'time' : timeObj.text.strip(),
                    'pontos' : ptsObj.text.strip(),
                    'jogos' : jogObj.text.strip(),
                    'vitorias' : vitObj.text.strip(),
                    'empates' : empObj.text.strip(),
                    'derrotas' :  derObj.text.strip()})
   
    return jsonify({'tabela': data})



@app.route('/api/futebol/serie-a/jogos', methods=['GET'])
def jogos_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a')
    soup = BeautifulSoup(html_doc.text, 'html.parser')


    rodada = soup.find('h3', class_='text-center').text
    container = soup.find('div', class_='aside-content').find('ul', class_='list-unstyled')
    data = []
    for dataBox in container.find_all('li'):
        jogo = dataBox.find('span', class_='partida-desc text-1 color-lightgray p-b-15 block uppercase text-center').text.strip()
        timeCasaSigla = dataBox.find('div', class_='time pull-left').find('span', class_='time-sigla')
        timeCasaImg = dataBox.find('div', class_='time pull-left').find('img')
        timeForaSigla = dataBox.find('div', class_='time pull-right').find('span', class_='time-sigla')
        timeForaImg = dataBox.find('div', class_='time pull-right').find('img')
        descricao = dataBox.find('span', class_='partida-desc text-1 color-lightgray block uppercase text-center').text.strip()
        detalhes = dataBox.find('span', class_='partida-desc text-1 color-lightgray block uppercase text-center').find('a')

        #tratamento do conteudo jogo
        aux = '\r\n'
        jogo = jogo.replace(aux, '')

        aux = '                          '
        jogo = jogo.replace(aux, '')

        #tratamento do conteudo descricao
        aux = '\nDetalhes do jogo'
        descricao = descricao.replace(aux, '')

        data.append({'jogo' : jogo,
                    'sigla_time_casa' : timeCasaSigla.text.strip(),
                    'escudo_time_casa' : timeCasaImg['src'],
                    'sigla_time_fora' : timeForaSigla.text.strip(),
                    'escudo_time_fora' : timeForaImg['src'],
                    'descricao' : descricao,
                    'detalhes' : detalhes['href']})

    return jsonify({'rodada': rodada,
                    'jogos': data})



@app.route('/api/futebol/serie-a/noticias', methods=['GET'])
def noticias_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/noticias/campeonato-brasileiro-serie-a')
    soup = BeautifulSoup(html_doc.text, 'html.parser')


    data = []
    for dataBox in soup.find_all('div', class_='news col-md-12 news-type-2 has-overlay'):
        titulo = dataBox.find('div').find('span', class_='text-2')
        imagem = dataBox.find('img')
        noticia = dataBox.find('h2', class_='news-title m-t-5 m-b-15 hidden-xs hidden-sm').find('a')
        conteudo = dataBox.find('p', class_='news-desc m-b-10').find('a')

        data.append({'titulo' : titulo.text.strip(),
                    'imagem' : imagem['src'],
                    'noticia' : noticia.text.strip(),
                    'conteudo' : conteudo.text.strip()})
    
    return jsonify({'noticias': data})

#app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)