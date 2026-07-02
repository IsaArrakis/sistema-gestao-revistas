# Sistema de Revistas

## Visao geral

Esta aplicacao e um sistema web simples feito com Flask para controle de revistas, estoque, vendas e visualizacao de indicadores em um painel BI.

O projeto usa a estrutura MVC de forma simples:

- Model: conexao e criacao do banco em `app/models/db.py`.
- Controllers: rotas e regras de negocio em `app/controllers/`.
- Views: telas HTML em `app/views/`.

O banco de dados usado e SQLite, salvo no arquivo `sistema_revistas.db`, localizado na raiz do projeto.

## Tecnologias usadas

- Python
- Flask
- SQLite
- bcrypt
- HTML
- CSS inline dentro dos templates
- Jinja2, por meio do Flask, para renderizar dados nas paginas HTML

As dependencias externas estao em `requirements.txt`:

```txt
Flask==3.0.3
bcrypt==4.1.3
```

## Como executar

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute a aplicacao:

```bash
python run.py
```

Ao iniciar, o Flask sobe o servidor em modo debug por causa de:

```python
app.run(debug=True)
```

Normalmente a aplicacao fica disponivel em:

```txt
http://127.0.0.1:5000
```

## Estrutura de arquivos

```txt
sistema_revistas/
├── app/
│   ├── controllers/
│   │   ├── auth.py
│   │   ├── bi_ctrl.py
│   │   ├── cadastrar_novo.py
│   │   ├── revista_ctrl.py
│   │   └── venda_ctrl.py
│   ├── models/
│   │   └── db.py
│   ├── views/
│   │   ├── bi.html
│   │   ├── editar_revista.html
│   │   ├── login.html
│   │   ├── nova_revista.html
│   │   ├── nova_venda.html
│   │   └── revistas.html
│   └── __init__.py
├── DOCUMENTACAO.md
├── requirements.txt
├── run.py
└── sistema_revistas.db
```

## Arquivo `run.py`

Este e o ponto de entrada da aplicacao.

Ele importa a funcao `create_app()` do pacote `app`, cria a instancia Flask e executa o servidor:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

## Arquivo `app/__init__.py`

Este arquivo cria e configura a aplicacao Flask.

Responsabilidades:

- Criar o objeto `Flask`.
- Definir a pasta de templates como `views`.
- Definir a `secret_key`, usada pela sessao do Flask.
- Importar os Blueprints dos controllers.
- Registrar as rotas dos Blueprints.
- Redirecionar a rota raiz `/` para a tela de login.

Blueprints registrados:

- `auth_bp`, de `auth.py`
- `revista_bp`, de `revista_ctrl.py`
- `venda_bp`, de `venda_ctrl.py`
- `bi_bp`, de `bi_ctrl.py`

## Banco de dados `sistema_revistas.db`

O arquivo `sistema_revistas.db` e o banco SQLite da aplicacao.

Ele guarda os dados reais do sistema:

- Funcionarios
- Senhas criptografadas
- Clientes
- Revistas
- Estoque
- Vendas
- Dados usados pelo painel BI

SQLite funciona em arquivo local. Por isso, o projeto nao precisa de um servidor MySQL, PostgreSQL ou SQL Server.

## Arquivo `app/models/db.py`

Este arquivo centraliza a conexao com o banco.

Principais responsabilidades:

- Montar o caminho absoluto para `sistema_revistas.db`.
- Abrir conexao SQLite.
- Ativar suporte a chaves estrangeiras.
- Configurar retorno das consultas como `sqlite3.Row`.
- Criar as tabelas se ainda nao existirem.
- Inserir dados iniciais se a tabela `FUNCIONARIO` ainda nao existir.

### Caminho do banco

O caminho e definido assim:

```python
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'sistema_revistas.db')
```

Isso faz o banco ser localizado na raiz do projeto, mesmo que o codigo seja executado a partir de outro diretorio.

### Conexao com SQLite

A funcao principal e:

```python
get_db_connection()
```

Ela retorna uma conexao pronta para uso.

Caracteristicas importantes:

- `sqlite3.connect(DB_PATH)` abre o banco.
- `conn.row_factory = sqlite3.Row` permite acessar colunas por nome, como `revista['preco']`.
- `PRAGMA foreign_keys = ON` ativa validacao de relacionamentos.
- Se a tabela `FUNCIONARIO` nao existir, o sistema cria todas as tabelas e insere dados iniciais.

## Tabelas do banco

### `FUNCIONARIO`

Guarda usuarios do sistema.

Campos:

| Campo | Tipo | Descricao |
|---|---|---|
| `id_funcionario` | INTEGER PRIMARY KEY AUTOINCREMENT | Identificador automatico |
| `cpf` | TEXT NOT NULL UNIQUE | CPF usado no login |
| `senha` | TEXT NOT NULL | Senha criptografada com bcrypt |
| `nome_funcionario` | TEXT NOT NULL | Nome do funcionario |
| `cargo` | TEXT NOT NULL | Define permissao, como Administrador ou Vendedor |

### `CLIENTE`

Guarda clientes.

Campos:

| Campo | Tipo | Descricao |
|---|---|---|
| `id_cliente` | INTEGER PRIMARY KEY AUTOINCREMENT | Identificador automatico |
| `nome_cliente` | TEXT NOT NULL | Nome do cliente |
| `cpf` | TEXT NOT NULL | CPF do cliente |

O sistema usa um cliente padrao chamado `Cliente Balcao`, com `id_cliente = 1`.

### `REVISTA`

Guarda o catalogo e estoque de revistas.

Campos:

| Campo | Tipo | Descricao |
|---|---|---|
| `id_revista` | INTEGER PRIMARY KEY | Codigo da revista |
| `nome_revista` | TEXT NOT NULL | Nome da revista |
| `quantidade_em_estoque` | INTEGER NOT NULL DEFAULT 0 | Estoque atual |
| `preco` | REAL NOT NULL DEFAULT 0.0 | Preco unitario |

### `VENDA`

Guarda vendas realizadas.

Campos:

| Campo | Tipo | Descricao |
|---|---|---|
| `id_venda` | INTEGER PRIMARY KEY | Codigo da venda |
| `data_da_venda` | TEXT NOT NULL | Data em formato ISO |
| `forma_de_pagamento` | TEXT NOT NULL | Dinheiro, PIX ou Cartao |
| `preco_total` | REAL NOT NULL | Total da venda |
| `id_cliente` | INTEGER | Referencia `CLIENTE.id_cliente` |
| `id_funcionario` | INTEGER | Referencia `FUNCIONARIO.id_funcionario` |
| `id_revista` | INTEGER | Referencia `REVISTA.id_revista` |

## Dados iniciais

Quando o banco ainda nao possui a tabela `FUNCIONARIO`, o sistema cria dados iniciais.

Funcionarios:

| CPF | Senha | Nome | Cargo |
|---|---|---|---|
| `11111111111` | `admin123` | Ana Administradora | Administrador |
| `22222222222` | `user123` | Bruno Vendedor | Vendedor |

Revistas iniciais:

| ID | Revista | Estoque | Preco |
|---|---|---:|---:|
| 1 | Veja | 50 | 15.90 |
| 2 | Superinteressante | 30 | 12.50 |
| 3 | National Geographic | 20 | 18.00 |
| 4 | Mundo Estranho | 40 | 9.90 |
| 5 | Epoca Negocios | 25 | 22.00 |

## Autenticacao

Arquivo responsavel:

```txt
app/controllers/auth.py
```

Rotas:

| Rota | Metodo | Funcao |
|---|---|---|
| `/login` | GET | Exibe tela de login |
| `/login` | POST | Valida CPF e senha |
| `/logout` | GET | Limpa a sessao e volta para login |

Fluxo do login:

1. Usuario informa CPF e senha.
2. O sistema busca o funcionario pelo CPF.
3. A senha digitada e comparada com o hash salvo no banco usando `bcrypt.checkpw`.
4. Se estiver correta, o sistema salva na sessao:
   - `id_funcionario`
   - `nome`
   - `cargo`
5. O usuario e redirecionado para `/revistas`.

A busca do funcionario usa parametro SQL:

```sql
SELECT * FROM FUNCIONARIO WHERE cpf = ?
```

Isso evita concatenacao direta de valores na query.

## Controle de acesso

O sistema usa a sessao do Flask para controlar acesso.

Para acessar paginas internas, normalmente existe uma verificacao:

```python
if 'id_funcionario' not in session:
    return redirect(url_for('auth.login'))
```

Para acoes administrativas, existe verificacao de cargo:

```python
if session.get('cargo') != 'Administrador':
    return "Acesso Negado", 403
```

O usuario com cargo `Administrador` pode:

- Cadastrar revistas
- Editar revistas
- Excluir revistas
- Registrar vendas
- Acessar o painel BI

O usuario comum consegue acessar o catalogo, mas nao ve os botoes administrativos.

## Controller de revistas

Arquivo:

```txt
app/controllers/revista_ctrl.py
```

Responsabilidades:

- Listar revistas.
- Cadastrar nova revista.
- Editar revista existente.
- Excluir revista.
- Proteger rotas que exigem login.
- Bloquear acoes administrativas para usuarios que nao sejam administradores.

Rotas:

| Rota | Metodo | Funcao |
|---|---|---|
| `/revistas` | GET | Lista revistas |
| `/revistas/nova` | GET | Exibe formulario de cadastro |
| `/revistas/nova` | POST | Salva nova revista |
| `/revistas/editar/<id_revista>` | GET | Exibe formulario de edicao |
| `/revistas/editar/<id_revista>` | POST | Atualiza revista |
| `/revistas/excluir/<id_revista>` | GET | Exclui revista |

### Listagem

Consulta usada:

```sql
SELECT * FROM REVISTA
```

Retorna todas as revistas cadastradas.

### Cadastro

Comando usado:

```sql
INSERT INTO REVISTA (id_revista, nome_revista, quantidade_em_estoque, preco)
VALUES (?, ?, ?, ?)
```

Os valores vem do formulario `nova_revista.html`.

### Edicao

Comando usado:

```sql
UPDATE REVISTA
SET nome_revista = ?, quantidade_em_estoque = ?, preco = ?
WHERE id_revista = ?
```

O formulario `editar_revista.html` carrega a revista pelo ID e envia os novos valores.

### Exclusao

Comando usado:

```sql
DELETE FROM REVISTA WHERE id_revista = ?
```

Como `VENDA.id_revista` referencia `REVISTA.id_revista`, uma revista que ja possui venda registrada pode causar erro de integridade. O codigo captura excecao, desfaz a transacao com `rollback()` e exibe uma mensagem de bloqueio.

## Controller de vendas

Arquivo:

```txt
app/controllers/venda_ctrl.py
```

Rota:

| Rota | Metodo | Funcao |
|---|---|---|
| `/vendas/nova` | GET | Exibe formulario de venda |
| `/vendas/nova` | POST | Registra venda e baixa estoque |

Fluxo da venda:

1. Verifica se o usuario esta logado.
2. Verifica se o usuario e Administrador.
3. Carrega revistas com estoque maior que zero.
4. No POST, recebe:
   - `id_revista`
   - `quantidade`
   - `pagamento`
5. Garante que o cliente padrao existe.
6. Busca preco e estoque da revista.
7. Verifica se ha estoque suficiente.
8. Calcula `preco_total`.
9. Gera um `id_venda` aleatorio entre 10000 e 99999.
10. Insere a venda.
11. Atualiza o estoque da revista.
12. Confirma tudo com `commit()`.

Consultas principais:

```sql
SELECT id_cliente FROM CLIENTE WHERE id_cliente = 1
```

```sql
INSERT INTO CLIENTE (id_cliente, nome_cliente, cpf)
VALUES (1, 'Cliente Balcao', '00000000000')
```

```sql
SELECT preco, quantidade_em_estoque
FROM REVISTA
WHERE id_revista = ?
```

```sql
INSERT INTO VENDA (
    id_venda,
    data_da_venda,
    forma_de_pagamento,
    preco_total,
    id_cliente,
    id_funcionario,
    id_revista
)
VALUES (?, ?, ?, ?, ?, ?, ?)
```

```sql
UPDATE REVISTA
SET quantidade_em_estoque = quantidade_em_estoque - ?
WHERE id_revista = ?
```

Caracteristica importante: a venda e a baixa de estoque acontecem dentro do mesmo bloco com `try`. Se der erro, o sistema chama `conn.rollback()`.

## Controller do painel BI

Arquivo:

```txt
app/controllers/bi_ctrl.py
```

Rota:

| Rota | Metodo | Funcao |
|---|---|---|
| `/bi` | GET | Exibe indicadores gerenciais |

O painel BI so pode ser acessado por Administradores.

Indicadores calculados:

- Total de unidades em estoque.
- Faturamento total.
- Faturamento agrupado por revista.

Consultas usadas:

```sql
SELECT SUM(quantidade_em_estoque) as total
FROM REVISTA
```

```sql
SELECT SUM(preco_total) as faturamento
FROM VENDA
```

```sql
SELECT r.nome_revista, SUM(v.preco_total) as faturamento_revista
FROM VENDA v
JOIN REVISTA r ON v.id_revista = r.id_revista
GROUP BY r.id_revista, r.nome_revista
ORDER BY faturamento_revista DESC
```

Esta ultima consulta usa:

- `JOIN` para relacionar vendas com revistas.
- `SUM` para somar o faturamento por revista.
- `GROUP BY` para agrupar por revista.
- `ORDER BY DESC` para mostrar primeiro as revistas com maior faturamento.

## Arquivo `app/controllers/cadastrar_novo.py`

Este arquivo parece ser um script auxiliar para cadastrar um funcionario manualmente.

Ele:

- Define CPF, senha, nome e cargo.
- Gera hash da senha com bcrypt.
- Tenta inserir o funcionario no banco.

Ponto importante: o restante do projeto usa SQLite, que trabalha com placeholders `?`. Este arquivo usa `%s`:

```sql
INSERT INTO FUNCIONARIO (cpf, senha, nome_funcionario, cargo)
VALUES (%s, %s, %s, %s)
```

Esse formato e comum em MySQL, mas nao e o padrao do `sqlite3` usado no projeto. Para SQLite, o correto seria:

```sql
INSERT INTO FUNCIONARIO (cpf, senha, nome_funcionario, cargo)
VALUES (?, ?, ?, ?)
```

## Views

As views ficam em:

```txt
app/views/
```

O Flask foi configurado com:

```python
Flask(__name__, template_folder='views')
```

Por isso, chamadas como:

```python
render_template('login.html')
```

procuram os arquivos dentro de `app/views/`.

### `login.html`

Tela de login.

Contem:

- Campo de CPF.
- Campo de senha.
- Botao de entrada.
- Exibicao de erro quando o login falha.

Formulario:

```html
<form action="/login" method="POST">
```

### `revistas.html`

Tela principal do catalogo.

Mostra:

- Nome e cargo do usuario logado.
- Lista de revistas.
- Estoque.
- Preco.
- Botoes administrativos, se o usuario for Administrador.

Usa Jinja2 para percorrer revistas:

```jinja2
{% for revista in revistas %}
```

Tambem usa condicional para exibir acoes somente para Administrador:

```jinja2
{% if session['cargo'] == 'Administrador' %}
```

### `nova_revista.html`

Formulario para cadastrar revista.

Campos:

- ID da revista.
- Nome.
- Quantidade em estoque.
- Preco.

Envia POST para:

```txt
/revistas/nova
```

### `editar_revista.html`

Formulario para editar revista existente.

Carrega os valores atuais da revista e envia POST para:

```txt
/revistas/editar/<id_revista>
```

### `nova_venda.html`

Formulario para registrar venda.

Campos:

- Revista.
- Quantidade.
- Forma de pagamento.

As revistas exibidas no select sao carregadas do banco, filtradas por estoque maior que zero.

### `bi.html`

Tela gerencial.

Mostra:

- Total em estoque.
- Faturamento total.
- Tabela de faturamento por revista.

Recebe do controller:

- `dados`
- `detalhes`

## Caracteristicas das execucoes SQL

### Uso de parametros

A maior parte das consultas usa parametros com `?`, que e o formato correto para `sqlite3`.

Exemplo:

```python
cursor.execute("SELECT * FROM FUNCIONARIO WHERE cpf = ?", (cpf,))
```

Isso e melhor do que montar SQL com concatenacao de strings, porque reduz risco de SQL Injection.

### Transacoes

Operacoes que alteram dados chamam:

```python
conn.commit()
```

Isso grava definitivamente as mudancas.

Quando ha erro em exclusao ou venda, o codigo usa:

```python
conn.rollback()
```

Isso desfaz alteracoes pendentes naquela transacao.

### Chaves estrangeiras

O SQLite so aplica chaves estrangeiras se elas forem ativadas por conexao:

```sql
PRAGMA foreign_keys = ON
```

O projeto faz isso dentro de `get_db_connection()`.

As chaves estrangeiras aparecem na tabela `VENDA`:

```sql
FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente)
FOREIGN KEY (id_funcionario) REFERENCES FUNCIONARIO(id_funcionario)
FOREIGN KEY (id_revista) REFERENCES REVISTA(id_revista)
```

### Criacao automatica de tabelas

Ao abrir conexao, o sistema verifica se a tabela `FUNCIONARIO` existe:

```sql
SELECT name
FROM sqlite_master
WHERE type='table' AND name='FUNCIONARIO'
```

Se nao existir, chama:

- `_criar_tabelas(conn)`
- `_inserir_dados_iniciais(conn)`

### Retorno por nome de coluna

Por causa de:

```python
conn.row_factory = sqlite3.Row
```

o codigo consegue acessar resultados assim:

```python
funcionario['senha']
revista['quantidade_em_estoque']
```

Sem isso, o SQLite retornaria tuplas acessadas por indice.

## Fluxo principal da aplicacao

1. Usuario acessa `/`.
2. O Flask redireciona para `/login`.
3. Usuario faz login com CPF e senha.
4. Se o login for valido, vai para `/revistas`.
5. Na tela de revistas:
   - Usuario comum visualiza o catalogo.
   - Administrador pode cadastrar, editar, excluir, vender e acessar BI.
6. Ao registrar venda:
   - Sistema verifica estoque.
   - Cria registro em `VENDA`.
   - Diminui estoque em `REVISTA`.
7. O painel BI le os dados de `REVISTA` e `VENDA` para gerar indicadores.

## Rotas resumidas

| Rota | Metodo | Controller | Acesso |
|---|---|---|---|
| `/` | GET | `app/__init__.py` | Publico, redireciona |
| `/login` | GET/POST | `auth.py` | Publico |
| `/logout` | GET | `auth.py` | Usuario logado |
| `/revistas` | GET | `revista_ctrl.py` | Usuario logado |
| `/revistas/nova` | GET/POST | `revista_ctrl.py` | Administrador |
| `/revistas/editar/<id>` | GET/POST | `revista_ctrl.py` | Administrador |
| `/revistas/excluir/<id>` | GET | `revista_ctrl.py` | Administrador |
| `/vendas/nova` | GET/POST | `venda_ctrl.py` | Administrador |
| `/bi` | GET | `bi_ctrl.py` | Administrador |

## Observacoes importantes

- O projeto usa SQLite local, entao o arquivo `sistema_revistas.db` contem os dados da aplicacao.
- Se o arquivo `.db` for apagado, os dados atuais sao perdidos, mas o sistema pode recriar as tabelas e os dados iniciais.
- As senhas sao armazenadas com hash bcrypt, nao em texto puro.
- A `secret_key` esta fixa no codigo, o que funciona para estudo, mas nao e ideal para producao.
- O ID de venda e gerado com `random.randint(10000, 99999)`, entao existe possibilidade de colisao caso o numero ja exista.
- O projeto nao possui testes automatizados.
- O projeto nao possui `.gitignore`; normalmente seria recomendado ignorar `__pycache__/` e `*.pyc`.

