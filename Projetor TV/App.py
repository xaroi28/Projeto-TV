from flask import Flask, render_template, request, jsonify
import os
import re
import threading
import subprocess
import time
import webbrowser

app = Flask(__name__)

@app.route('/update_pedidos', methods=['POST'])
def update_pedidos():
    try:
        data = request.get_json()
        pedidos_text = data.get('pedidos')
        pedidos_path = r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Pedidos.txt'
        with open(pedidos_path, 'w') as file:
            file.write(pedidos_text)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Erro ao atualizar pedidos: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/letreiro')
def letreiro():
    return render_template('letreiro.html')

@app.route('/get_data')
def get_data():
    file_path = r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\pedidos.txt'

    pedidos_dirs = [
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 1 - Arquivos de_',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 2',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 3',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 4',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 5',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out hosp'
    ]

    if not os.path.exists(file_path):
        return {"error": "Arquivo 'pedidos.txt' não encontrado."}

    hosp_remessas = []
    farma_remessas = []
    farma_count = 0

    incluidos = ["MUNICIPIO ", "FUNDO MUNICIPAL ", "FMS", "MUN ", "INTERMUNICIPAL", "FUNDO MUN ", "MUNICIPAL ", "SEC DE EST", "INSTITUTO DE PREVIDENCIA", "FUNDACAO HOSPITALAR", "MUNCIPIO"]
    excluidos = ["LTDA", "EIRELI", "FARMA", " ME ", " MEI "]

    remessas_remover = set()
    for dir_path in pedidos_dirs:
        if not os.path.exists(dir_path):
            print(f"Diretório não encontrado: {dir_path}")
            continue

        for file_name in os.listdir(dir_path):
            if file_name.endswith('.txt'):
                pedidos_path = os.path.join(dir_path, file_name)
                try:
                    with open(pedidos_path, 'r') as pedidos_file:
                        remessas_remover.update(line.strip() for line in pedidos_file)
                except Exception as e:
                    print(f"Erro ao ler {pedidos_path}: {e}")

    total_value = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip().split('\t')
                if len(line) < 6:
                    continue

                remessa = line[1]
                cliente = line[2]

                is_hosp = any(exc in cliente for exc in incluidos) and not any(exc in cliente for exc in excluidos)

                if is_hosp:
                    if remessa not in remessas_remover:
                        hosp_remessas.append({'remessa': remessa, 'cliente': cliente})
                else:
                    if remessa not in remessas_remover:
                        farma_remessas.append({'remessa': remessa, 'cliente': cliente})
                        farma_count += 1

                total_value += 1
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")

    checkout_contents = {}
    for index, dir_path in enumerate(pedidos_dirs, start=1):
        if not os.path.exists(dir_path):
            print(f"Diretório não encontrado: {dir_path}")
            continue

        for file_name in os.listdir(dir_path):
            if file_name.endswith('.txt'):
                date_match = re.search(r'Check Out \d+ - (\d{4}-\d{2}-\d{2})\.txt$', file_name)
                date = date_match.group(1) if date_match else ''

                pedidos_path = os.path.join(dir_path, file_name)
                try:
                    with open(pedidos_path, 'r') as checkout_file:
                        lines = checkout_file.readlines()
                        for line in lines:
                            remessa = line.strip()
                            checkout_entry = f"{remessa} - {date}"
                            if f'Checkout {index}' not in checkout_contents:
                                checkout_contents[f'Checkout {index}'] = []
                            checkout_contents[f'Checkout {index}'].append(checkout_entry)
                except Exception as e:
                    print(f"Erro ao ler {pedidos_path}: {e}")

    for key in checkout_contents:
        checkout_contents[key] = '<br>'.join(checkout_contents[key])

    total_remessas = len(hosp_remessas) + farma_count

    return {
        "hosp_count": len(hosp_remessas),
        "farma_count": farma_count,
        "total_value": total_remessas,
        "checkout_contents": checkout_contents
    }

def abrir_letreiro_em_tela_cheia():
    time.sleep(2)
    chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'
    comando = f'{chrome_path} --new-window --start-fullscreen --window-position=1366,0 http://127.0.0.1:5000/letreiro'
    subprocess.Popen(comando, shell=True)

def abrir_index():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000/")

@app.route('/log')
def log():
    file_path = r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\pedidos.txt'

    pedidos_dirs = [
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 1 - Arquivos de_',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 2',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 3',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 4',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out 5',
        r'C:\Users\Visitante\OneDrive\Documentos\ondrive\OneDrive\Check out hosp'
    ]

    incluidos = ["MUNICIPIO ", "FUNDO MUNICIPAL ", "FMS", "MUN ", "INTERMUNICIPAL", "FUNDO MUN ", "MUNICIPAL ", "SEC DE EST", "INSTITUTO DE PREVIDENCIA", "FUNDACAO HOSPITALAR", "MUNCIPIO"]
    excluidos = ["LTDA", "EIRELI", "FARMA", " ME ", " MEI "]

    remessas_remover = set()
    for dir_path in pedidos_dirs:
        if os.path.exists(dir_path):
            for file_name in os.listdir(dir_path):
                if file_name.endswith('.txt'):
                    with open(os.path.join(dir_path, file_name), 'r') as pedidos_file:
                        remessas_remover.update(line.strip() for line in pedidos_file)

    hosp_remessas = []
    farma_remessas = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().split('\t')
            if len(line) < 6:
                continue
            remessa = line[1]
            cliente = line[2]

            if remessa in remessas_remover:
                continue

            is_hosp = any(exc in cliente for exc in incluidos) and not any(exc in cliente for exc in excluidos)

            if is_hosp:
                hosp_remessas.append({'remessa': remessa, 'cliente': cliente})
            else:
                farma_remessas.append({'remessa': remessa, 'cliente': cliente})

    return render_template('log.html', hosp_remessas=hosp_remessas, farma_remessas=farma_remessas)

if __name__ == '__main__':
    threading.Thread(target=abrir_letreiro_em_tela_cheia, daemon=True).start()
    threading.Thread(target=abrir_index, daemon=True).start()
    app.run(debug=True)
