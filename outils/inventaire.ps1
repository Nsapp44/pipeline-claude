# Inventaire de la configuration Claude (CLAUDE.md, skills, agents, hooks, routines) + comparaison avec le dernier relevé.
# Usage : powershell -File inventaire.ps1 [-Update] [-Extra "D:\autre\.claude"]
# Sans -Update : affiche seulement ajouts / modifications / suppressions depuis le dernier relevé.
# Avec -Update : enregistre le relevé courant (à faire APRÈS le point, une fois les changements analysés).
param([switch]$Update, [string[]]$Extra = @())
$snap = 'C:\pipeline\docs\inventaire.json'
$racines = @("$env:USERPROFILE\.claude") + $Extra
$now = @{}
foreach ($r in $racines) {
  if (-not (Test-Path $r)) { continue }
  $cibles = @()
  $cibles += Get-Item "$r\CLAUDE.md", "$r\settings.json" -ErrorAction SilentlyContinue
  foreach ($sous in 'skills', 'agents', 'hooks', 'scheduled-tasks') {
    if (Test-Path "$r\$sous") { $cibles += Get-ChildItem "$r\$sous" -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in '.md', '.py', '.sh', '.ps1', '.json' } }
  }
  foreach ($f in $cibles) {
    $now[$f.FullName] = @{ hash = (Get-FileHash $f.FullName -Algorithm SHA256).Hash.Substring(0, 12); date = $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm') }
  }
}
$old = @{}
if (Test-Path $snap) { (Get-Content $snap -Raw | ConvertFrom-Json).PSObject.Properties | ForEach-Object { $old[$_.Name] = $_.Value } }
$ajout = $now.Keys | Where-Object { -not $old.ContainsKey($_) }
$suppr = $old.Keys | Where-Object { -not $now.ContainsKey($_) }
$modif = $now.Keys | Where-Object { $old.ContainsKey($_) -and $old[$_].hash -ne $now[$_].hash }
"AJOUTES ($(@($ajout).Count))";    $ajout | Sort-Object | ForEach-Object { "  + $_  [$($now[$_].date)]" }
"MODIFIES ($(@($modif).Count))";   $modif | Sort-Object | ForEach-Object { "  ~ $_  [$($now[$_].date)]" }
"SUPPRIMES ($(@($suppr).Count))";  $suppr | Sort-Object | ForEach-Object { "  - $_" }
if ($Update) { $now | ConvertTo-Json -Depth 4 | Set-Content $snap -Encoding utf8; "Relevé enregistré : $snap ($($now.Count) fichiers)" }
