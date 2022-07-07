from bs4 import BeautifulSoup
from datetime import date
import json
import requests

page = 'https://www.bloodstoneonline.com/pt/pontuacao/'
output = {}
counter = 1
today = date.today()

# Loop entre todos os servidores
for world in range(1, 6):
    
    # POST request da URL
    data = {'server': world,
            'vocation': '0',
            'category': '0',
            'submit': 'Filtrar'}

    r = requests.post(url = page, data = data)

    page_source = BeautifulSoup(r.content, 'html.parser') # Código fonte da página
    highscore = page_source.find_all('td') # Buscando todos os resultados com a tag <td> no código fonte]
    
    # Mapeamento de servidores
    if world == 1:
        server = 'Onix'
    elif world == 2:
        server = 'Ruby'
    elif world == 3:
        server = 'Jasper'
    elif world == 4:
        server = 'Gold'
    elif world == 5:
        server = 'Platinum'

    # Loop entre todos os <td> encontrados.
    # O loop é feito com passo 6 pois cada personagem possui 6 colunas de conteúdo
    for i in range(0, len(highscore), 6):
        name = str(highscore[i + 1].text).replace(' ', '_')
        output[name] = {'id': counter, 'name': highscore[i + 1].text, 'vocation': highscore[i + 2].text, 'level': int(highscore[i + 4].text), 'experience': int(highscore[i + 5].text), 'server': server}
        counter += 1

# Salva os dados em um arquivo JSON
with open(str(today) + '.json', 'w') as json_file:
    json.dump(output, json_file, indent=4, ensure_ascii=False)

print(str(today))