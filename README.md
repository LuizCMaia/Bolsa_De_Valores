# Consulta de Ações com Flask e Selenium

Este é um projeto de uma aplicação web simples, desenvolvida em Python com o framework Flask, que permite consultar a cotação histórica de ações da bolsa de valores brasileira (B3).

O grande diferencial deste projeto é o uso do **Selenium** para realizar a coleta de dados (web scraping) diretamente do site Yahoo Finance. Essa abordagem torna a aplicação resiliente a bloqueios de rede (como os encontrados em ambientes corporativos ou de faculdades) que normalmente impedem scripts de acessarem a internet diretamente.

## Funcionalidades

- Interface web simples para consulta por código da ação (ex: `PETR4`) e data.
- Coleta de dados em tempo real da página do Yahoo Finance.
- Exibição dos valores de Abertura, Fechamento, Máxima, Mínima e Volume do dia.
- Valores formatados em Reais (R$).
- Design responsivo básico para uso em desktop e mobile.

## Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Web Scraping:** Selenium
- **Parsing de HTML:** BeautifulSoup4
- **Frontend:** HTML, CSS

## Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados em seu computador:

1.  **Python 3.8+**: [Download do Python](https://www.python.org/downloads/)
2.  **pip**: (Normalmente já vem instalado com o Python)
3.  **Git**: [Download do Git](https://git-scm.com/downloads)
4.  **Google Chrome**: [Download do Google Chrome](https://www.google.com/chrome/)

## Guia de Instalação e Execução

Siga estes passos para configurar e rodar o projeto em um novo computador.

**1. Clonar o Repositório**

Abra um terminal (CMD, PowerShell ou Terminal) e clone este repositório do GitHub.

```bash
git clone https://github.com/LuizCMaia/Bolsa_De_Valores
```
Ou fazer o download clicando em Download ZIP
Após isso, extrair a pasta.

Abra um terminal (CMD, PowerShell ou Terminal).

Caminhe para a pasta do projeto utilizado CD: (Caminho da pasta).

**2. Criar um Ambiente Virtual**

É uma boa prática isolar as dependências do projeto.

```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate
```

**3. Instalar as Dependências**

Com o ambiente virtual ativo, instale todas as bibliotecas listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

**4. Baixar o ChromeDriver Correto (Passo Crucial!)**

O Selenium precisa de um "driver" para se comunicar com o Google Chrome.

- **a. Descubra a sua versão do Chrome:** Abra o Chrome, vá em **Ajuda > Sobre o Google Chrome** e anote a versão (ex: `129.0.5112.81`).

- **b. Baixe o driver correspondente:** Acesse o site [Google Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/), encontre a sua versão na lista e baixe o `chromedriver` para `win64`.

- **c. Coloque na pasta do projeto:** Descompacte o arquivo ZIP e coloque o `chromedriver.exe` **na raiz da pasta do projeto** (`site_bolsa`), ao lado do arquivo `app.py`.

**5. Rodar a Aplicação**

Finalmente, execute o script principal do Flask.

```bash
python app.py
```

O terminal irá mostrar que o servidor está rodando em `http://127.0.0.1:5000`.

**6. Acessar o Site**

Abra seu navegador e acesse o endereço: [http://127.0.0.1:5000](http://127.0.0.1:5000).

Pronto! Agora você pode consultar as cotações das ações.

## Solução de Problemas (Troubleshooting)

- **`SessionNotCreatedException`**: Este erro significa que a versão do seu `chromedriver.exe` é incompatível com a versão do seu navegador Google Chrome. Refaça o **Passo 4** com atenção para baixar a versão exata.

- **`Tabela de dados históricos não encontrada`**: Se o site funcionar mas não encontrar os dados, pode ser que a sua conexão com a internet esteja lenta ou o site do Yahoo Finance tenha mudado sua estrutura. No arquivo `app.py`, tente aumentar o tempo de espera na linha `wait = WebDriverWait(driver, 20)` para um valor maior, como `30`.
