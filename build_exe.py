#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para gerar o executável do NZBGeek Post usando PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

# Configura encoding para suportar emojis no Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def build_executable():
    """Compila o script Python em executável Windows"""
    
    print("=" * 70)
    print("NZBGeek Post - Build Script v1.1.0")
    print("=" * 70)
    print()
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print("[OK] PyInstaller encontrado")
    except ImportError:
        print("[ERRO] PyInstaller nao encontrado!")
        print("\nInstalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller instalado com sucesso")
    
    print()
    print("Gerando executavel...")
    print()
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--console",                    # Modo console (não GUI)
        "--name=nzbgeek-post",          # Nome do executável
        "--icon=NONE",                  # Sem ícone customizado
        "--clean",                      # Limpa cache antes de build
        "--noconfirm",                  # Não pede confirmação
        "nzbgeek-post.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print()
        print("=" * 70)
        print("[OK] Executavel criado com sucesso!")
        print("=" * 70)
        print()
        print("Localizacao: dist/nzbgeek-post.exe")
        print()
        print("Proximos passos:")
        print("1. Teste o executavel: dist\\nzbgeek-post.exe")
        print("2. Se funcionar, crie uma release no GitHub")
        print("3. Anexe o arquivo .exe na release")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Erro ao gerar executavel: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(build_executable())
