#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NZBGeek Submission Script
Submete arquivos .nzb para o indexador NZBGeek através da API
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


# ==================== CONFIGURAÇÕES ====================

# Constantes
API_URL = "https://api.nzbgeek.info/submit"
DEFAULT_CATEGORY = "4010"  # PC/0day

# Categorias disponíveis (conforme documentação da API)
CATEGORIES = {
    "1": "Console",
    "2": "Movies",
    "3": "Audio",
    "4": "PC",
    "5": "TV",
    "6": "XXX",
    "7": "Books",
    "8": "Other"
}


# ==================== FUNÇÕES AUXILIARES ====================

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Exibe o cabeçalho do script"""
    header_width = 70
    line = "=" * header_width
    
    clear_screen()
    print(line)
    print()
    print()
    print("        ███╗   ██╗███████╗██████╗  ██████╗ ███████╗███████╗██╗  ██╗")
    print("        ████╗  ██║╚══███╔╝██╔══██╗██╔════╝ ██╔════╝██╔════╝██║ ██╔╝")
    print("        ██╔██╗ ██║  ███╔╝ ██████╔╝██║  ███╗█████╗  █████╗  █████╔╝ ")
    print("        ██║╚██╗██║ ███╔╝  ██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔═██╗ ")
    print("        ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██╗")
    print("        ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝")
    print()
    print()


def get_api_key() -> Optional[str]:
    """
    Obtém a API key da variável de ambiente
    
    Returns:
        str: API key ou None se não encontrada
    """
    api_key = os.environ.get('NZBGEEK_API_KEY')
    
    if not api_key:
        print("\n❌ [ERRO] API key não encontrada!")
        print("Por favor, configure a variável de ambiente 'NZBGEEK_API_KEY'")
        print("\nPara configurar no Windows:")
        print("  setx NZBGEEK_API_KEY \"sua_api_key_aqui\"")
        print("\nOu adicione através do Painel de Controle -> Sistema -> Variáveis de Ambiente")
        return None
    
    return api_key


def get_folders() -> Tuple[Optional[Path], Optional[Path], Optional[Path]]:
    """
    Obtém as pastas de origem, destino e logs das variáveis de ambiente
    
    Returns:
        Tuple: (pasta_origem, pasta_destino, pasta_logs) ou (None, None, None) se alguma não existir
    """
    submission_folder = os.environ.get('NZBGEEK_SUBMISSION_FOLDER')
    complete_folder = os.environ.get('NZBGEEK_COMPLETE_FOLDER')
    log_folder = os.environ.get('NZBGEEK_LOG_FOLDER')
    
    if not submission_folder:
        print("\n❌ [ERRO] Pasta de submissão não configurada!")
        print("Configure a variável de ambiente 'NZBGEEK_SUBMISSION_FOLDER'")
        return None, None, None
    
    if not complete_folder:
        print("\n❌ [ERRO] Pasta de destino não configurada!")
        print("Configure a variável de ambiente 'NZBGEEK_COMPLETE_FOLDER'")
        return None, None, None
    
    if not log_folder:
        print("\n❌ [ERRO] Pasta de logs não configurada!")
        print("Configure a variável de ambiente 'NZBGEEK_LOG_FOLDER'")
        return None, None, None
    
    submission_path = Path(submission_folder)
    complete_path = Path(complete_folder)
    log_path = Path(log_folder)
    
    # Verifica se a pasta de origem existe
    if not submission_path.exists():
        print(f"\n❌ [ERRO] Pasta de origem não encontrada: '{submission_path}'")
        return None, None, None
    
    # Cria pasta de destino se não existir
    if not complete_path.exists():
        print(f"📁 [INFO] Criando pasta de destino: '{complete_path}'")
        try:
            complete_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ [ERRO] Não foi possível criar pasta de destino: {e}")
            return None, None, None
    
    # Cria pasta de logs se não existir
    if not log_path.exists():
        print(f"📝 [INFO] Criando pasta de logs: '{log_path}'")
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ [ERRO] Não foi possível criar pasta de logs: {e}")
            return None, None, None
    
    return submission_path, complete_path, log_path


def select_category() -> str:
    """
    Permite ao usuário selecionar uma categoria
    
    Returns:
        str: ID da categoria selecionada
    """
    print("\n📋 Selecione a categoria para os arquivos NZB:")
    print("=" * 50)
    
    # Lista as categorias principais
    print("1 - Console")
    print("2 - Movies (Filmes)")
    print("3 - Audio (Música)")
    print("4 - PC (Aplicativos)")
    print("5 - TV (Séries)")
    print("6 - XXX (Adulto)")
    print("7 - Books (Livros)")
    print("8 - Other (Outros)")
    print("0 - Usar padrão (PC/0day - 4010)")
    print("=" * 50)
    
    while True:
        choice = input("\nDigite o número da categoria (0-8): ").strip()
        
        if choice == "0":
            return DEFAULT_CATEGORY
        
        if choice in CATEGORIES:
            # Permite inserir subcategoria se necessário
            print(f"\nVocê selecionou: {CATEGORIES[choice]}")
            sub = input("Digite o ID completo da subcategoria (ou ENTER para usar apenas a categoria principal): ").strip()
            
            if sub:
                return sub
            else:
                return f"{choice}000"  # Categoria principal
        
        print("❌ Opção inválida! Digite um número entre 0 e 8.")


def write_log(log_file: Path, message: str):
    """
    Escreve uma mensagem no arquivo de log
    
    Args:
        log_file: Caminho do arquivo de log
        message: Mensagem a ser escrita
    """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} {message}\n")
    except Exception as e:
        print(f"⚠️  [AVISO] Erro ao escrever no log: {e}")


def submit_nzb(nzb_file: Path, api_key: str, category: Optional[str] = None) -> Tuple[bool, str]:
    """
    Submete um arquivo NZB para o NZBGeek
    
    Args:
        nzb_file: Caminho do arquivo NZB
        api_key: API key do NZBGeek
        category: ID da categoria (opcional)
    
    Returns:
        Tuple: (sucesso: bool, resposta: str)
    """
    try:
        # Prepara a URL com a API key
        url = f"{API_URL}?apikey={api_key}"
        
        # Adiciona categoria se fornecida
        if category:
            url += f"&cat={category}"
        
        # Prepara o arquivo para upload
        with open(nzb_file, 'rb') as f:
            files = {'nzb': (nzb_file.name, f, 'application/x-nzb')}
            
            # Envia a requisição
            response = requests.post(url, files=files, timeout=60, verify=False)
            response.raise_for_status()
            
            # Retorna o resultado
            return True, response.text
            
    except requests.exceptions.RequestException as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def process_nzbs(submission_folder: Path, complete_folder: Path, log_folder: Path, 
                 api_key: str, category: str) -> int:
    """
    Processa todos os arquivos NZB na pasta de submissão
    
    Args:
        submission_folder: Pasta contendo os arquivos NZB
        complete_folder: Pasta para onde os arquivos serão movidos após o envio
        log_folder: Pasta onde os logs serão salvos
        api_key: API key do NZBGeek
        category: ID da categoria
    
    Returns:
        int: Número de arquivos enviados com sucesso
    """
    # Cria arquivo de log diário
    today = datetime.now().strftime("%d-%m-%Y")
    log_file = log_folder / f"submit_log_{today}.txt"
    
    # Exibe configurações
    print("\n" + " " * 8 + "=" * 49)
    print(" " * 8 + "           📋 CONFIGURAÇÕES")
    print(" " * 8 + "=" * 49)
    print(f" " * 8 + f"📂 Pasta de origem:    {submission_folder}")
    print(f" " * 8 + f"📁 Pasta de destino:   {complete_folder}")
    print(f" " * 8 + f"📝 Log do dia:         {log_file}")
    print(f" " * 8 + f"🔖 Categoria:          ID {category}")
    print(" " * 8 + "=" * 49)
    print()
    
    # Confirmação
    input("\nPressione ENTER para iniciar o envio dos arquivos NZB, ou CTRL+C para cancelar.\n")
    
    # Lista arquivos NZB
    nzb_files = list(submission_folder.glob("*.nzb"))
    
    if not nzb_files:
        print("\n⚠️  Nenhum arquivo NZB encontrado para enviar.")
        write_log(log_file, "Nenhum arquivo NZB encontrado.")
        return 0
    
    # Processa cada arquivo
    success_count = 0
    
    for nzb_file in nzb_files:
        print(f"\n📤 Enviando: {nzb_file.name}")
        write_log(log_file, f"Enviando: {nzb_file.name} (Categoria: {category})")
        
        # Submete o arquivo
        success, response = submit_nzb(nzb_file, api_key, category)
        
        if success:
            write_log(log_file, f"Resposta: {response}")
            
            # Verifica se o envio foi bem-sucedido
            try:
                response_json = json.loads(response)
                if response_json.get('response', {}).get('@attributes', {}).get('REGISTER') == 'OK':
                    print(f"✅ Enviado com sucesso!")
                    
                    # Move o arquivo para a pasta de completos
                    try:
                        destination = complete_folder / nzb_file.name
                        
                        # Remove arquivo existente se necessário
                        if destination.exists():
                            destination.unlink()
                        
                        nzb_file.rename(destination)
                        print(f"   ➜ Movido para: {destination}")
                        write_log(log_file, f"Movido para: {destination}")
                        success_count += 1
                        
                    except Exception as e:
                        print(f"❌ [ERRO] Falha ao mover arquivo: {e}")
                        write_log(log_file, f"[ERRO] Falha ao mover arquivo: {e}")
                else:
                    print(f"⚠️  Resposta inesperada da API: {response}")
                    write_log(log_file, f"[AVISO] Resposta inesperada: {response}")
                    
            except json.JSONDecodeError:
                print(f"⚠️  Não foi possível interpretar a resposta: {response}")
                write_log(log_file, f"[AVISO] Resposta não-JSON: {response}")
        else:
            print(f"❌ [ERRO] Falha no envio: {response}")
            write_log(log_file, f"[ERRO] Falha no envio: {response}")
    
    return success_count


def main():
    """Função principal"""
    try:
        while True:
            # Exibe cabeçalho
            print_header()
            
            # Obtém configurações
            api_key = get_api_key()
            if not api_key:
                input("\nPressione ENTER para sair...")
                return 1
            
            submission_folder, complete_folder, log_folder = get_folders()
            if not submission_folder:
                input("\nPressione ENTER para sair...")
                return 1
            
            # Seleciona categoria
            category = select_category()
            
            # Processa arquivos NZB
            success_count = process_nzbs(
                submission_folder, 
                complete_folder, 
                log_folder, 
                api_key, 
                category
            )
            
            # Exibe resultado
            print("\n" + "=" * 70)
            print(f"✅ Total de arquivos enviados com sucesso: {success_count}")
            print("=" * 70)
            print("          PROCESSAMENTO CONCLUÍDO")
            print("=" * 70)
            
            # Pergunta se deseja continuar
            print("\n\nO que deseja fazer agora?")
            print("1 - Verificar novamente por novos NZBs")
            print("0 - Sair")
            
            while True:
                choice = input("\nDigite sua opção (0-1): ").strip()
                
                if choice == "0":
                    print("\n✅ Script finalizado!")
                    input("Pressione ENTER para sair...")
                    return 0
                elif choice == "1":
                    break
                else:
                    print("❌ Opção inválida! Digite 0 ou 1.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrompido pelo usuário.")
        input("Pressione ENTER para sair...")
        return 130
    except Exception as e:
        print(f"\n\n❌ [ERRO CRÍTICO] {e}")
        input("Pressione ENTER para sair...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
