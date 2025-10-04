import json
from flask import Flask, render_template, request
from datetime import datetime, time

app = Flask(__name__)

def processar_dados_colados(dados_json_str, data_pesquisa):
    """
    Processa o texto JSON colado pelo usuário para encontrar os dados de um dia específico.
    """
    try:
        dados_json = json.loads(dados_json_str)

        historico = dados_json.get('results', [{}])[0].get('historicalDataPrice')
        if not historico:
            return None

        timestamp_inicio_dia = int(datetime.combine(data_pesquisa, time.min).timestamp())
        timestamp_fim_dia = int(datetime.combine(data_pesquisa, time.max).timestamp())

        for dados_dia in historico:
            if timestamp_inicio_dia <= dados_dia['date'] <= timestamp_fim_dia:
                return {
                    'fechamento': f"R$ {dados_dia['close']:.2f}",
                    'abertura': f"R$ {dados_dia['open']:.2f}",
                    'maxima': f"R$ {dados_dia['high']:.2f}",
                    'minima': f"R$ {dados_dia['low']:.2f}",
                    'volume': f"{dados_dia['volume']:,}".replace(",", ".")
                }
        return None

    except (json.JSONDecodeError, KeyError, IndexError):
        return {'erro_json': 'O texto colado não é um JSON válido ou está em um formato inesperado.'}
    except Exception as e:
        return {'erro_geral': f'Ocorreu um erro inesperado: {e}'}

@app.route('/', methods=['GET', 'POST'])
def index():
    contexto = {}
    if request.method == 'POST':
        codigo_acao = request.form.get('codigo_acao')
        data_str = request.form.get('data')
        dados_colados = request.form.get('dados_colados')

        if codigo_acao and data_str and dados_colados:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
            dados = processar_dados_colados(dados_colados, data_obj)
            
            if dados and 'erro_json' in dados:
                 contexto['erro'] = dados['erro_json']
            elif dados and 'erro_geral' in dados:
                 contexto['erro'] = dados['erro_geral']
            elif dados:
                contexto['dados_acao'] = {'codigo': codigo_acao.upper(), 'data': data_obj.strftime('%d/%m/%Y'), **dados}
            else:
                contexto['erro'] = f"Não foram encontrados dados para a data {data_obj.strftime('%d/%m/%Y')} no texto que você colou."
        else:
            contexto['erro'] = "Por favor, preencha todos os campos, incluindo os dados da API."
                
    return render_template('index.html', **contexto)

if __name__ == '__main__':
    app.run(debug=True)

