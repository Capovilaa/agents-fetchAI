Projeto criado para estudos gerais sobre agentes Fetch.AI

cd\uAgents
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt

-----------------------------------------------------------------------------------------------------------
Lógica que foi possível entender até agora:

1° Devemos realizar os imports necessários

por padrão de uagents devemos importar Agent para criar um agente e
Context para conseguir realizar algumas funções

outras bibliotecas podem ser importadas, isso vai depender
do caso de uso do código


2° Devemos criar a estrutura das mensagens com o class Model,

esse que vai permitir definirmos qual o tipo de mensagem aceito

podem ser criados mais de uma estrutura de mensagem

isso será levado em conta para saber qual função deve ser
chamada com base nos parâmetros recebidos quando comparados
aos Models


3° Devemos criar os agentes

criação dos agentes devem ser feitos com a class Agent, que
foi importada no início


caso seja necessário, também podemos fazer algumas funções e 
lógicas fora dos comportamentos


4° Devemos criar os comportamentos dos agentes e quando eles vão ocorrer

assim que quisermos, podemos usar @agent para definir uma função
que será chamada assim que um intervalo, mensagem etc for definido

esses comportamentos vão variar de acordo com cada Model criado, sendo
possível criar toda a lógica com isso

a função que será executada deve ser do tipo assíncrona, para que
todas as etapas sejam finalizadas por completo

nos parâmetros da função, devemos passar ctx : Context para ter acesso às
funções, sender : str para ver quem mandou a mensagem, msg : TipoMensageDefinido
para ver qual foi a mensagem que foi recebida

toda lógica do que vai acontecer quando a mensagem for recebida ou pelo intervalo
definido, deve ser codificada dentro da função

mais de um comportamento pode ser criado por agente


5° Devemos criar bureau (caso seja necessário)

isso permite que mais de 1 agente seja executado por arquivo ao
mesmo tempo

criamos e adicionamos os agentes necessários

chamamos bureau.run() no main do arquivo
