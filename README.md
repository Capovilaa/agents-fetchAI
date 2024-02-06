# uAgent

Projeto criado para estudos gerais sobre agentes fetch.

## Instalação

```bash
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
```

## Uso

```python
python .\cleaning_demo\user.py
```

## Lógica que foi possível entender até agora:

## Devemos realizar os imports necessários

Por padrão de uagents devemos importar Agent para criar um agente e
Context para conseguir realizar algumas funções.

Outras bibliotecas podem ser importadas, isso vai depender
do caso de uso do código.



## Devemos criar a estrutura das mensagens com o class Model

Esse que vai permitir definirmos qual o tipo de mensagem aceito.

Podem ser criados mais de uma estrutura de mensagem.

Isso será levado em conta para saber qual função deve ser
chamada com base nos parâmetros recebidos quando comparados
aos Models.



## Devemos criar os agentes

Criação dos agentes devem ser feitos com a class Agent, que
foi importada no início.


Caso seja necessário, também podemos fazer algumas funções e 
lógicas fora dos comportamentos.


## Devemos criar os comportamentos dos agentes e quando eles vão ocorrer

Assim que quisermos, podemos usar @agent para definir uma função
que será chamada assim que um intervalo, mensagem etc for definido.

Esses comportamentos vão variar de acordo com cada Model criado, sendo
possível criar toda a lógica com isso.

A função que será executada deve ser do tipo assíncrona, para que
todas as etapas sejam finalizadas por completo.

Nos parâmetros da função, devemos passar ctx : Context para ter acesso às funções, sender : str para ver quem mandou a mensagem, msg : TipoMensageDefinido
para ver qual foi a mensagem que foi recebida.

Toda lógica do que vai acontecer quando a mensagem for recebida ou pelo intervalo
definido, deve ser codificada dentro da função.

Mais de um comportamento pode ser criado por agente.



## Devemos criar bureau (caso seja necessário)

Isso permite que mais de 1 agente seja executado por arquivo ao
mesmo tempo.

Criamos e adicionamos os agentes necessários.

Chamamos bureau.run() no main do arquivo.

## Baseamento para desenvolvimento

[fetch.ia](https://fetch.ai/docs/guides/agents/installing-uagent)
