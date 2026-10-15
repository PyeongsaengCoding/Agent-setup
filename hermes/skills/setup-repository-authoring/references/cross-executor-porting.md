# Porting setup features across agent executors

## Consolidation order

1. Locate every source (a setup repo may live outside the expected folder; search by name across Downloads/Documents). Record HEAD, dirty status and per-file SHA256 before copying.
2. Copy only tracked files of each source into `<repo>/<executor>/` with a script that refuses symlinks, runtime/credential files and changed-during-copy sources. Exclude historical reports/records and per-repo CI; fix any doc that linked to them so the executor's own link checker still passes.
3. Add a root `scripts/check.py --executor {all,codex,claude,hermes}` that only invokes each executor's existing checks with the executor folder as cwd, plus a regression test that one selection does not run the others and that a failing native check is not reported as PASS.
4. Re-diff the live source against the copy before finishing; another session may have edited the source meanwhile. Reapply changed files and re-run checks.
5. Run everything with the project-required Python (tomllib needs >=3.11); the macOS system python3 can be older.

## Portability table (typical)

| Hermes feature | Codex | Claude Code |
|---|---|---|
| Aside `repl` browser rule | rule section in managed `~/.codex/AGENTS.md` source | managed block in `~/.claude/CLAUDE.md` |
| Custom SKILL.md skills | copy into `codex/skills/` (+ allowlist `.gitignore`, skill counts in docs) | copy into `.claude/skills/` |
| GPT+Claude mixed routing presets | Codex stays GPT-only | port both presets (below) |
| Desktop UI sizing, usage plugin, document folder cards, Hermes source fallback patches | Hermes-only | Hermes-only |

When a codex allowlist `.gitignore` exists, every new file must be added to it; verify with `git check-ignore -v`.

## Claude Code routing with GPT models

Claude Code can run GPT models through OpenAI's official plugin (`claude plugin marketplace add openai/codex-plugin-cc`, `claude plugin install codex@openai-codex`, then `/codex:setup`). Its `codex:codex-rescue` subagent forwards to the local Codex CLI and accepts `--model` and `--effort`; it uses the machine's Codex login and limits.

- Keep one routing JSON with `descriptions` and `presets` copied verbatim (model + effort per chain entry) from the Hermes presets; add a test that compares them to the Hermes preset files.
- Generate one agent per (category, Claude family): `route-<category>-<family>.md` with `model:` and `effort:` frontmatter. Fail generation if two presets disagree on the same agent's model/effort.
- Map `gpt-*` entries to executor `codex:codex-rescue` with `--model/--effort`.
- Claude Code has no per-subagent automatic model fallback (`--fallback-model` is session-level). Put the fallback procedure in the global CLAUDE.md block: on model-unavailable, limit, auth error or empty Codex result, hand the same task to the next chain entry; report category, requested model and the entry that actually ran.
- Installer (`scripts/install.py --home ~/.claude --preset ... [--apply]`): default preview; record hashes of files it wrote; update only unchanged managed files; stop with no writes on user-edited or foreign files, edited managed block, or symlinks; append the CLAUDE.md block after existing text; back up before overwrite; report whether the Codex plugin and `aside` CLI are present. Test preview, first install, repeat-unchanged, preset switch, conflict, and symlink refusal in a temp home.
