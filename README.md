# NZBGeek Post

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![English Version](https://img.shields.io/badge/🇺🇸_version-english-blue)](https://github.com/fullerhkz/nzbgeek-post-en)

Script Python para submeter arquivos `.nzb` para o indexador **NZBGeek** através da API oficial.

> **🇺🇸 English Version:** [nzbgeek-post-en](https://github.com/fullerhkz/nzbgeek-post-en)

## 📋 Índice

- [Descrição](#-descrição)
- [Características](#-características)
- [Download](#-download)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
  - [Variáveis de Ambiente](#variáveis-de-ambiente)
  - [Como Configurar no Windows](#como-configurar-no-windows)
- [Uso](#-uso)
- [Categorias Disponíveis](#-categorias-disponíveis)
- [Compilando o Executável](#-compilando-o-executável)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API do NZBGeek](#-api-do-nzbgeek)
- [Logs](#-logs)
- [Solução de Problemas](#-solução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

> [!NOTE]
> ## 🎯 Descrição
> 
> Este script automatiza o envio de arquivos `.nzb` para o **NZBGeek**, um popular indexador da rede descentralizada Usenet. Desenvolvido para facilitar a contribuição com a comunidade, oferece uma interface moderna e colorida para submissão em lote, seleção interativa de categorias, logs detalhados e feedback visual em tempo real.
> 
> **Ideal para:** Usuários da Usenet que desejam contribuir com o indexador NZBGeek de forma rápida e organizada.

**Principais funcionalidades:**
- ✅ Interface colorida e moderna com barras de progresso (v1.1.0+)
- ✅ Submissão automática de múltiplos arquivos NZB
- ✅ Seleção interativa de categorias
- ✅ Movimentação automática de arquivos processados
- ✅ Sistema de logs detalhado com timestamps
- ✅ Feedback visual em tempo real com cores contextuais
- ✅ Configuração via variáveis de ambiente (segura)
- ✅ Tratamento de erros robusto
- ✅ Executável standalone (.exe) disponível

## ✨ Características

- **Interface Visual Colorida**: ASCII art com cores vibrantes e barras de progresso (v1.1.0+)
- **Segurança**: API key armazenada em variável de ambiente (não no código)
- **Organização**: Move automaticamente arquivos processados para pasta separada
- **Logs Diários**: Registra todas as operações com timestamp
- **Categorização**: Suporte completo às categorias da API do NZBGeek
- **Execução Simples**: Duplo clique no arquivo `.py` ou `.exe`
- **Modo Loop**: Opção de processar múltiplas vezes sem reiniciar
- **Multiplataforma**: Suporte a cores no Windows, Linux e macOS

## 🆕 Novidades v1.1.0

- 🎨 **Interface totalmente renovada** com cores vibrantes
- 📊 **Barras de progresso** durante o envio dos arquivos
- 🌈 **Separadores coloridos** para melhor organização visual
- ✨ **Mensagens de status** destacadas com cores (sucesso, erro, aviso)
- 🎯 **Contador de arquivos** em tempo real durante o processamento
- 🔄 **Melhor feedback visual** em todas as etapas do processo

## 📥 Download

### Executável Windows (.exe) - Recomendado

Para usuários que não querem instalar Python, baixe o executável pronto para uso:

**[📦 Download da Última Versão (Releases)](https://github.com/fullerhkz/nzbgeek-post/releases/latest)**

- ✅ Não requer instalação do Python
- ✅ Arquivo único e portátil
- ✅ Pronto para usar
- 🎨 Interface colorida e moderna (v1.1.0+)

### Script Python (.py)

Para desenvolvedores ou quem prefere executar o código-fonte diretamente:

```bash
git clone https://github.com/fullerhkz/nzbgeek-post.git
```

## 📦 Pré-requisitos

### Para Executável (.exe)

- ✅ **Nenhum pré-requisito adicional**
- Apenas configure as variáveis de ambiente

### Para Script Python (.py)

1. **Python 3.7 ou superior**
   - Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"

2. **Git** (opcional, para clonar o repositório)
   - Download: [https://git-scm.com/downloads](https://git-scm.com/downloads)

3. **Dependências Python**:
   ```bash
   pip install -r requirements.txt
   ```

### Comum a Ambos

- **Conta no NZBGeek**
  - Cadastre-se em: [https://nzbgeek.info](https://nzbgeek.info)
  - Obtenha sua API key no painel de controle

## 🚀 Instalação

### Método 1: Usando o Executável (Recomendado para Usuários)

1. Baixe `nzbgeek-post.exe` da [página de releases](https://github.com/fullerhkz/nzbgeek-post/releases/latest)
2. Coloque o arquivo em uma pasta de sua preferência
3. Configure as variáveis de ambiente (veja abaixo)
4. Dê duplo clique no arquivo `.exe`

### Método 2: Clonando o Repositório (Para Desenvolvedores)

```bash
git clone https://github.com/fullerhkz/nzbgeek-post.git
cd nzbgeek-post
pip install -r requirements.txt
```

### Método 3: Download Manual do Script

1. Baixe o repositório como ZIP
2. Extraia os arquivos
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute: `python nzbgeek-post.py` ou dê duplo clique em `nzbgeek-post.py`

## ⚙️ Configuração

### Variáveis de Ambiente

O script utiliza variáveis de ambiente para configuração. São necessárias **4 variáveis**:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `NZBGEEK_API_KEY` | Sua chave de API do NZBGeek | `SuaAPIKeyAqui123456789` |
| `NZBGEEK_SUBMISSION_FOLDER` | Pasta contendo os arquivos .nzb para enviar | `C:\NZBs\Para_Enviar` |
| `NZBGEEK_COMPLETE_FOLDER` | Pasta para onde os arquivos serão movidos após o envio | `C:\NZBs\Enviados` |
| `NZBGEEK_LOG_FOLDER` | Pasta onde os logs serão salvos | `C:\NZBs\Logs` |

### Como Configurar no Windows

#### Método 1: Via Linha de Comando (CMD)

Abra o **Prompt de Comando** como Administrador e execute:

```cmd
setx NZBGEEK_API_KEY "SuaAPIKeyAqui123456789"
setx NZBGEEK_SUBMISSION_FOLDER "C:\Caminho\Para\Pasta\Origem"
setx NZBGEEK_COMPLETE_FOLDER "C:\Caminho\Para\Pasta\Destino"
setx NZBGEEK_LOG_FOLDER "C:\Caminho\Para\Pasta\Logs"
```

**Exemplo prático:**

```cmd
setx NZBGEEK_API_KEY "abc123def456ghi789jkl012mno345pqr"
setx NZBGEEK_SUBMISSION_FOLDER "C:\Users\SeuUsuario\NZBs\Enviar"
setx NZBGEEK_COMPLETE_FOLDER "C:\Users\SeuUsuario\NZBs\Enviados"
setx NZBGEEK_LOG_FOLDER "C:\Users\SeuUsuario\NZBs\Logs"
```

⚠️ **Importante**: Após configurar as variáveis, **feche e abra novamente o terminal** para que as mudanças tenham efeito.

#### Método 2: Via Interface Gráfica do Windows

1. Pressione `Win + Pause/Break` ou clique com botão direito em "Este Computador" → "Propriedades"
2. Clique em "Configurações avançadas do sistema"
3. Clique em "Variáveis de Ambiente"
4. Na seção "Variáveis do usuário", clique em "Novo"
5. Adicione cada variável:
   - **Nome da variável**: `NZBGEEK_API_KEY`
   - **Valor da variável**: Sua API key
6. Repita para as outras 3 variáveis
7. Clique em "OK" para salvar

#### Método 3: Via PowerShell

Abra o **PowerShell** como Administrador e execute:

```powershell
[Environment]::SetEnvironmentVariable("NZBGEEK_API_KEY", "SuaAPIKeyAqui123456789", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_SUBMISSION_FOLDER", "C:\Caminho\Para\Pasta\Origem", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_COMPLETE_FOLDER", "C:\Caminho\Para\Pasta\Destino", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_LOG_FOLDER", "C:\Caminho\Para\Pasta\Logs", "User")
```

### Verificando a Configuração

Para verificar se as variáveis foram configuradas corretamente, abra um **novo terminal** e execute:

**CMD:**
```cmd
echo %NZBGEEK_API_KEY%
```

**PowerShell:**
```powershell
$env:NZBGEEK_API_KEY
```

**Python:**
```python
python -c "import os; print(os.environ.get('NZBGEEK_API_KEY'))"
```

## 💻 Uso

### Usando o Executável (.exe)

1. Localize o arquivo `nzbgeek-post.exe`
2. Dê **duplo clique** no arquivo
3. Siga as instruções na tela

### Usando o Script Python (.py)

**Duplo Clique:**
- Simplesmente dê duplo clique em `nzbgeek-post.py`

**Via Terminal:**
```bash
python nzbgeek-post.py
```

### Fluxo de Uso

1. **Selecione a Categoria**: O script apresentará um menu com as categorias disponíveis
2. **Confirmação**: Pressione ENTER para iniciar o envio
3. **Processamento**: Os arquivos serão enviados um por um
4. **Movimentação**: Arquivos enviados com sucesso são movidos para a pasta de completos
5. **Logs**: Todas as operações são registradas no arquivo de log diário
6. **Repetir ou Sair**: Escolha se deseja processar mais arquivos ou encerrar

## 📂 Categorias Disponíveis

O script suporta as seguintes categorias principais:

| ID | Categoria | Descrição |
|----|-----------|-----------|
| 1xxx | Console | Jogos de console |
| 2xxx | Movies | Filmes |
| 3xxx | Audio | Músicas e áudios |
| 4xxx | PC | Aplicativos e jogos de PC |
| 5xxx | TV | Séries e programas de TV |
| 6xxx | XXX | Conteúdo adulto |
| 7xxx | Books | Livros e revistas |
| 8xxx | Other | Outros |

### Categoria Padrão

Se você pressionar `0` no menu de categorias, será utilizada a categoria padrão:
- **4010**: PC/0day (Aplicativos de PC)

### Subcategorias

Você pode especificar uma subcategoria exata digitando o ID completo quando solicitado. Consulte a [página de capacidades da API do NZBGeek](https://nzbgeek.info/api) para a lista completa de subcategorias.

## 🔨 Compilando o Executável

Se você quiser gerar seu próprio executável a partir do código-fonte:

```bash
# Instale as dependências (incluindo PyInstaller)
pip install -r requirements.txt

# Execute o script de build
python build_exe.py
```

O executável será criado em: `dist/nzbgeek-post.exe`

### Build Manual com PyInstaller

```bash
pyinstaller --onefile --console --name=nzbgeek-post nzbgeek-post.py
```

## 📁 Estrutura do Projeto

```
nzbgeek-post/
│
├── nzbgeek-post.py        # Script principal em Python
├── build_exe.py           # Script para gerar executável
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
├── CONTRIBUTING.md        # Guia de contribuição
├── LICENSE                # Licença do projeto (MIT)
├── .gitignore             # Arquivos ignorados pelo git
│

```

## 🔌 API do NZBGeek

### Endpoint

```
https://api.nzbgeek.info/submit
```

### Parâmetros

- `apikey` (obrigatório): Sua chave de API
- `cat` (opcional): ID da categoria
- `nzb` (obrigatório): Arquivo NZB (multipart/form-data)
- `nfo` (opcional): Arquivo NFO (multipart/form-data)

### Resposta de Sucesso

```json
{
  "response": {
    "@attributes": {
      "API": "OK",
      "REGISTER": "OK"
    }
  }
}
```

### Resposta com NFO

```json
{
  "response": {
    "@attributes": {
      "API": "OK",
      "NFO": "OK",
      "REGISTER": "OK"
    }
  }
}
```

## 📝 Logs

Os logs são salvos diariamente na pasta configurada em `NZBGEEK_LOG_FOLDER`.

### Formato do Nome do Arquivo

```
submit_log_DD-MM-YYYY.txt
```

Exemplo: `submit_log_14-02-2026.txt`

### Conteúdo do Log

```
14-02-2026 22:15:30 Enviando: arquivo1.nzb (Categoria: 4010)
14-02-2026 22:15:32 Resposta: {"response":{"@attributes":{"API":"OK","REGISTER":"OK"}}}
14-02-2026 22:15:32 Movido para: C:\NZBs\Enviados\arquivo1.nzb
14-02-2026 22:15:35 Enviando: arquivo2.nzb (Categoria: 4010)
14-02-2026 22:15:37 [ERRO] Falha no envio: Connection timeout
```

## 🔧 Solução de Problemas

### Erro: "Python não encontrado" (apenas para .py)

**Causa**: Python não está instalado ou não está no PATH do sistema.

**Solução**:
1. Baixe e instale o Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Durante a instalação, marque "Add Python to PATH"
3. Reinicie o terminal

**Alternativa**: Use o executável `.exe` que não requer Python instalado.

### Erro: "API key não encontrada"

**Causa**: A variável de ambiente `NZBGEEK_API_KEY` não está configurada.

**Solução**:
1. Configure a variável conforme a seção [Configuração](#configuração)
2. Feche e abra novamente o terminal/aplicação
3. Verifique a configuração com: `echo %NZBGEEK_API_KEY%`

### Erro: "Pasta de submissão não encontrada"

**Causa**: O caminho configurado em `NZBGEEK_SUBMISSION_FOLDER` não existe.

**Solução**:
1. Verifique se o caminho está correto
2. Crie a pasta manualmente
3. Reconfigure a variável de ambiente com o caminho correto

### Erro: "ModuleNotFoundError: No module named 'requests'" (apenas para .py)

**Causa**: A biblioteca `requests` não está instalada.

**Solução**:
```bash
pip install requests
```

ou

```bash
pip install -r requirements.txt
```

**Alternativa**: Use o executável `.exe` que já inclui todas as dependências.

### Avisos de SSL/Certificado

**Causa**: O script desabilita a verificação SSL para evitar problemas com certificados.

**Solução**: Isto é intencional e seguro para a API do NZBGeek. Se desejar habilitar a verificação SSL, edite a linha no script:
```python
response = requests.post(url, files=files, timeout=60, verify=True)
```

### Arquivos não são movidos após o envio

**Causa**: Permissões insuficientes ou pasta de destino em uso.

**Solução**:
1. Verifique as permissões das pastas
2. Certifique-se de que nenhum outro programa está usando os arquivos
3. Execute o script como Administrador se necessário

### Executável bloqueado pelo Windows Defender

**Causa**: Executáveis Python compilados às vezes são sinalizados como suspeitos.

**Solução**:
1. Adicione exceção no Windows Defender
2. Ou compile você mesmo usando `build_exe.py`
3. Ou use o script `.py` diretamente

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir.

### Como Criar uma Release

Para mantenedores do projeto:

1. Compile o executável: `python build_exe.py`
2. Teste o executável: `dist\nzbgeek-post.exe`
3. Crie uma tag: `git tag v1.1.0`
4. Push da tag: `git push origin v1.1.0`
5. Crie uma release no GitHub
6. Anexe o arquivo `nzbgeek-post.exe` à release

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Consulte a [documentação da API do NZBGeek](https://nzbgeek.info/api)
3. Abra uma [issue no GitHub](https://github.com/fullerhkz/nzbgeek-post/issues)

---

## 🌟 Agradecimentos

- Script original em PowerShell desenvolvido para uso pessoal
- API fornecida por [NZBGeek](https://nzbgeek.info)
- Biblioteca `requests` pelos desenvolvedores do projeto Requests
- PyInstaller para geração de executáveis

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade Usenet**

[⬆ Voltar ao topo](#nzbgeek-post)

</div>
