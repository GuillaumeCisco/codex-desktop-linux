# Local FreeLLM rollout on Sugar, Kiwi, and Lemon

The FreeLLM desktop uses the same tested 26.928.21956 application payload as
Pro, but a separate `CODEX_HOME`, XDG profile, CLI wrapper, and private provider
environment. Start it with [`scripts/launch-freellm-local.sh`](../scripts/launch-freellm-local.sh).
The launcher expects the existing private files in `~/.config/codex-freellm/`
and the existing `~/.local/bin/codex-freellm-cli-isolated`; neither belongs in
the repository. Set `CODEX_FREELLM_APP_DIR` when testing a newer payload.

Before replacing an installation, back up its old runtime, `~/.codex-freellm`,
`~/.config/codex-freellm`, XDG state, CLI wrapper, and launchers. Keep Pro and
FreeLLM profiles distinct. The old FreeLLM launcher used a per-instance XDG
configuration under
`~/.local/state/codex-freellm-desktop/xdg-state/codex-freellm/instances/port-5180/xdg-config/`.
To keep existing Remote client authorization, copy its
`codex-desktop/remote-control-device-keys/remote-control-device-keys-v1.json`
into `~/.local/state/codex-freellm-desktop/official-xdg-config/codex-desktop/remote-control-device-keys/`
before first launch. The matching enrollment metadata remains in
`~/.codex-freellm/.codex-global-state.json`. Keep both files private and do
not create a new client enrollment accidentally.

Use a fresh `official-xdg-config` directory for the new Electron profile;
the old renderer profile can retain stale Remote connection discovery state.
Preserve the FreeLLM history by continuing to use the real
`~/.codex-freellm` as `CODEX_HOME`. Sugar's first isolated test used a new
device key and found no Remote hosts; restoring the existing key and using a
fresh Electron profile made the Lemon connection reach `connected`.

The 2026-09-30 deployment order was Sugar FreeLLM, Kiwi FreeLLM, Lemon
FreeLLM. Lemon Pro was left running on its previous version pending separate
approval. Kiwi Pro was upgraded only after its own runtime and profile backup.
The Kiwi X11 Computer Use doctor needs `xdotool`, `wmctrl`, and `xprop` on the
launcher's `PATH`; its ready result had no blockers and selected `xdotool`
input, X11 screenshots, and X11 window control.
