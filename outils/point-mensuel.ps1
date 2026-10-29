Start-Process notepad.exe 'C:\pipeline\docs\point-mensuel.md'
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show('Point mensuel pipeline : alleger les regles qui brident les nouveaux modeles (30 min). Check-list ouverte.', 'Point mensuel pipeline IA') | Out-Null
