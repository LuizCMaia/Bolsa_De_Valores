from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time

app = Flask(__name__)

def buscar_dados_com_selenium(codigo_acao, data_pesquisa):
    data_formatada_yahoo = data_pesquisa.strftime('%b %d, %Y').replace(data_pesquisa.strftime('%b'), data_pesquisa.strftime('%b').capitalize())
    url = f"https://finance.yahoo.com/quote/{codigo_acao.upper()}.SA/history"

    chrome_options = Options()
    
    # --- MUDANÇA 1: DEIXE A LINHA ABAIXO COMENTADA POR ENQUANTO ---
    # Ao comentar a linha abaixo, a janela do Chrome vai aparecer na sua tela.
    # chrome_options.add_argument("--headless")
    # ---------------------------------------------------------------
    
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")
    
    service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Acessando {url}...")
        driver.get(url)

        # --- MUDANÇA 2: Usando uma espera inteligente ---
        # Em vez de time.sleep(5), vamos esperar até 20 segundos para a tabela aparecer.
        # Se ela aparecer antes, o código continua imediatamente.
        print("Aguardando a tabela de dados carregar...")
        wait = WebDriverWait(driver, 20)
        
        # Primeiro, vamos tentar encontrar e clicar no botão de aceitar cookies
        try:
            print("Procurando pelo botão de 'Aceitar cookies'...")
            # Este seletor busca por um botão dentro do formulário de consentimento
            botao_aceitar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='agree']")))
            print("Botão encontrado! Clicando...")
            botao_aceitar.click()
            # Espera um pouquinho para a ação ser processada
            time.sleep(2)
        except Exception:
            print("Botão de 'Aceitar' não foi encontrado ou não foi necessário clicar. Continuando...")

        # Agora, esperamos pela tabela principal
        wait.until(EC.presence_of_element_located((By.XPATH, "//table[@data-test='historical-prices']")))
        print("Tabela encontrada!")
        # ----------------------------------------------------

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tabela = soup.find('table', {'data-test': 'historical-prices'})

        if not tabela:
            print("Erro inesperado: Tabela não encontrada mesmo após a espera.")
            return None

        for linha in tabela.find_all('tr'):
            celulas = linha.find_all('td')
            if len(celulas) == 7:
                data_da_linha = celulas[0].text
                if data_da_linha == data_formatada_yahoo:
                    print(f"Dados encontrados para {data_formatada_yahoo}!")
                    dados = {
                        'abertura': f"R$ {float(celulas[1].text.replace(',', '')):.2f}",
                        'maxima': f"R$ {float(celulas[2].text.replace(',', '')):.2f}",
                        'minima': f"R$ {float(celulas[3].text.replace(',', '')):.2f}",
                        'fechamento': f"R$ {float(celulas[4].text.replace(',', '')):.2f}",
                        'volume': celulas[6].text
                    }
                    return dados
        
        print(f"Nenhuma linha encontrada para a data {data_formatada_yahoo}.")
        return None

    except Exception as e:
        print(f"Ocorreu um erro no Selenium: {e}")
        return None
    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    contexto = {}
    if request.method == 'POST':
        codigo_acao = request.form.get('codigo_acao')
        data_str = request.form.get('data')

        if codigo_acao and data_str:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d')
            dados = buscar_dados_com_selenium(codigo_acao, data_obj)
            if dados:
                contexto['dados_acao'] = {'codigo': codigo_acao.upper(), 'data': data_obj.strftime('%d/%m/%Y'), **dados}
            else:
                contexto['erro'] = f"Não foram encontrados dados para a ação {codigo_acao.upper()} na data {data_obj.strftime('%d/%m/%Y')}."

    return render_template('index.html', **contexto)

if __name__ == '__main__':

    app.run(debug=True)
