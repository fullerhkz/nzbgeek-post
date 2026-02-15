# NZBGeek Post

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Script Python para submeter arquivos `.nzb` para o indexador **NZBGeek** através da API oficial.

## 📋 Índice

- [Descrição](#-descrição)
- [Características](#-características)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
  - [Variáveis de Ambiente](#variáveis-de-ambiente)
  - [Como Configurar no Windows](#como-configurar-no-windows)
- [Uso](#-uso)
- [Categorias Disponíveis](#-categorias-disponíveis)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API do NZBGeek](#-api-do-nzbgeek)
- [Logs](#-logs)
- [Solução de Problemas](#-solução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## 🎯 Descrição

Este script foi desenvolvido para automatizar o processo de submissão de arquivos NZB para o indexador NZBGeek. Ele oferece uma interface simples e amigável para enviar múltiplos arquivos com suporte a categorização e logging completo.

**Principais funcionalidades:**
- ✅ Submissão automática de múltiplos arquivos NZB
- ✅ Seleção interativa de categorias
- ✅ Movimentação automática de arquivos processados
- ✅ Sistema de logs detalhado
- ✅ Interface com menu interativo
- ✅ Configuração via variáveis de ambiente
- ✅ Tratamento de erros robusto

## ✨ Características

- **Interface Visual**: ASCII art e interface colorida no terminal
- **Segurança**: API key armazenada em variável de ambiente (não no código)
- **Organização**: Move automaticamente arquivos processados para pasta separada
- **Logs Diários**: Registra todas as operações com timestamp
- **Categorização**: Suporte completo às categorias da API do NZBGeek
- **Execução Simples**: Basta dar duplo clique no arquivo `.bat`
- **Modo Loop**: Opção de processar múltiplas vezes sem reiniciar

## 📦 Pré-requisitos

### Software Necessário

1. **Python 3.7 ou superior**
   - Download: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANTE**: Durante a instalação, marque a opção "Add Python to PATH"

2. **Git** (opcional, para clonar o repositório)
   - Download: [https://git-scm.com/downloads](https://git-scm.com/downloads)

3. **Conta no NZBGeek**
   - Cadastre-se em: [https://nzbgeek.info](https://nzbgeek.info)
   - Obtenha sua API key no painel de controle

### Dependências Python

- `requests` >= 2.31.0

## 🚀 Instalação

### Método 1: Clonando o Repositório (Recomendado)

```bash
git clone https://github.com/seu-usuario/nzbgeek-post.git
cd nzbgeek-post
pip install -r requirements.txt
```

### Método 2: Download Manual

1. Baixe o repositório como ZIP
2. Extraia os arquivos em uma pasta de sua preferência
3. Abra o terminal na pasta extraída
4. Execute: `pip install -r requirements.txt`

### Método 3: Instalação Manual das Dependências

Se preferir, instale apenas o pacote necessário:

```bash
pip install requests
```

## ⚙️ Configuração

### Variáveis de Ambiente

O script utiliza variáveis de ambiente para configuração. São necessárias **4 variáveis**:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `NZBGEEK_API_KEY` | Sua chave de API do NZBGeek | `MMf77lARapmzxbATtZn9vtTqwDraCAGE` |
| `NZBGEEK_SUBMISSION_FOLDER` | Pasta contendo os arquivos .nzb para enviar | `C:\NZBs\Para_Enviar` |
| `NZBGEEK_COMPLETE_FOLDER` | Pasta para onde os arquivos serão movidos após o envio | `C:\NZBs\Enviados` |
| `NZBGEEK_LOG_FOLDER` | Pasta onde os logs serão salvos | `C:\NZBs\Logs` |

### Como Configurar no Windows

#### Método 1: Via Linha de Comando (CMD)

Abra o **Prompt de Comando** como Administrador e execute:

```cmd
setx NZBGEEK_API_KEY "sua_api_key_aqui"
setx NZBGEEK_SUBMISSION_FOLDER "C:\caminho\para\pasta\origem"
setx NZBGEEK_COMPLETE_FOLDER "C:\caminho\para\pasta\destino"
setx NZBGEEK_LOG_FOLDER "C:\caminho\para\pasta\logs"
```

**Exemplo real:**

```cmd
setx NZBGEEK_API_KEY "MMf77lARapmzxbATtZn9vtTqwDraCAGE"
setx NZBGEEK_SUBMISSION_FOLDER "F:\.nzb\NZBs_Gerados"
setx NZBGEEK_COMPLETE_FOLDER "F:\.nzb\Submetidos"
setx NZBGEEK_LOG_FOLDER "F:\.nzb\Logs"
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
[Environment]::SetEnvironmentVariable("NZBGEEK_API_KEY", "sua_api_key_aqui", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_SUBMISSION_FOLDER", "C:\caminho\para\pasta\origem", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_COMPLETE_FOLDER", "C:\caminho\para\pasta\destino", "User")
[Environment]::SetEnvironmentVariable("NZBGEEK_LOG_FOLDER", "C:\caminho\para\pasta\logs", "User")
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

### Execução Simplificada (Duplo Clique)

1. Localize o arquivo `submit_nzbs.bat` na pasta do projeto
2. Dê **duplo clique** no arquivo
3. Siga as instruções na tela

### Execução via Terminal

**CMD:**
```cmd
cd caminho\para\nzbgeek-post
submit_nzbs.bat
```

**PowerShell:**
```powershell
cd caminho\para\nzbgeek-post
.\submit_nzbs.bat
```

**Python Direto:**
```bash
python submit_nzbs.py
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

Você pode especificar uma subcategoria exata digitando o ID completo quando solicitado. Consulte a página de capacidades da API do NZBGeek para a lista completa de subcategorias.

## 📁 Estrutura do Projeto

```
nzbgeek-post/
│
├── submit_nzbs.py          # Script principal em Python
├── submit_nzbs.bat         # Launcher para Windows (duplo clique)
├── requirements.txt        # Dependências Python
├── README.md              # Este arquivo
├── LICENSE                # Licença do projeto
│
├── SubmitNZBs.ps1         # Script PowerShell original (referência)
└── SubmitNZBs.bat         # Batch original (referência)
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
14-02-2026 22:15:32 Movido para: F:\.nzb\Submetidos\arquivo1.nzb
14-02-2026 22:15:35 Enviando: arquivo2.nzb (Categoria: 4010)
14-02-2026 22:15:37 [ERRO] Falha no envio: Connection timeout
```

## 🔧 Solução de Problemas

### Erro: "Python não encontrado"

**Causa**: Python não está instalado ou não está no PATH do sistema.

**Solução**:
1. Baixe e instale o Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Durante a instalação, marque "Add Python to PATH"
3. Reinicie o terminal

### Erro: "API key não encontrada"

**Causa**: A variável de ambiente `NZBGEEK_API_KEY` não está configurada.

**Solução**:
1. Configure a variável conforme a seção [Configuração](#configuração)
2. Feche e abra novamente o terminal
3. Verifique a configuração com: `echo %NZBGEEK_API_KEY%`

### Erro: "Pasta de submissão não encontrada"

**Causa**: O caminho configurado em `NZBGEEK_SUBMISSION_FOLDER` não existe.

**Solução**:
1. Verifique se o caminho está correto
2. Crie a pasta manualmente
3. Reconfigure a variável de ambiente com o caminho correto

### Erro: "ModuleNotFoundError: No module named 'requests'"

**Causa**: A biblioteca `requests` não está instalada.

**Solução**:
```bash
pip install requests
```

ou

```bash
pip install -r requirements.txt
```

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

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

### Sugestões de Melhorias

- [ ] Suporte a arquivos NFO
- [ ] Interface gráfica (GUI)
- [ ] Modo batch não-interativo (para automação)
- [ ] Configuração via arquivo .ini ou .env
- [ ] Suporte a múltiplos indexadores
- [ ] Retry automático em caso de falha
- [ ] Notificações desktop

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Consulte a documentação da API do NZBGeek: [https://nzbgeek.info/api](https://nzbgeek.info/api)
3. Abra uma issue no GitHub

---

## 🌟 Agradecimentos

- Script original em PowerShell desenvolvido por [autor original]
- API fornecida por [NZBGeek](https://nzbgeek.info)
- Biblioteca `requests` pelos desenvolvedores do projeto Requests

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade Usenet**

[⬆ Voltar ao topo](#nzbgeek-post)

</div>
