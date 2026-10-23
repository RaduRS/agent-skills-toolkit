# Agent Skills Toolkit

Six selected engineering skills from [Addy Osmani's Agent Skills](https://github.com/addyosmani/agent-skills), pinned to **aeac41d4d005999432bb7312f7ff06383a91d59d** (upstream 0.6.13). Bundle version 1.0.0. MIT; copyright (c) 2025 Addy Osmani.

| Skill | Use |
|---|---|
| `spec-driven-development` | Clarify significant work and agree measurable requirements before coding |
| `planning-and-task-breakdown` | Order dependencies and split work into verifiable slices |
| `api-and-interface-design` | Define contracts, validation, errors and safe retry behavior |
| `test-driven-development` | Prove behavior with focused tests and red/green/refactor |
| `debugging-and-error-recovery` | Reproduce and diagnose root causes before fixing |
| `security-and-hardening` | Review trust boundaries, authorization, dependencies and data handling |

This is a reviewed, instruction-only subset, not the full upstream plugin. No hooks, auto-updater, proxy, telemetry, MCP server, runtime package installation or credentials. The installer is local Python standard library code with no network calls. Existing Frontend Design and system Review Agent remain separate; this bundle does not copy or replace them. Examples inside Markdown are not executed during installation.

## Install on Windows

Requires GitHub access to this private repository, Git (or GitHub CLI) and Python 3.9+. Python is already available on the Windows machine used to prepare this bundle.

```powershell
gh repo clone RaduRS/agent-skills-toolkit
Set-Location agent-skills-toolkit
# Read install.py, manifest.json and the skill files before running.
python .\install.py install
python .\install.py verify
```

## Install on macOS

Requires GitHub access, Git (or GitHub CLI) and an existing Python 3.9+ installation. This bundle does not install Python or any packages. If `python3` is missing, install Python through your normal trusted developer setup first.

```sh
git clone https://github.com/RaduRS/agent-skills-toolkit.git
cd agent-skills-toolkit
# Read install.py, manifest.json and the skill files before running.
python3 install.py install
python3 install.py verify
```

On both systems the destination is **`~/.agents/skills/<skill-name>/`**, the [Codex user-level skill location](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). Every skill has its own license and supporting documents, so it is independent of this checkout. No sudo/admin privileges are needed. Existing skill directories cause an all-six preflight refusal; there is no overwrite flag. Unrelated skills such as `unity-cli` are untouched.

The skills should be available on the next Codex turn; restart Codex if discovery has not refreshed. Try `$planning-and-task-breakdown` with a clear engineering requirement. Planning/spec skills include human review gates; your direct instructions and the host's rules take precedence. Skills are guidance, not a correctness or security guarantee.

## Update, uninstall and restore

There is no automatic upstream update. Updating this toolkit requires reviewing and pinning a new upstream revision, reviewing all changed skill/reference files and adaptations, regenerating the manifest and testing before committing. A Git pull alone never updates installed skills.

To update an installed copy, **before pulling**, run the old checkout's installer with `verify`, then explicitly run `backup`. This moves only these six unchanged skill folders to a timestamped sibling `~/.agents/skill-backups/agent-skills-toolkit-<timestamp>/`; it deletes nothing. It refuses modified or incomplete installations. Keep the old checkout/revision available for rollback.

```sh
# On Windows use python instead of python3.
python3 install.py verify
python3 install.py backup
git pull --ff-only
# Review the new diff, install.py, manifest and skills before continuing.
python3 install.py install
python3 install.py verify
```

To uninstall, run `python3 install.py backup` (Windows: `python .\install.py backup`) from the matching installed bundle revision. For locally edited skills, back up/reconcile your edits manually first; the script will not move them. To restore, move each of the six named folders from the reported backup into `~/.agents/skills/` only after checking that the destination does not exist. Restart Codex if necessary. Do not move or delete the entire skills root.

## Provenance and adaptations

`manifest.json` records the upstream SHA, original file hashes, installed file hashes and review scope. Copied root references (`definition-of-done.md`, `testing-patterns.md`, `security-checklist.md`) are retained unchanged under the consuming skill's `references/upstream/`. Relative links in the skill and hardening patterns are rewritten to those local copies; no references are placed beside unrelated user configuration. The security skill's own `references/hardening-patterns.md` is included.

Each SKILL.md adds a small host-compatibility note: respect host/user rules, treat examples as illustrative and do not auto-install optional tools or unselected skills. The spec skill's two unselected file references link to the pinned upstream revision; its selected TDD reference links to the sibling installed skill. Other mentioned skill names are optional context, not included workflows. Core upstream engineering instructions and review gates are retained.

`install.py` validates exact inventories/checksums, rejects symlink/junction destinations, refuses existing skill destinations, copies only the six allowlisted directories, and supports a reversible explicit backup. SHA-256 detects accidental changes relative to the manifest; it is not a signature or proof that a compromised repository is trustworthy. An interrupted operation preserves partial files for inspection rather than deleting anything automatically.

Run installer checks with `python -m unittest discover -s tests -v` (macOS: `python3`). Windows installation and behavior checks were tested. The installed Codex loader reported all six skills enabled at user scope with no skill-loading errors. Python syntax is cross-platform, but this version has **not been executed on a Mac**. No private project files or machine configuration are included.
