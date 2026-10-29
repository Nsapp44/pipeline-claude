#!/usr/bin/env bash
# Usage : bash scan.sh <dossier du depot git>
# Cherche les mots interdits (mots-interdits.txt, hors depot) dans l'arbre, tout l'historique,
# les messages de commit et les auteurs. Code de sortie 1 si trouvaille.
set -u
repo="${1:-.}"
words="$(cd "$(dirname "$0")" && pwd)/mots-interdits.txt"
cd "$repo" || exit 2
pat=$(grep -v '^\s*#' "$words" | sed '/^\s*$/d' | paste -sd'|')
[ -z "$pat" ] && { echo "liste vide"; exit 2; }
bad=0
echo "== Arbre actuel"
out=$(git grep -n -I -i -E "$pat" -- . | cut -c1-200); [ -n "$out" ] && { echo "$out"; bad=1; }
echo "== Historique (tous commits, toutes branches)"
for c in $(git rev-list --all); do
  git grep -l -I -i -E "$pat" "$c" -- . 2>/dev/null | sed "s/^/${c:0:7} /"
done | sort -u | tee /tmp/scan_hist.$$ | head -30
[ -s /tmp/scan_hist.$$ ] && bad=1; rm -f /tmp/scan_hist.$$
echo "== Messages de commit et auteurs"
out=$(git log --all --format='%h %an <%ae> %s%n%b' | grep -i -E "$pat"); [ -n "$out" ] && { echo "$out"; bad=1; }
echo "== Chemins personnels / secrets courants"
out=$(git grep -n -I -E 'C:\\Users\\|/Users/[A-Za-z]+/|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}' -- . | cut -c1-160); [ -n "$out" ] && { echo "$out"; bad=1; }
if [ $bad -eq 0 ]; then echo "PROPRE"; else echo "TROUVE : corriger (si l'historique est touche : reecrire + push force, jamais sans accord de Nolann)"; fi
exit $bad
