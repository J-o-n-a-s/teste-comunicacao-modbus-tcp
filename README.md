[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

[contributors-shield]: https://img.shields.io/github/contributors/J-o-n-a-s/teste-comunicacao-modbus-tcp.svg?style=for-the-badge
[contributors-url]: https://github.com/J-o-n-a-s/teste-comunicacao-modbus-tcp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/J-o-n-a-s/teste-comunicacao-modbus-tcp.svg?style=for-the-badge
[forks-url]: https://github.com/J-o-n-a-s/teste-comunicacao-modbus-tcp/network/members
[stars-shield]: https://img.shields.io/github/stars/J-o-n-a-s/teste-comunicacao-modbus-tcp.svg?style=for-the-badge
[stars-url]: https://github.com/J-o-n-a-s/teste-comunicacao-modbus-tcp/stargazers
[issues-shield]: https://img.shields.io/github/issues/J-o-n-a-s/teste-comunicacao-modbus-tcp.svg?style=for-the-badge
[issues-url]: https://github.com/J-o-n-a-s/teste-comunicacao-modbus-tcp/issues
[license-shield]: https://img.shields.io/github/license/J-o-n-a-s/teste-comunicacao-modbus-tcp.svg?style=for-the-badge
[license-url]: https://github.com/J-o-n-a-s/teste-comunicacao-modbus-tcp/blob/master/LICENSE

# Programa para teste de comunicação modbus TCP

**SEJA BEM-VINDO A ESTE REPOSITÓRIO!!!**

-------------

**Instruções**

 - *Fork* este repositório;
 - Clone seu repositório *forked*;
 - Adicione seus scripts;
 - *Commit & Push*;
 - Crie um *pull request*;
 - Dê uma estrela para este repositório;
 - Aguarde que o seu *pull request* solicitado vire um *merge*;
 - Comemore, seu primeiro passo para o mundo de código aberto e continue contribuindo.

## Introdução

Esse é um programa criado para realizar testes de comunicação modbus TCP. A ideia inicial foi fazer um programa que pudesse ser configurável e que no final apresentasse alguns dados estatísticos relacionados ao teste que acabou de ser realizado.

## Motivação

Realizar testes em equipamentos com comunicação modbus TCP de forma facilitada e de forma configurável.

## Descrição do projeto

O projeto foi desenvolvido em Python 3.12 realizando o código em arquivos separados como boa prática para facilitar a localização das funções. Está sendo utilizado formatadores de código para garantir a padronização da maneira de escrever os códigos.

Nesta primeira versão, toda a interação com o software é realizada sem interface gráfica. A ideia é o usuário interagir com um menu para selecionar as opções necessária para receber a informação que precisa.

### Bibliotecas e recursos utilizados

 - Time -> Para adição de tempo e registro do início, fim e duração do processo;
 - Tkinter -> Para utilização da caixa de diálogo de seleção de diretório para exportação de arquivo;
 - Textwrap -> Para facilitar a quebra de textos para a impressão
 - Datetime -> Para pegar a data atual do sistema;
 - PyModbus -> Para realização das leituras das variáveis modbus TCP;
 - Pyinstaller -> Para criação do arquivo executável. Facilitando a utilização do programa mesmo em máquinas que não possuem o Python instalado.

### Funcionamento do programa

O programa funciona em modo de prompt informando nome da empresa e um menu com as opções que o usuário pode selecionar. Cada menu válido selecionado apresentará mensagens distintas para seleção e mensagens distintas também para a apresentação final dos dados. É possível visualizar as informações diretamente no prompt ou ainda solicitar que os dados sejam exportados para arquivo do Excel.

Abaixo é mostrada imagem da tela e menu inicial:


Importante salientar que no caso de selecionar que deseja gravar o arquivo no log, será necessário selecionar o caminho onde o arquivo será gravado. O nome dele iniciará com `Log` e será seguido pela data e hora do momento da gravação no formato ano, mês, dia, hora e minuto (`AAAA-MM-DD_HH-MM.csv`).



### Amostra do resultado da execução do programa

A imagem abaixo apresenta o resultado final da execução do programa com a seguinte configuração:

 - IP =
 - Porta =
 - Timeout =
 - Tentativas =
 - Número do escravo =
 - Registro =
 - Quantidade de registros sequênciais =
 - Número de leituras =
 - Tempo entre leituras

![Visualização do resultado final](img/resultado_final.gif)

## Instalação e execução do projeto

 - `pip install poetry` para instalar o gerenciador de pacotes;
 - `poetry install` para que o poetry instale os pacotes usados no projeto;
 - `poetry shell` para que o poetry crie um ambiente virtual;
 - `python src/main.py` para executar o projeto.

## Licença

MIT License
 
