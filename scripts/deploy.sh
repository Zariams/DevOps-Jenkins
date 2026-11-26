#!/usr/bin/env bash
set -euo pipefail
# Виконується на VM4 під deploy; номер надає Jenkins.
build=${1:?build number required}
[[ "$build" =~ ^[0-9]+$ ]]
base=/opt/lifedays
release="$base/releases/$build"
previous=$(readlink "$base/current" || true)
mkdir -p "$release"
tar -xzf "$base/incoming/$build.tar.gz" -C "$release"
python3 -m venv "$release/.venv"
"$release/.venv/bin/pip" install -r "$release/requirements.txt"
ln -sfn "$release" "$base/current.next"
mv -Tf "$base/current.next" "$base/current"
if sudo -n /usr/bin/systemctl restart lifedays.service && curl -fsS --retry 5 --retry-connrefused --retry-delay 1 http://127.0.0.1/health; then
    rm -f "$base/incoming/$build.tar.gz"
else
    if [[ -n "$previous" ]]; then
        ln -sfn "$previous" "$base/current.next"
        mv -Tf "$base/current.next" "$base/current"
        sudo -n /usr/bin/systemctl restart lifedays.service
    else
        rm -f "$base/current"
    fi
    exit 1
fi
