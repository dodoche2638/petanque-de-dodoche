#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
version=$(cat VERSION)
[[ "$version" =~ ^[1-9][0-9]*$ ]]
tag="v$version"
test -z "$(git status --porcelain)"
test "$(git branch --show-current)" = main
grep -q "^$tag ·" Historique-des-versions.txt
gh auth status
python3 scripts/build.py
git push origin main
if ! git show-ref --verify --quiet "refs/tags/$tag"; then
  git tag -a "$tag" -m "LA PETANQUE DE DODOCHE $tag"
fi
test "$(git rev-list -n 1 "$tag")" = "$(git rev-parse HEAD)"
git push origin "refs/tags/$tag"
notes=$(mktemp)
trap 'rm -f "$notes"' EXIT
awk -v tag="$tag" '$1==tag {show=1} show && /^v[0-9]/ && $1!=tag {exit} show {print}' Historique-des-versions.txt >"$notes"
if ! gh release view "$tag" >/dev/null 2>&1; then
  gh release create "$tag" --verify-tag --draft --title "LA PETANQUE DE DODOCHE $tag" --notes-file "$notes"
fi
test "$(gh release view "$tag" --json isDraft --jq .isDraft)" = true
gh release upload "$tag" --clobber "dist/Dodoche-$tag.apk" "dist/Dodoche-$tag.zip" "dist/Petanque-de-Dodoche-Windows-$tag.zip" windows/Dodoche.html Historique-des-versions.txt
gh release edit "$tag" --draft=false
