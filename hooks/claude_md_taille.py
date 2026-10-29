# Hook UserPromptSubmit : si le CLAUDE.md du projet depasse la limite, le signaler a Claude
# (sans tokens tant qu'il est sous la limite). Le menage suit le skill « menage-claude-md ».
import json
import os
import sys

LIMITE = 15_000  # octets (~150 lignes de 100 caracteres)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cwd = data.get("cwd") or os.getcwd()
for nom in ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md")):
    chemin = os.path.join(cwd, nom)
    if os.path.isfile(chemin):
        taille = os.path.getsize(chemin)
        if taille > LIMITE:
            msg = (f"CLAUDE.md du projet trop gros : {taille // 1000} Ko (limite {LIMITE // 1000} Ko), "
                   f"{chemin}. A la fin de la tache en cours (pas pendant un workflow ou un agent qui "
                   "ecrit dedans), lancer le skill menage-claude-md.")
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
        break
sys.exit(0)
