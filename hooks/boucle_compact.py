# Hook UserPromptSubmit : detecte une boucle de compaction (>= 2 compactions en moins de 15 min) et demande a
# Claude de proposer la passation (skill `passation`) a Nolann au lieu de continuer a compacter. Une seule alerte
# par compaction. Ne bloque jamais le message.
import json
import os
import sys
from datetime import datetime

FENETRE = 900            # s entre deux compactions pour parler de boucle
QUEUE = 6_000_000        # octets lus en fin de transcript (le fichier peut faire 100+ Mo)
ETAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boucle_compact_etat.json")

try:
    data = json.load(sys.stdin)
    chemin = data["transcript_path"]
    taille = os.path.getsize(chemin)
    with open(chemin, "rb") as f:
        f.seek(max(0, taille - QUEUE))
        brut = f.read().decode("utf-8", errors="ignore")
except Exception:
    sys.exit(0)

dates = []
for l in brut.splitlines():
    if '"compact_boundary"' not in l:
        continue
    try:
        e = json.loads(l)
        dates.append(datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).timestamp())
    except Exception:
        continue

if len(dates) < 2 or dates[-1] - dates[-2] > FENETRE:
    sys.exit(0)

try:
    etat = json.load(open(ETAT, encoding="utf-8"))
except Exception:
    etat = {}
cle = data.get("session_id", chemin)
if etat.get(cle) == dates[-1]:
    sys.exit(0)
etat[cle] = dates[-1]
etat = dict(list(etat.items())[-50:])
json.dump(etat, open(ETAT, "w", encoding="utf-8"))

print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": (
    "BOUCLE DE COMPACTION detectee : deux compactions a moins de 15 min d'ecart (le contexte repart trop haut "
    "pour tenir sous le seuil). Compacter encore ne sert a rien. Ne pose AUCUNE question : reecris SUIVI.md "
    "propre si ce n'est pas fait, puis FAIS la passation toi-meme (skill `passation`, mode autonome, sans pop-up) et continue a "
    "travailler dans la nouvelle conversation. Dis-le a Nolann en une ligne apres coup. "
    "Si la creation est refusee, ecris SUIVI.md et continue.")}}))
sys.exit(0)
