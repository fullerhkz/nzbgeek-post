#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NZBGeek Post - Submission Script
Submete arquivos .nzb para o indexador NZBGeek através da API
Versão: 1.1.1
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

# Inicializa colorama para suporte de cores no Windows
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_ENABLED = True
except ImportError:
    # Fallback se colorama não estiver disponível
    COLORS_ENABLED = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""


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

def print_colored(text: str, color=Fore.WHITE, style=Style.NORMAL, end='\n'):
    """
    Imprime texto colorido
    
    Args:
        text: Texto a ser impresso
        color: Cor do texto (Fore.*)
        style: Estilo do texto (Style.*)
        end: Caractere final
    """
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)


def print_separator(char="=", length=70, color=Fore.CYAN):
    """Imprime uma linha separadora colorida"""
    print_colored(char * length, color)


def print_progress_bar(current: int, total: int, prefix='', suffix='', length=50):
    """
    Exibe uma barra de progresso
    
    Args:
        current: Valor atual
        total: Valor total
        prefix: Texto antes da barra
        suffix: Texto depois da barra
        length: Comprimento da barra
    """
    if total == 0:
        percent = 100
    else:
        percent = int(100 * (current / float(total)))
    
    filled_length = int(length * current // total) if total > 0 else length
    bar_char = '█'
    empty_char = '░'
    
    bar = bar_char * filled_length + empty_char * (length - filled_length)
    
    print(f'\r{Fore.CYAN}{prefix} {Fore.GREEN}|{bar}| {Fore.YELLOW}{percent}% {Fore.WHITE}{suffix}', end='')
    
    if current == total:
        print()  # Nova linha quando completo


def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Exibe o cabeçalho do script com cores"""
    clear_screen()
    
    print_separator("═", 70, Fore.CYAN)
    print()
    print_colored("        ███╗   ██╗███████╗██████╗  ██████╗ ███████╗███████╗██╗  ██╗", Fore.CYAN, Style.BRIGHT)
    print_colored("        ████╗  ██║╚══███╔╝██╔══██╗██╔════╝ ██╔════╝██╔════╝██║ ██╔╝", Fore.CYAN, Style.BRIGHT)
    print_colored("        ██╔██╗ ██║  ███╔╝ ██████╔╝██║  ███╗█████╗  █████╗  █████╔╝ ", Fore.CYAN, Style.BRIGHT)
    print_colored("        ██║╚██╗██║ ███╔╝  ██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔═██╗ ", Fore.CYAN, Style.BRIGHT)
    print_colored("        ██║ ╚████║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██╗", Fore.CYAN, Style.BRIGHT)
    print_colored("        ╚═╝  ╚═══╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝", Fore.CYAN, Style.BRIGHT)
    print()
    print_colored("                         Submission Tool v1.1.1", Fore.YELLOW, Style.BRIGHT)
    print()
    print_separator("═", 70, Fore.CYAN)


def get_api_key() -> Optional[str]:
    """
    Obtém a API key da variável de ambiente
    
    Returns:
        str: API key ou None se não encontrada
    """
    api_key = os.environ.get('NZBGEEK_API_KEY')
    
    if not api_key:
        print()
        print_colored("❌ [ERRO] API key não encontrada!", Fore.RED, Style.BRIGHT)
        print_colored("Por favor, configure a variável de ambiente 'NZBGEEK_API_KEY'", Fore.YELLOW)
        print()
        print_colored("Para configurar no Windows:", Fore.CYAN)
        print_colored("  setx NZBGEEK_API_KEY \"sua_api_key_aqui\"", Fore.WHITE)
        print()
        print_colored("Ou adicione através do Painel de Controle -> Sistema -> Variáveis de Ambiente", Fore.CYAN)
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
        print()
        print_colored("❌ [ERRO] Pasta de submissão não configurada!", Fore.RED, Style.BRIGHT)
        print_colored("Configure a variável de ambiente 'NZBGEEK_SUBMISSION_FOLDER'", Fore.YELLOW)
        return None, None, None
    
    if not complete_folder:
        print()
        print_colored("❌ [ERRO] Pasta de destino não configurada!", Fore.RED, Style.BRIGHT)
        print_colored("Configure a variável de ambiente 'NZBGEEK_COMPLETE_FOLDER'", Fore.YELLOW)
        return None, None, None
    
    if not log_folder:
        print()
        print_colored("❌ [ERRO] Pasta de logs não configurada!", Fore.RED, Style.BRIGHT)
        print_colored("Configure a variável de ambiente 'NZBGEEK_LOG_FOLDER'", Fore.YELLOW)
        return None, None, None
    
    submission_path = Path(submission_folder)
    complete_path = Path(complete_folder)
    log_path = Path(log_folder)
    
    # Verifica se a pasta de origem existe
    if not submission_path.exists():
        print()
        print_colored(f"❌ [ERRO] Pasta de origem não encontrada: '{submission_path}'", Fore.RED, Style.BRIGHT)
        return None, None, None
    
    # Cria pasta de destino se não existir
    if not complete_path.exists():
        print_colored(f"📁 [INFO] Criando pasta de destino: '{complete_path}'", Fore.BLUE)
        try:
            complete_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print_colored(f"❌ [ERRO] Não foi possível criar pasta de destino: {e}", Fore.RED, Style.BRIGHT)
            return None, None, None
    
    # Cria pasta de logs se não existir
    if not log_path.exists():
        print_colored(f"📝 [INFO] Criando pasta de logs: '{log_path}'", Fore.BLUE)
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print_colored(f"❌ [ERRO] Não foi possível criar pasta de logs: {e}", Fore.RED, Style.BRIGHT)
            return None, None, None
    
    return submission_path, complete_path, log_path


def select_category() -> Optional[str]:
    """
    Permite ao usuário selecionar uma categoria
    
    Returns:
        str: ID da categoria selecionada, ou None se o usuário escolheu sair
    """
    print()
    print_separator("─", 70, Fore.CYAN)
    print_colored("📋 Selecione a categoria para os arquivos NZB:", Fore.CYAN, Style.BRIGHT)
    print_separator("─", 70, Fore.CYAN)
    print()
    
    # Lista as categorias principais com cores
    print_colored("  1", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - Console", Fore.WHITE)
    
    print_colored("  2", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - Movies (Filmes)", Fore.WHITE)
    
    print_colored("  3", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - Audio (Música)", Fore.WHITE)
    
    print_colored("  4", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - PC (Aplicativos)", Fore.WHITE)
    
    print_colored("  5", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - TV (Séries)", Fore.WHITE)
    
    print_colored("  6", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - XXX (Adulto)", Fore.WHITE)
    
    print_colored("  7", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - Books (Livros)", Fore.WHITE)
    
    print_colored("  8", Fore.YELLOW, Style.BRIGHT, end="")
    print_colored(" - Other (Outros)", Fore.WHITE)
    
    print()
    print_colored("  9", Fore.GREEN, Style.BRIGHT, end="")
    print_colored(" - Usar padrão (PC/0day - 4010)", Fore.GREEN)
    
    print()
    print_colored("  0", Fore.RED, Style.BRIGHT, end="")
    print_colored(" - Sair do programa", Fore.RED)
    
    print()
    print_separator("─", 70, Fore.CYAN)
    
    while True:
        print()
        print_colored("Digite o número da categoria (0-9 ou ENTER para padrão): ", Fore.CYAN, end="")
        choice = input().strip()
        
        if choice == "":
            # ENTER pressionado - usar categoria padrão
            return DEFAULT_CATEGORY
        
        if choice == "0":
            return None  # Sinal para sair
        
        if choice == "9":
            return DEFAULT_CATEGORY
        
        if choice in CATEGORIES:
            # Permite inserir subcategoria se necessário
            print()
            print_colored(f"✓ Você selecionou: {CATEGORIES[choice]}", Fore.GREEN, Style.BRIGHT)
            print_colored("Digite o ID completo da subcategoria (ou ENTER para usar apenas a categoria principal): ", Fore.CYAN, end="")
            sub = input().strip()
            
            if sub:
                return sub
            else:
                return f"{choice}000"  # Categoria principal
        
        print_colored("❌ Opção inválida! Digite um número entre 0 e 9.", Fore.RED, Style.BRIGHT)


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
    print()
    print_separator("═", 70, Fore.MAGENTA)
    print_colored("                     📋 CONFIGURAÇÕES", Fore.MAGENTA, Style.BRIGHT)
    print_separator("═", 70, Fore.MAGENTA)
    print()
    
    print_colored("  📂 Pasta de origem:    ", Fore.CYAN, end="")
    print_colored(str(submission_folder), Fore.WHITE)
    
    print_colored("  📁 Pasta de destino:   ", Fore.CYAN, end="")
    print_colored(str(complete_folder), Fore.WHITE)
    
    print_colored("  📝 Log do dia:         ", Fore.CYAN, end="")
    print_colored(log_file.name, Fore.WHITE)
    
    print_colored("  🔖 Categoria:          ", Fore.CYAN, end="")
    print_colored(f"ID {category}", Fore.YELLOW, Style.BRIGHT)
    
    print()
    print_separator("═", 70, Fore.MAGENTA)
    print()
    
    # Confirmação
    print_colored("Pressione ENTER para iniciar o envio dos arquivos NZB, ou CTRL+C para cancelar.", Fore.GREEN, Style.BRIGHT)
    input()
    
    # Lista arquivos NZB
    nzb_files = list(submission_folder.glob("*.nzb"))
    
    if not nzb_files:
        print()
        print_colored("⚠️  Nenhum arquivo NZB encontrado para enviar.", Fore.YELLOW, Style.BRIGHT)
        write_log(log_file, "Nenhum arquivo NZB encontrado.")
        return 0
    
    # Exibe informações sobre processamento
    total_files = len(nzb_files)
    print()
    print_separator("─", 70, Fore.CYAN)
    print_colored(f"📦 Total de arquivos encontrados: {total_files}", Fore.CYAN, Style.BRIGHT)
    print_separator("─", 70, Fore.CYAN)
    print()
    
    # Processa cada arquivo
    success_count = 0
    
    for idx, nzb_file in enumerate(nzb_files, 1):
        print()
        print_separator("─", 70, Fore.BLUE)
        print_colored(f"📤 [{idx}/{total_files}] Enviando: ", Fore.CYAN, Style.BRIGHT, end="")
        print_colored(nzb_file.name, Fore.WHITE, Style.BRIGHT)
        print_separator("─", 70, Fore.BLUE)
        
        write_log(log_file, f"[{idx}/{total_files}] Enviando: {nzb_file.name} (Categoria: {category})")
        
        # Simula barra de progresso durante upload
        print_colored("Enviando...", Fore.YELLOW)
        for i in range(11):
            print_progress_bar(i, 10, prefix='Progresso:', suffix='', length=40)
            time.sleep(0.05)  # Pequeno delay para visualização
        
        # Submete o arquivo
        success, response = submit_nzb(nzb_file, api_key, category)
        
        if success:
            write_log(log_file, f"Resposta: {response}")
            
            # Verifica se o envio foi bem-sucedido
            try:
                response_json = json.loads(response)
                if response_json.get('response', {}).get('@attributes', {}).get('REGISTER') == 'OK':
                    print()
                    print_colored("✅ Enviado com sucesso!", Fore.GREEN, Style.BRIGHT)
                    
                    # Move o arquivo para a pasta de completos
                    try:
                        destination = complete_folder / nzb_file.name
                        
                        # Remove arquivo existente se necessário
                        if destination.exists():
                            destination.unlink()
                        
                        nzb_file.rename(destination)
                        print_colored(f"   ➜ Movido para: ", Fore.CYAN, end="")
                        print_colored(str(destination), Fore.WHITE)
                        write_log(log_file, f"Movido para: {destination}")
                        success_count += 1
                        
                    except Exception as e:
                        print()
                        print_colored(f"❌ [ERRO] Falha ao mover arquivo: {e}", Fore.RED, Style.BRIGHT)
                        write_log(log_file, f"[ERRO] Falha ao mover arquivo: {e}")
                else:
                    print()
                    print_colored(f"⚠️  Resposta inesperada da API: {response}", Fore.YELLOW)
                    write_log(log_file, f"[AVISO] Resposta inesperada: {response}")
                    
            except json.JSONDecodeError:
                print()
                print_colored(f"⚠️  Não foi possível interpretar a resposta: {response}", Fore.YELLOW)
                write_log(log_file, f"[AVISO] Resposta não-JSON: {response}")
        else:
            print()
            print_colored(f"❌ [ERRO] Falha no envio: {response}", Fore.RED, Style.BRIGHT)
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
                print()
                print_colored("Pressione ENTER para sair...", Fore.CYAN)
                input()
                return 1
            
            submission_folder, complete_folder, log_folder = get_folders()
            if not submission_folder:
                print()
                print_colored("Pressione ENTER para sair...", Fore.CYAN)
                input()
                return 1
            
            # Seleciona categoria
            category = select_category()
            
            # Se usuário escolheu sair
            if category is None:
                print()
                print_colored("👋 Até logo!", Fore.CYAN, Style.BRIGHT)
                time.sleep(1)
                return 0
            
            # Processa arquivos NZB
            success_count = process_nzbs(
                submission_folder, 
                complete_folder, 
                log_folder, 
                api_key, 
                category
            )
            
            # Exibe resultado
            print()
            print_separator("═", 70, Fore.GREEN)
            print_colored(f"✅ Total de arquivos enviados com sucesso: {success_count}", Fore.GREEN, Style.BRIGHT)
            print_separator("═", 70, Fore.GREEN)
            print_colored("            PROCESSAMENTO CONCLUÍDO", Fore.GREEN, Style.BRIGHT)
            print_separator("═", 70, Fore.GREEN)
            
            # Pergunta se deseja continuar
            print()
            print()
            print_colored("O que deseja fazer agora?", Fore.CYAN, Style.BRIGHT)
            print()
            print_colored("  1", Fore.YELLOW, Style.BRIGHT, end="")
            print_colored(" - Verificar novamente por novos NZBs", Fore.WHITE)
            print_colored("  0", Fore.RED, Style.BRIGHT, end="")
            print_colored(" - Sair do programa", Fore.RED)
            
            while True:
                print()
                print_colored("Digite sua opção (0-1): ", Fore.CYAN, end="")
                choice = input().strip()
                
                if choice == "0":
                    print()
                    print_colored("👋 Até logo!", Fore.CYAN, Style.BRIGHT)
                    time.sleep(1)
                    return 0
                elif choice == "1":
                    break
                else:
                    print_colored("❌ Opção inválida! Digite 0 ou 1.", Fore.RED, Style.BRIGHT)
    
    except KeyboardInterrupt:
        print()
        print()
        print_colored("⚠️  Script interrompido pelo usuário.", Fore.YELLOW, Style.BRIGHT)
        time.sleep(2)
        return 130
    except Exception as e:
        print()
        print()
        print_colored(f"❌ [ERRO CRÍTICO] {e}", Fore.RED, Style.BRIGHT)
        print()
        print_colored("Pressione ENTER para sair...", Fore.CYAN)
        input()
        return 1


if __name__ == "__main__":
    sys.exit(main())
