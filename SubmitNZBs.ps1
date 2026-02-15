# -------------------- CONFIGURAÇÃO --------------------
$nzbSubmissionFolder = "F:\.nzb\NZBs_Gerados"
$nzbSubmissionFolderComplete = "F:\.nzb\Submetidos"
$myApiKey = "MMf77lARapmzxbATtZn9vtTqwDraCAGE"
$logFolder = "F:\.nzb\Logs"
$logFile = Join-Path -Path $logFolder -ChildPath "submit_log_$(Get-Date -Format 'dd-MM-yyyy').txt"
$categoryId = "4010"  # PC/0day

# -------------------- VALIDAÇÃO DE PASTAS (executa apenas uma vez) --------------------
if (-not (Test-Path -Path $nzbSubmissionFolder -PathType Container)) {
    Write-Host "[ERRO] Pasta de NZBs não encontrada: '$nzbSubmissionFolder'" -ForegroundColor Red
    Pause
    exit 1
}

if (-not (Test-Path -Path $nzbSubmissionFolderComplete -PathType Container)) {
    Write-Host "[INFO] Criando pasta de NZBs processados..." -ForegroundColor Yellow
    try {
        New-Item -Path $nzbSubmissionFolderComplete -ItemType Directory | Out-Null
    }
    catch {
        Write-Host "[ERRO] Não foi possível criar a pasta: '$nzbSubmissionFolderComplete'. Erro: $($_.Exception.Message)" -ForegroundColor Red
        Pause
        exit 1
    }
}

if (-not (Test-Path -Path $logFolder -PathType Container)) {
    try {
        New-Item -Path $logFolder -ItemType Directory | Out-Null
    }
    catch {
        Write-Host "[ERRO] Não foi possível criar a pasta de logs: '$logFolder'. Erro: $($_.Exception.Message)" -ForegroundColor Red
        Pause
        exit 1
    }
}

# -------------------- FUNÇÃO PARA PROCESSAR NZBs --------------------
function Process-NZBs {
    param()

    # -------------------- CABEÇALHO --------------------
    Clear-Host
    $headerWidth = 70
    $line = "=" * $headerWidth
    $centeredText = "ENVIO DE NZBs PARA NZBGEEK - INÍCIO"
    $padding = ($headerWidth - $centeredText.Length) / 2
    $leftPadding = [math]::Floor($padding)
    $rightPadding = [math]::Ceiling($padding)
    $formattedCenteredText = (" " * $leftPadding) + $centeredText + (" " * $rightPadding)

    Write-Host $line
    Write-Host ""
    Write-Host ""
    Write-Host "        ███████╗██╗   ██╗██╗     ██╗     ███████╗██████╗  " -ForegroundColor Green
    Write-Host "        ██╔════╝██║   ██║██║     ██║     ██╔════╝██╔══██╗ " -ForegroundColor Green
    Write-Host "        █████╗  ██║   ██║██║     ██║     █████╗  ██████╔╝ " -ForegroundColor Green
    Write-Host "        ██╔══╝  ██║   ██║██║     ██║     ██╔══╝  ██╔══██╗ " -ForegroundColor Green
    Write-Host "        ██║     ╚██████╔╝███████╗███████╗███████╗██║  ██║ " -ForegroundColor Green
    Write-Host "        ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ " -ForegroundColor Green
    Write-Host ""
    Write-Host (" " * 8) + "================= CONFIGURAÇÕES =================" -ForegroundColor Cyan
    Write-Host (" " * 8) + "📂 Pasta de origem:    " -NoNewline -ForegroundColor Yellow; Write-Host "$nzbSubmissionFolder" -ForegroundColor Gray
    Write-Host (" " * 8) + "📁 Pasta de destino:   " -NoNewline -ForegroundColor Yellow; Write-Host "$nzbSubmissionFolderComplete" -ForegroundColor Gray
    Write-Host (" " * 8) + "📝 Log do dia:         " -NoNewline -ForegroundColor Yellow; Write-Host "$logFile" -ForegroundColor Gray
    Write-Host (" " * 8) + "🔖 Categoria:          " -NoNewline -ForegroundColor Yellow; Write-Host "PC/0day (ID: $categoryId)" -ForegroundColor Gray
    Write-Host (" " * 8) + "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host ""

    # -------------------- CONFIRMAÇÃO DE ENVIO --------------------
    Write-Host ""
    Write-Host "Pressione ENTER para iniciar o envio dos arquivos NZB, ou feche esta janela para cancelar." -ForegroundColor Yellow
    Read-Host | Out-Null
    Write-Host ""

    # -------------------- PROCESSAMENTO --------------------
    $count = 0
    $found = $false

    $nzbFiles = Get-ChildItem -Path $nzbSubmissionFolder -Filter "*.nzb" -File

    if ($nzbFiles.Count -eq 0) {
        $found = $false
        Write-Host "Nenhum arquivo NZB encontrado para enviar." -ForegroundColor Yellow
    }
    else {
        $found = $true
        foreach ($file in $nzbFiles) {
            Write-Host "Enviando: $($file.Name)" -ForegroundColor Cyan
            $logEntry = "$(Get-Date -Format 'dd-MM-yyyy HH:mm:ss') Enviando: $($file.Name) (Categoria: $categoryId)"
            $logEntry | Out-File -FilePath $logFile -Append -Encoding UTF8

            try {
                # Construir o formulário multipart
                $boundary = [System.Guid]::NewGuid().ToString()
                $LF = "`r`n"
                
                $url = "https://api.nzbgeek.info/submit?apikey=$myApiKey"
                $fileBytes = [System.IO.File]::ReadAllBytes($file.FullName)
                $fileName = [System.IO.Path]::GetFileName($file.FullName)
                
                $bodyLines = (
                    "--$boundary",
                    "Content-Disposition: form-data; name=`"nzb`"; filename=`"$fileName`"",
                    "Content-Type: application/x-nzb$LF",
                    [System.Text.Encoding]::UTF8.GetString($fileBytes),
                    "--$boundary",
                    "Content-Disposition: form-data; name=`"category`"$LF",
                    "$categoryId",
                    "--$boundary--$LF"
                ) -join $LF
                
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($bodyLines)
                
                $webRequest = [System.Net.WebRequest]::Create($url)
                $webRequest.Method = "POST"
                $webRequest.ContentType = "multipart/form-data; boundary=$boundary"
                $webRequest.ContentLength = $bytes.Length
                $webRequest.UserAgent = "NZBUploader"
                
                $requestStream = $webRequest.GetRequestStream()
                $requestStream.Write($bytes, 0, $bytes.Length)
                $requestStream.Close()
                
                $response = $webRequest.GetResponse()
                $responseStream = $response.GetResponseStream()
                $streamReader = New-Object System.IO.StreamReader($responseStream)
                $responseString = $streamReader.ReadToEnd()
                $streamReader.Close()
                $response.Close()
                
                $responseString | Out-File -FilePath $logFile -Append -Encoding UTF8
                "" | Out-File -FilePath $logFile -Append -Encoding UTF8

                # MOVER ARQUIVO APÓS ENVIO BEM-SUCEDIDO
                try {
                    $destinationPath = Join-Path -Path $nzbSubmissionFolderComplete -ChildPath $file.Name

                    # Remover arquivo existente no destino se necessário
                    if (Test-Path -Path $destinationPath) {
                        Remove-Item -Path $destinationPath -Force
                    }

                    # Mover o arquivo para pasta de processados
                    Move-Item -Path $file.FullName -Destination $destinationPath -Force
                    Write-Host "✅ Movido para: $destinationPath" -ForegroundColor DarkGray
                }
                catch {
                    Write-Host "[ERRO] Falha ao mover $($file.Name): $($_.Exception.Message)" -ForegroundColor Red
                    "$(Get-Date -Format 'dd-MM-yyyy HH:mm:ss') [ERRO] Falha ao mover $($file.Name). Erro: $($_.Exception.Message)" | Out-File -FilePath $logFile -Append -Encoding UTF8
                }

                $count++

            }
            catch {
                $errorDetails = $_.Exception.Message
                if ($_.Exception.Response) {
                    $errorStream = $_.Exception.Response.GetResponseStream()
                    $streamReader = New-Object System.IO.StreamReader($errorStream)
                    $errorDetails = $streamReader.ReadToEnd()
                    $streamReader.Close()
                }
                
                Write-Host "[ERRO] Falha ao enviar $($file.Name). Erro: $errorDetails" -ForegroundColor Red
                "$(Get-Date -Format 'dd-MM-yyyy HH:mm:ss') [ERRO] Falha ao enviar $($file.Name). Erro: $errorDetails" | Out-File -FilePath $logFile -Append -Encoding UTF8
                "" | Out-File -FilePath $logFile -Append -Encoding UTF8
            }
        }
    }

    # -------------------- FINALIZAÇÃO --------------------
    if ($found) {
        Write-Host ""
        Write-Host "Total de arquivos enviados: $count" -ForegroundColor Green
        Write-Host "Log completo salvo em: $logFile" -ForegroundColor Green
    }

    Write-Host $line
    Write-Host "          PROCESSAMENTO CONCLUÍDO"
    Write-Host $line
}

# -------------------- LOOP PRINCIPAL --------------------
do {
    # Executa o processamento principal
    Process-NZBs

    # Pergunta se deseja verificar novamente
    Write-Host ""
    Write-Host "O que deseja fazer agora?" -ForegroundColor Cyan
    Write-Host "1 - Verificar novamente por novos NZBs" -ForegroundColor Yellow
    Write-Host "0 - Sair" -ForegroundColor Yellow
    Write-Host ""
    
    $choice = Read-Host "Digite sua opção (0-1)"
    
    # Valida a entrada
    while ($choice -notmatch '^[01]$') {
        Write-Host "Opção inválida. Por favor digite 0 ou 1." -ForegroundColor Red
        $choice = Read-Host "Digite sua opção (0-1)"
    }
    
} while ($choice -eq '1')

Write-Host ""
Write-Host "Script finalizado. Pressione qualquer tecla para sair..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')