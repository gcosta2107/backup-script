import os
import time
import shutil

def obter_data_atual():
    return time.time()

def calcular_diferenca_tres_dias():
    return 3 * 24 * 60 * 60  # 3 dias em segundos

def listar_arquivos(caminho_backup, arquivo_log):
    for root, dirs, files in os.walk(caminho_backup):
        for nome_arquivo in files:
            caminho_completo = os.path.join(root, nome_arquivo)
            
            tamanho = os.path.getsize(caminho_completo)
            data_criacao = os.path.getctime(caminho_completo)
            data_modificacao = os.path.getmtime(caminho_completo)
            
            arquivo_log.write(f"Nome: {nome_arquivo}\n")
            arquivo_log.write(f"Tamanho: {tamanho} bytes\n")
            arquivo_log.write(f"Data de Criação: {time.ctime(data_criacao)}\n")
            arquivo_log.write(f"Data da Última Modificação: {time.ctime(data_modificacao)}\n\n")
            
            yield caminho_completo, data_criacao

def copiar_arquivos_recentes(caminho_destino, arquivo_log_destino, data_atual, diferenca_tres_dias):
    with open(arquivo_log_destino, 'w') as arquivo_log_destino:
        for caminho_completo, data_criacao in listar_arquivos(caminho_backup, arquivo_log_destino):
            if data_atual - data_criacao <= diferenca_tres_dias:
                destino = os.path.join(caminho_destino, os.path.basename(caminho_completo))
                shutil.copy2(caminho_completo, destino)
                arquivo_log_destino.write(f"Arquivo copiado para {destino}\n")

def remover_arquivos_antigos(caminho_backup, data_atual, diferenca_tres_dias):
    for caminho_completo, data_criacao in listar_arquivos(caminho_backup, open(arquivo_saida, 'w')):
        if data_atual - data_criacao > diferenca_tres_dias:
            os.remove(caminho_completo)
            arquivo_saida.write(f"Arquivo removido: {caminho_completo}\n")

if __name__ == "__main__":
    caminho_backup = '/home/valcann/backupsFrom'
    arquivo_saida = '/home/valcann/backupsFrom.log'
    caminho_destino = '/home/valcann/backupsTo'
    arquivo_log_destino = '/home/valcann/backupsTo.log'

    data_atual = obter_data_atual()
    diferenca_tres_dias = calcular_diferenca_tres_dias()

    copiar_arquivos_recentes(caminho_destino, arquivo_log_destino, data_atual, diferenca_tres_dias)
    remover_arquivos_antigos(caminho_backup, data_atual, diferenca_tres_dias)
