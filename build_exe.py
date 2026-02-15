#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para gerar o executável do NZBGeek Post usando PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path


def build_executable():
    """Compila o script Python em executável Windows"""
    
    print("=" * 70)
    print("🔨 NZBGeek Post - Build Script")
    print("=" * 70)
    print()
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("\nInstalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso")
    
    print()
    print("📦 Gerando executável...")
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
        print("✅ Executável criado com sucesso!")
        print("=" * 70)
        print()
        print("📁 Localização: dist/nzbgeek-post.exe")
        print()
        print("🎯 Próximos passos:")
        print("1. Teste o executável: dist\\nzbgeek-post.exe")
        print("2. Se funcionar, crie uma release no GitHub")
        print("3. Anexe o arquivo .exe na release")
        print()
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(build_executable())
