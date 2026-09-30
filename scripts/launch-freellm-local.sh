#!/usr/bin/env bash
set -euo pipefail

# A separate profile lets FreeLLM and Pro run from the same tested app payload.
state_dir="${CODEX_FREELLM_STATE_DIR:-$HOME/.local/state/codex-freellm-desktop}"
app_dir="${CODEX_FREELLM_APP_DIR:-$HOME/.local/opt/codex-desktop-linux/codex-app-official-linux-26.928.21956-pro-candidate-v3}"
secret_dir="${CODEX_FREELLM_SECRET_DIR:-$HOME/.config/codex-freellm}"

for required in \
    "$app_dir/start.sh" \
    "$HOME/.local/bin/codex-freellm-cli-isolated" \
    "$secret_dir/cloudflare-access.env" \
    "$secret_dir/freellm.env"; do
    if [ ! -f "$required" ]; then
        printf 'FreeLLM prerequisite missing: %s\n' "$required" >&2
        exit 1
    fi
done

export CODEX_HOME="${CODEX_FREELLM_CODEX_HOME:-$HOME/.codex-freellm}"
export XDG_CONFIG_HOME="$state_dir/official-xdg-config"
export XDG_STATE_HOME="$state_dir/xdg-state"
export XDG_CACHE_HOME="$state_dir/xdg-cache"
export CODEX_LINUX_APP_ID=codex-freellm
export CODEX_LINUX_APP_DISPLAY_NAME='Codex FreeLLM'
export CODEX_CLI_PATH="$HOME/.local/bin/codex-freellm-cli-isolated"
export PATH="$HOME/.local/opt/codex-desktop-linux/x11-tools/bin:$PATH"

mkdir -p "$XDG_CONFIG_HOME" "$XDG_STATE_HOME" "$XDG_CACHE_HOME"
set -a
# These private files contain credentials; never commit or print their values.
. "$secret_dir/cloudflare-access.env"
. "$secret_dir/freellm.env"
set +a

exec "$app_dir/start.sh" --no-sandbox \
    --user-data-dir="$XDG_CONFIG_HOME/Codex" "$@"
