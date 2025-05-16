# Caminho para o diretório do projeto
$projectPath = "C:\Users\gvalm\Documents\Projetos\WordCounter"

# Caminho para o ambiente virtual
$envActivate = "$projectPath\myenv\Scripts\Activate.ps1"

# Ativar ambiente virtual
& $envActivate

# Navegar até o diretório do projeto
Set-Location $projectPath

# Rodar o script 15 vezes com valores de 5555 a 5569
for ($i = 0; $i -lt 5; $i++) {
    $port = 5555 + $i
    Start-Process -NoNewWindow -FilePath "python.exe" -ArgumentList ".\worker.py $port"
}