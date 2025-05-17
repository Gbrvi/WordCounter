$projectPath = "C:\Users\gvalm\Documents\Projetos\WordCounter"
$envActivate = "$projectPath\myenv\Scripts\Activate.ps1"
& $envActivate
Set-Location $projectPath

$numWorkers = 5
for ($i = 0; $i -lt $numWorkers; $i++) {
    $name = "worker-$i"
    Start-Process -NoNewWindow -FilePath "python.exe" -ArgumentList ".\worker.py $name"
}
