"""Hook PreToolUse : garde-fou sans coût de contexte.

- refuse l'écriture / édition d'un fichier .env (sauf .env.example / .env.sample) ;
- demande confirmation avant une suppression récursive (rm -r, Remove-Item -Recurse, rmdir /s, del /s).
Entrée : JSON sur stdin. Sortie : JSON permissionDecision (deny / ask) ou rien (laisser passer).
"""
import json
import os
import re
import sys


def decision(kind, raison):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": kind,
        "permissionDecisionReason": raison,
    }}, ensure_ascii=True))
    sys.exit(0)


def est_env(chemin):
    nom = os.path.basename(str(chemin)).lower()
    return nom.startswith(".env") and not nom.endswith((".example", ".sample", ".template"))


RM_RECURSIF = re.compile(
    r"(\brm\s+(-[a-z]*r[a-z]*|--recursive)\b)"
    r"|(\bRemove-Item\b[^\n;|]*-Recurse)"
    r"|(\brmdir\s+/s\b)|(\bdel\s+[^\n;|]*/s\b)"
    r"|(\bgit\s+clean\s+-[a-z]*f)",
    re.IGNORECASE,
)
ECRIT_ENV = re.compile(r"(>>?|\btee\b|\bsed\s+-i\b|Set-Content|Add-Content|Out-File)[^\n;|]*\.env\b(?!\.(example|sample|template))",
                       re.IGNORECASE)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    outil = data.get("tool_name", "")
    entree = data.get("tool_input") or {}
    if outil in ("Write", "Edit", "NotebookEdit"):
        if est_env(entree.get("file_path", "")):
            decision("deny", "Écriture dans un fichier .env bloquée par le garde-fou (secrets). À faire par Nolann.")
    elif outil in ("Bash", "PowerShell"):
        cmd = entree.get("command", "")
        if ECRIT_ENV.search(cmd):
            decision("deny", "Écriture dans un fichier .env bloquée par le garde-fou (secrets). À faire par Nolann.")
        if RM_RECURSIF.search(cmd):
            decision("ask", "Suppression récursive détectée : confirmer avant d'exécuter.")


main()
