# Hook UserPromptSubmit : apres une pause > 1 h dans une conversation lourde, le cache du fil est perdu et le
# message de reprise recree tout le contexte (~2 x sa taille). Le 1er message est bloque (rien n'est paye) avec
# un avertissement ; si on renvoie un message, il passe (on continue et on paye).
import json
import os
import sys
import time
from datetime import datetime

PAUSE = 3600       # s, duree du cache du fil principal
SEUIL = 80_000     # tokens de contexte en dessous desquels la reprise coute peu
ETAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pause_longue_etat.json")

try:
    data = json.load(sys.stdin)
    chemin = data["transcript_path"]
except Exception:
    sys.exit(0)

# Seuls les messages TAPES par Nolann sont bloques. Tout ce que Claude s'est auto-programme ou recoit d'une
# autre source passe : taches planifiees, reveils (/loop, ScheduleWakeup), notifications, messages entre
# conversations, evenements du bureau. Un retour de rendu auto-programme ne doit jamais etre bloque.
_p = str(data.get("prompt", "")).lstrip()
_AUTO = ("<scheduled-task", "<task-notification", "<cross-session-message", "[Cross-session",
         "Another Claude session", "The coordinator sent", "<<autonomous-loop", "<side-sessions-event",
         "<ci-monitor-event", "<system-reminder", "[SYSTEM NOTIFICATION", "<command-name>", "<loop")
if _p.startswith(_AUTO) or "<cross-session-message" in _p or "This is an automated run" in _p[:400]:
    sys.exit(0)

dernier, ctx = None, 0
try:
    with open(chemin, encoding="utf-8", errors="ignore") as f:
        lignes = f.readlines()[-400:]
    for l in reversed(lignes):
        try:
            e = json.loads(l)
        except Exception:
            continue
        m = e.get("message") if isinstance(e.get("message"), dict) else {}
        u = m.get("usage")
        if u and e.get("timestamp"):
            dernier = datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).timestamp()
            ctx = (u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                   + u.get("input_tokens", 0))
            break
except Exception:
    sys.exit(0)

if not dernier or ctx < SEUIL or time.time() - dernier < PAUSE:
    sys.exit(0)

try:
    etat = json.load(open(ETAT, encoding="utf-8"))
except Exception:
    etat = {}
cle = data.get("session_id", chemin)
if etat.get(cle) == dernier:   # deja prevenu pour cette pause : on laisse passer
    sys.exit(0)
etat[cle] = dernier
etat = dict(list(etat.items())[-50:])
json.dump(etat, open(ETAT, "w", encoding="utf-8"))

h = (time.time() - dernier) / 3600
print(json.dumps({"decision": "block", "reason": (
    f"Pause de {h:.1f} h : le cache de cette conversation ({ctx // 1000} k) est perdu, ce message le "
    f"recreerait en entier (~{2 * ctx // 1000} k equivalent). Moins cher : nouvelle conversation avec "
    "« lis SUIVI.md et continue » (~15-30 k). Pour continuer ici quand meme, renvoie ton message "
    "(il passera), par exemple « ecris SUIVI.md » s'il n'existe pas.")}))
sys.exit(0)
