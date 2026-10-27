# Disposable eval vault

From this skill root, run `python3 evals/init_vault.py --destination /tmp/ace-eval-vault` with a new destination for each run. The script copies only bundled fixtures and refuses an existing destination. No personal vault is needed.

Open that directory as a vault in Obsidian Desktop, enable the CLI, and confirm `obsidian vault info=path` points to this disposable directory. Register/open it before any CLI evaluation, and supply its actual `vault=<name>` before every command when another vault is open. Do not execute evaluation writes against a personal vault. The CLI/app is required for live vault questions and property mutations; structure linting runs offline.

The eval `files` entries are skill-relative source fixtures; initialization preserves their vault-relative paths. Reset by choosing a fresh destination and rerunning initialization. Read-only ACE evals may leave the generated core folders empty; optional subfolder/config findings are expected. Full model-driven output evaluation is separate from fixture validation.
