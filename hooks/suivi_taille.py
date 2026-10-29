# Hook UserPromptSubmit : si le SUIVI.md du projet depasse la limite, le signaler a Claude
# UNE SEULE FOIS par conversation (sans tokens tant qu'il est sous la limite).
# Le menage = archiver le fini dans docs/chantiers/<chantier>.md (voir CLAUDE.md global).
import json
import os
import sys
import tempfile

LIMITE = 8_000  # octets

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cwd = data.get("cwd") or os.getcwd()
session = str(data.get("session_id") or "inconnue")
marque = os.path.join(tempfile.gettempdir(), f"suivi_taille_{session}.flag")

for nom in ("SUIVI.md", os.path.join("docs", "SUIVI.md")):
    chemin = os.path.join(cwd, nom)
    if os.path.isfile(chemin):
        taille = os.path.getsize(chemin)
        if taille > LIMITE and not os.path.exists(marque):
            msg = (f"SUIVI.md trop gros : {taille // 1000} Ko (limite {LIMITE // 1000} Ko), {chemin}. "
                   "A la fin de la tache en cours (pas pendant un agent qui ecrit dedans), deplacer ce qui "
                   "est fini et l'historique dans docs/chantiers/<chantier>.md (renvoi d'une ligne dans le "
                   "SUIVI), sans rien supprimer, puis reecrire le SUIVI propre.")
            try:
                open(marque, "w").close()
            except OSError:
                pass
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
        break
sys.exit(0)
