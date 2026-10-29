"""Status line Claude Code : relève la conso 5 h / 7 j pour Bureau entreprise.

Claude Code envoie sur stdin un JSON contenant rate_limits (abonnés Pro/Max).
On l'écrit dans ~/.claude/bureau_conso.json (lu par le panneau mural) et on
affiche une ligne courte dans la barre d'état. Aucun réseau, aucun jeton.
"""

import json
import os
import sys
import time
from pathlib import Path

OUT = Path.home() / ".claude" / "bureau_conso.json"


def main() -> None:
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig") or "{}")
    except ValueError:
        data = {}
    limits = data.get("rate_limits") or {}
    keep = {k: limits[k] for k in ("five_hour", "seven_day") if isinstance(limits.get(k), dict)}

    if keep:
        keep["updated_at"] = int(time.time())
        tmp = OUT.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(keep), encoding="utf-8")
            os.replace(tmp, OUT)
        except OSError:
            pass

    parts = []
    for key, name in (("five_hour", "5h"), ("seven_day", "7j")):
        win = keep.get(key)
        if win and win.get("used_percentage") is not None:
            parts.append(f"{name} {round(win['used_percentage'])}%")
    ctx = (data.get("context_window") or {}).get("used_percentage")
    if ctx is not None:
        parts.append(f"ctx {round(ctx)}%")
    print(" | ".join(parts))


if __name__ == "__main__":
    main()
