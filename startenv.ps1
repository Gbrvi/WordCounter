# Caminho relativo para o script de ativação
$activateScript = Join-Path -Path $PSScriptRoot -ChildPath "myenv\Scripts\Activate.ps1"

# Verifica se o arquivo de ativação existe
if (Test-Path $activateScript) {
    # Executa o script de ativação
    & $activateScript
} else {
    Write-Host "Arquivo de ativação não encontrado em: $activateScript"
    Write-Host "Certifique-se de que o ambiente virtual está criado na pasta correta."
}