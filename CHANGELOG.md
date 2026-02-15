# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.1] - 2026-02-15

### ✨ Adicionado
- Opção numérica "0" para sair do programa no menu de categorias
- Fechamento automático do terminal ao selecionar sair (sem necessidade de pressionar ENTER adicional)

### 🔄 Modificado
- Menu de categorias agora vai de 0-9 (opção 9 para categoria padrão)
- Opção "0 - Sair" destaca em vermelho para maior visibilidade
- Mensagem de saída mais amigável ("👋 Até logo!")
- Interrupção por CTRL+C agora fecha automaticamente após 2 segundos

### 🐛 Correções
- Usuário pode sair do programa a qualquer momento sem precisar processar arquivos

---

## [1.1.0] - 2026-02-15

### ✨ Adicionado
- Interface colorida usando biblioteca `colorama`
- Barras de progresso durante o envio dos arquivos
- Separadores visuais coloridos para melhor organização
- Mensagens de status com cores (sucesso em verde, erro em vermelho, avisos em amarelo)
- Contador de arquivos em tempo real durante o processamento
- Versão exibida no cabeçalho do aplicativo

### 🔄 Modificado
- Renomeado `submit_nzbs.py` para `nzbgeek-post.py` (padronização com nome do projeto)
- Renomeado executável de `submit_nzbs.exe` para `nzbgeek-post.exe`
- Melhorado feedback visual em todas as etapas do processo
- Atualizada documentação com novo nome do arquivo
- Interface mais moderna e profissional

### 📦 Dependências
- Adicionada dependência `colorama>=0.4.6` para suporte a cores multiplataforma

### 🐛 Correções
- Melhor compatibilidade de cores no Windows
- Fallback gracioso quando colorama não está disponível

---

## [1.0.0] - 2026-02-14

### 🎉 Lançamento Inicial
- Script Python para submissão de arquivos NZB ao indexador NZBGeek
- Interface em modo console com ASCII art
- Seleção interativa de categorias
- Sistema de logs diários
- Movimentação automática de arquivos processados
- Configuração via variáveis de ambiente
- Modo loop para processamento contínuo
- Geração de executável Windows (.exe)
- Documentação completa em português
