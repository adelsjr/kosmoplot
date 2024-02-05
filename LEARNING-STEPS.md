### Objetivo 3
#### Refatorar o código existente, implementando Clean Code
- Espera-se que a maioria da codebase siga princípios estabelecidos de Clean Code e Design Patterns
- Espera-se que a codebase siga o PEP8 Style Guide
- Espera-se que o refactor seja explicado via Pull Request

1. **config**
   1. ✅ Refatorando a parte de config para que o app suporte várias fontes de dados. 
   2. ⏳ Adicionar try catch e tratar erros na validação do arquivo de configuração
   3. ⏳ Testes

### Objetivo 2 :heavy_check_mark:

##### Plotar a distância em anos luz das estrelas num gráfico 3D
#### Resultado
![](./assets/img/orion-3D.gif)

- Espera-se que o gráfico tenha 3 dimensões, sendo a dimensão `distance_light_year` utilizada para representar a distancia da estrela no eixo Z.
- Para facilitar a visialização, estrelas de magnitude maior (visíveis a olho nu) seja na cor azul e maiores e as não visíveis, na cor preta e menores e com um nível de transparência maior.

### Dificuldades:
1. Eixo Z (distance) quebrando a visualização da constelação

###  Objetivo 1 :heavy_check_mark:

##### Plotar a constelação num gráfico 2D usando o parametro `declination` e `right_ascention`

#### Resultado
![](./assets/img/orion-2D.png)

- Espera-se: que o gráfico represente o formato da constelação.
  - Passo 1: coletar os dados das estrelas de uma constelação na API, lidando com a paginação :check:
  - Passo 2: plotar os dados dos graus das estrelas com magnitude aparente alta (visíveis a olho nu) num gráfico 2D. :check:
- Melhorias:
  - colorir e mudar o tamanho das estrelas de acordo com sua magnitude
  - explorar mais as annotations
  - traçar linhas das constelações

### dificuldades
1. lidar com a paginação no site que fornece os dados via api. É preciso aprender a lidar com o parametro `offset`
   - Me matei aqui não entendendo como devereia o client gerenciar as requisições, incrementando o `offset` sendo que, neste caso, não existia a informação de total de páginas ou elementos no `response`.
     - posso muito bem fazer X requisições, incrementando o `offset` dentro de um `loop` e parando caso os dados retornem vazios, mas é uma **request a mais**, desnecessária e com o design feio. (Assim que foi feito!)
     - foi quando cheguei nesta pergunta: https://pt.stackoverflow.com/questions/197855/qual-a-forma-correta-de-passar-os-dados-de-pagina%C3%A7%C3%A3o-no-response-rest
       - resumindo, a API deveria me retornar headers ou informações no body de quantidade de elementos / páginas.
     - **conclusão**: utilizar o padrão HATEOS para facilitar a vida de quem for consumir a API, o que obviamente não foi o caso do (https://api-ninjas.com/api/stars)
2. Trabalhar com o tipo de dados correto para plotar o gráfico no matplotlib
   - Os dados utilizados para montar o gráfico 2D das constelações são: `right_ascension` e `declination`. Ambos vem da API num formato que não são compatíveis com o matplotlib
     - ~~foi necessário usar a lib `astropy.units` para converter os valores de graus *hora, minuto, segundo* para graus *decimal* ~~
     - os dados são compatíveis com a lib `astropy.coordinates` usando o método `Coordinates` ele já monta o objeto para ser utilizado no matplotlib. O único problema estava com um caractere, no atributo `declination`.
       - era o `espaço` que estava vindo com o formato unicode que não era compatível com o `Coordinates` do astropy.
         - A solução foi fazer um `replace`: 
        ```python
        i.update({"declination": i["declination"].replace(u"\u00a0", " ")})
        ```
`


