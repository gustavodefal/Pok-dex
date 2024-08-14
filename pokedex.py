import tkinter as tk
from PIL import Image, ImageTk
import requests
import json
from io import BytesIO

# Variável global para a imagem do Tkinter
tk_image = None
image_label = None

# Variável global para a imagem do Tkinter
tk_image2 = None
image_label2 = None

# Função de consulta da API
def buscarnaweb():
    request = requests.get(f'https://pokeapi.co/api/v2/pokemon/{nomedopokemon.get().lower()}')
    dados = request.content
    
    json_str = dados.decode('utf-8')
    data = json.loads(json_str)
    
    # URL da imagem
    urlImage = data['sprites']['front_default']
    # URL da imagem shiny
    urlImage2 = data['sprites']['front_shiny']

    # Baixa a imagem
    image = download_image(urlImage)
    # Baixa a imagem shiny
    image2 = download_image(urlImage2)
    
    # Converte as imagens para um formato compatível com o Tkinter
    global tk_image, tk_image2
    tk_image = ImageTk.PhotoImage(image)
    tk_image2 = ImageTk.PhotoImage(image2)
    
    # Atualiza as imagens nos widgets, se eles existirem
    if image_label:
        image_label.config(image=tk_image)
        image_label.image = tk_image
    if image_label2:
        image_label2.config(image=tk_image2)
        image_label2.image = tk_image2
        
    normal_version_label.grid(column=0, row=8, pady=5)  # Mostra o label "Normal Version"
    shiny_version_label.grid(column=2, row=8, pady=5)  # Mostra o label "Shiny Version"


    ability_name = data['abilities'][0]['ability']['name'].title()
    
    # Impede conflito em caso de uma só habilidade
    if len(data['abilities']) > 1:
        hidden_ability = data['abilities'][1]['ability']['name'].title()
    else:
        hidden_ability = ""
    
    name = data['name'].title()
    
    type1 = data['types'][0]['type']['name'].title()
    
    # Impede conflito em caso de um só tipo
    if len(data['types']) > 1:
        type2 = data['types'][1]['type']['name'].title()
        types_text = f'{type1} and {type2}'
    else:
        type2 = ""
        types_text = type1
    
    id = data['id']
    
    # Resultados
    resultado4['text'] = f'Number: {id}'
    resultado2['text'] = f'Name: {name}'
    resultado3['text'] = f'Types: {types_text}'
    resultado['text'] = f'Ability: {ability_name}'
    resultado5['text'] = f'Hidden Ability: {hidden_ability}'
    
    # Tira o texto de hidden ability, caso não haja uma
    if not hidden_ability:
        resultado5['text'] = ""
        
     # Atualiza a eficácia de combate do tipo
    effectiveness = get_type_effectiveness([type1.lower(), type2.lower()])
    fraco_contra['text'] = f'Weak to: {", ".join(effectiveness["double_damage_from"])}'
    forte_contra['text'] = f'Strong against: {", ".join(effectiveness["double_damage_to"])}'

# Função para obter a eficácia de combate do tipo
def get_type_effectiveness(pokemon_types):
    effectiveness = {
        'double_damage_from': [],
        'double_damage_to': []
    }
    
    for type_name in pokemon_types:
        if type_name:
            response = requests.get(f'https://pokeapi.co/api/v2/type/{type_name}')
            if response.status_code != 200:
                continue
            data = response.json()
            effectiveness['double_damage_from'].extend([type_info['name'].title() for type_info in data['damage_relations']['double_damage_from']])
            effectiveness['double_damage_to'].extend([type_info['name'].title() for type_info in data['damage_relations']['double_damage_to']])
    
    return effectiveness

#Fazendo download da imagem para apresentar
def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

#Fazendo download da imagem para apresenta
def download_image2(url2):
    response2 = requests.get(url2)
    return Image.open(BytesIO(response2.content))


# Cria a janela principal
janela = tk.Tk()
janela.title('Pokédex')

# Cria um frame centralizado com fundo vermelho
posicao = tk.Frame(janela, padx=30, pady=30, bg='red')
posicao.grid(row=0, column=0, sticky='nsew')

# Configura a expansão das linhas e colunas
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)
posicao.grid_rowconfigure(0, weight=1)
posicao.grid_columnconfigure(0, weight=1)

# Texto inicial
tk.Label(posicao, text='Insert the name of the Pokémon', bg='red', fg='white', font=('Arial', 12, 'bold')).grid(column=1, row=0, pady=10, sticky='n')

# Input do nome
nomedopokemon = tk.Entry(posicao, bg='white', font=('Arial', 12))
nomedopokemon.grid(column=1, row=1, pady=5, sticky='n')

# Botão de buscar
tk.Button(posicao, text='Search', command=buscarnaweb, bg='white', font=('Arial', 12)).grid(column=1, row=2, pady=10, sticky='n')

# Resultado do número
resultado4 = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
resultado4.grid(column=1, row=3, pady=5, sticky='n')

# Resultado do nome
resultado2 = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
resultado2.grid(column=1, row=4, pady=5, sticky='n')

# Resultado dos tipos
resultado3 = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
resultado3.grid(column=1, row=5, pady=5, sticky='n')

# Resultado da habilidade
resultado = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
resultado.grid(column=1, row=6, pady=5, sticky='n')

# Resultado da habilidade oculta
resultado5 = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
resultado5.grid(column=1, row=7, pady=5, sticky='n')

# Labels para as versões das imagens
normal_version_label = tk.Label(posicao, text='Normal Version', bg='red', fg='white', font=('Arial', 12, 'bold'))
shiny_version_label = tk.Label(posicao, text='Shiny Version', bg='red', fg='white', font=('Arial', 12, 'bold'))

# Widget para exibir a imagem
image_label = tk.Label(posicao)
image_label.grid(column=0, row=9, pady=10)
# Widget para exibir a imagem shiny
image_label2 = tk.Label(posicao)
image_label2.grid(column=2, row=9, pady=10)

# Labels para mostrar as fraquezas e resistências
fraco_contra = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
fraco_contra.grid(column=0, row=10, pady=5, sticky='n')
forte_contra = tk.Label(posicao, bg='red', fg='white', font=('Arial', 12, 'bold'))
forte_contra.grid(column=2, row=10, pady=5, sticky='n')


# Abre a janela
janela.mainloop()