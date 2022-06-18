# Procolo

## Especificar um protocolo e implementar na sua linguagem de programação preferida

Utilizar sockets (com a linguagem de programação de sua preferência) para implementar um programa, com um protocolo de rede especificado por você:

O que desenvolver?
1. Um programa cliente
2. Um programa servidor

O que entregar?
- 1. A especificação do seu protocolo em PDF, deixando claro:

1.1. As operações/comandos/requisições que podem ser enviadas
1.1.1. Os parâmetros de envio e o significado de cada parâmetro
1.1.2. Os códigos de erros definidos e o significado de cada um dos erros, e quando eles podem ocorrer
1.1.3. Quando cada uma das operações/comandos/requisições devem/podem ser enviadas

1.2. O formato das mensagens trafegadas (XML? JSON? Um formato seu próprio?)

O que devo entregar? Coloque o código-fonte num repositório git (ex.: github) e me adicione como colaborador: thiagobrunoms@gmail.com. No dia da apresentação, mostre-me a execução dos programas de forma individual.

Mais detalhes sobre o projeto

- Cliente deve sempre inicializar a comunicação, servidor deve sempre responder a requisições do cliente;
- Desenvolva e especifique um protocolo da camada de aplicação, definindo formato de mensagens e regras para envio e recebimento de mensagens.

Como exemplo (APENAS EXEMPLO!!!!), abaixo segue a especificação de um tipo de protocolo simples:

> Tipos de mensagens/operações etc.
Requisição: Ex1.: mensagens de requisição (operação) podem incluir os seguintes comandos: SAIR, REMOVER, PULAR, ENVIAR, BUSCAR etc., com seus respectivos parâmetros
Resposta: Ex1.: mensagens de resposta podem incluir os seguintes comandos: OK, ERROR etc.

Formato das mensagens: vários formatos podem ser considerados. Abaixo seguem dois exemplos para as mesmas operações/tipos de mensagens. O formato serve para que outros clientes possam seguir essa estrutura no formato correto esperado pelo seu servidor.

Ex.: Mensagem BUSCAR e REMOVER
---- Em JSON:
{"requestId":"5432", “operation”:”buscar”, “key”:”redes de computadores”}
{"requestId":"1199", “operation”:”remover”, “key”:”redes de computadores”}

---- Em XML
<request>
<requestId>5432</requestId>
<operation>buscar</operation>
<key>Redes de Computadores</key>
</request>
//Operação de remover segue o mesmo padrão

---- HTTP-like ("COPIANDO" a ideia do HTTP)
REQUESTID: 5432
OPERATION: buscar
KEY: Redes de Computadores

//Operação de remover segue o mesmo padrão
3. Códigos de erros retornados PELO SERVIDOR e significados: quando algum erro ocorre no lado do servidor, o cliente deve ser informado.

Exemplo de mensagens de erros

1. Usuário não encontrado: o código de erro será 401
---- Em JSON:
{“error”:”401”, “message”:”user not found”, "requestId":5432}

---- Em XML
<response>
<requestId>5432</requestId>
<error>401</error>
<message>User not found</message>
</response>

---- HTTP-like (em HTTP)
REQUESTID: 5432
ERROR: 401
MESSAGE: User not found

2: Comando não disponível: o código de erro será 402
---- Em JSON:
{“error”:”402”, “message”:”Operation unavailable”, "requestId":8787099}
---- Em XML
< response>
<requestId>8787099</requestId>
<error>402</error>
<message>Operation unavailable</message>
</response>
---- HTTP-like (em HTTP)
REQUESTID: 8787099
ERROR: 402
MESSAGE: Operation unavailable

## Tipos de Protocolos

rs: recurso
mt: Método
sc: código status
tm: trás o tempo de criação da resposta
tk: serve pra trafegar token
lu: última atualização
ky: (key) busca por uma chave



