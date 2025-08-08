# Desafio Técnico: Integração e Visualização de Dados com Django

Aplicação web desenvolvida como parte de um desafio técnico para uma vaga de desenvolvedor web. O projeto consiste em consumir dados de fontes externas (API do IBGE e CSV da Receita Federal), persisti-los em um banco de dados PostgreSQL e exibi-los em páginas web com funcionalidades de filtro e paginação.

## Tecnologias Utilizadas

* **Backend:** Python 3, Django
* **Banco de Dados:** PostgreSQL
* **Frontend:** HTML5, CSS3, Bootstrap
* **Bibliotecas Python Principais:**
    * `psycopg2-binary`: Driver de conexão com o PostgreSQL.
    * `requests`: Para consumo da API do IBGE.
    * `django-filter`: Para a funcionalidade de filtros nas listagens.
    * `python-decouple`: Para gerenciamento de variáveis de ambiente.

## Pré-requisitos

* Python 3.8+
* Git
* PostgreSQL instalado e rodando.

## Guia de Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto localmente.

**1. Clone o Repositório:**

```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
cd NOME_DO_REPOSITORIO
```

**2. Crie e Ative o Ambiente Virtual:**

```bash
# Criar ambiente virtual
python -m venv dt_env

# Ativar no Windows
dt_env\Scripts\activate

# Ativar no Linux/macOS
source dt_env/bin/activate
```

**3. Instale as Dependências:**

```bash
pip install -r requirements.txt
```

**4. Configure o Ambiente (Banco de Dados):**

Crie um banco de dados no PostgreSQL para o projeto. Em seguida, configure as credenciais:

* Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
    ```bash
    # No Windows (usando copy)
    copy .env.example .env

    # No Linux/macOS (usando cp)
    cp .env.example .env
    ```
* Abra o arquivo `.env` recém-criado e preencha com as informações do seu banco de dados (nome, usuário, senha, etc.).

**5. Execute as Migrações e Importe os Dados:**

* Aplique as migrações para criar as tabelas no banco:
    ```bash
    python manage.py migrate
    ```
* Execute o script para importar os dados do IBGE (Estados, Municípios, Distritos):
    ```bash
    python manage.py import_ibge_data
    ```
* Para importar os dados das empresas, primeiro baixe o arquivo `EmpresasX.zip` do [site da Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj) e descompacte-o. Em seguida, execute o comando abaixo, substituindo pelo caminho do arquivo CSV:
    ```bash
    python manage.py import_empresas /caminho/para/o/seu/arquivo.EMPRECSV
    ```
    *(Atenção: Este processo pode levar um tempo considerável devido ao tamanho do arquivo.)*

**6. Execute o Projeto:**

* Inicie o servidor de desenvolvimento do Django:
    ```bash
    python manage.py runserver
    ```
* O site estará disponível em `http://127.0.0.1:8000/`.

## Funcionalidades e Acesso

* **Página Inicial:** `http://127.0.0.1:8000/`
* **Listagem de Estados:** `http://127.0.0.1:8000/estados/`
* **Listagem de Municípios:** `http://127.0.0.1:8000/municipios/`
* **Listagem de Distritos:** `http://127.0.0.1:8000/distritos/`
* **Listagem de Empresas:** `http://127.0.0.1:8000/empresas/`

Todas as páginas de listagem possuem filtros por campos relevantes e controles de paginação.