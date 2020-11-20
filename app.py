# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests, json, os, time


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/api/futebol/serie-a/tabela', methods=['GET'])
def tabela_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2020')
    time.sleep(2)
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
            golproObj = lista_numeros[5]
            golcontraObj = lista_numeros[6]
            saldoObj = lista_numeros[7]
            c_amarelo = lista_numeros[8]
            c_vermelho = lista_numeros[9]
            aprovObj = lista_numeros[10]

        data.append({
            'posicao' : posObj.text.strip(),
            'result' : result,
            'escudo' : imgObj['src'],
            'time' : timeObj.text.strip(),
            'pontos' : ptsObj.text.strip(),
            'jogos' : jogObj.text.strip(),
            'vitorias' : vitObj.text.strip(),
            'empates' : empObj.text.strip(),
            'derrotas' :  derObj.text.strip(),
            'gol_pro' : golproObj.text.strip(),
            'gol_contra' : golcontraObj.text.strip(),
            'saldo' : saldoObj.text.strip(),
            'cartao_amarelo' : c_amarelo.text.strip(),
            'cartao_vermelho' : c_vermelho.text.strip(),
            'aproveitamento' : aprovObj.text.strip()
        })
   
    return jsonify({'tabela': data})

@app.route('/api/futebol/serie-a/jogos', methods=['GET'])
def jogos_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2020')
    time.sleep(2)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    container = soup.find('aside', class_='aside-rodadas')
    rodada = container.find('div', class_='swiper-slide active').find('h3', class_='text-center').text
    rodada_ativa = container.find('div', class_='swiper-slide active').find('div', class_='aside-content').find('ul', class_='list-unstyled')
    data = []
    for dataBox in rodada_ativa.find_all('li'):
        jogo = dataBox.find('span', class_='partida-desc text-1 color-lightgray p-b-15 block uppercase text-center').text.strip()
        timeCasaSigla = dataBox.find('div', class_='time pull-left').find('span', class_='time-sigla')
        timeCasaImg = dataBox.find('div', class_='time pull-left').find('img')
        timeForaSigla = dataBox.find('div', class_='time pull-right').find('span', class_='time-sigla')
        timeForaImg = dataBox.find('div', class_='time pull-right').find('img')
        local = dataBox.find('span', class_='partida-desc text-1 color-lightgray block uppercase text-center').text.strip()
        detalhes = dataBox.find('span', class_='partida-desc text-1 color-lightgray block uppercase text-center').find('a')


        if dataBox.find('strong', class_='partida-horario center-block').find('span'):
            placar = dataBox.find('strong', class_='partida-horario center-block').find('span')
            #tratamento divisao de placar do jogo
            timeCasaPlacar = placar.text.split(' x ')[0]
            timeForaPlacar = placar.text.split(' x ')[1]
        else:
            timeCasaPlacar = ''
            timeForaPlacar = ''

        #tratamento do conteudo jogo
        aux = '\r\n'
        jogo = jogo.replace(aux, '')
        aux = '                       1 alteração'
        jogo = jogo.replace(aux, '')
        aux = '                       2 alterações'
        jogo = jogo.replace(aux, '')
        aux = '                          '
        jogo = jogo.replace(aux, '')

        #tratamento do conteudo local
        aux = '\nDetalhes do jogo'
        local = local.replace(aux, '')
        aux = '\nComo foi o jogo'
        local = local.replace(aux, '')

        data.append({
            'jogo' : jogo,
            'sigla_time_casa' : timeCasaSigla.text.strip(),
            'escudo_time_casa' : timeCasaImg['src'],
            'sigla_time_fora' : timeForaSigla.text.strip(),
            'escudo_time_fora' : timeForaImg['src'],
            'placar_time_casa' : timeCasaPlacar,
            'placar_time_fora' : timeForaPlacar,
            'local' : local,
            'detalhes' : detalhes['href']
        })

    return jsonify({'rodada': rodada,
                    'jogos': data})

@app.route('/api/futebol/serie-a/noticias', methods=['GET'])
def noticias_brasileirao():
    html_doc = requests.get('https://www.cbf.com.br/futebol-brasileiro/noticias/campeonato-brasileiro-serie-a')
    time.sleep(2)
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    data = []
    for dataBox in soup.find_all('div', class_='news col-md-12 news-type-2 has-overlay'):
        titulo = dataBox.find('div').find('span', class_='text-2 block m-b-5')
        imagem = dataBox.find('img')
        noticia = dataBox.find('h2', class_='news-title m-b-15 hidden-xs hidden-sm').find('a')
        conteudo = dataBox.find('p', class_='news-desc m-b-10').find('a')
        tempo = dataBox.find('span', class_='text-1')

        data.append({
            'titulo' : titulo.text.strip(),
            'imagem' : imagem['src'],
            'noticia' : noticia.text.strip(),
            'conteudo' : conteudo.text.strip(),
            'tempo' : tempo.text.strip()
        })
    
    return jsonify({'noticias': data})

#app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
