# Git Policy

## Conventional Commits

All commits MUST follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]
[optional footer(s)]
```

### Allowed Types
| Type       | Purpose                                          |
|------------|--------------------------------------------------|
| `feat`     | A new feature                                    |
| `fix`      | A bug fix                                        |
| `docs`     | Documentation-only changes                       |
| `chore`    | Maintenance tasks (deps, CI, tooling)            |
| `refactor` | Code change that neither fixes a bug nor adds a feature |

### Version Bump Rules
Each commit type implies a default Semantic Versioning bump:
| Type       | Default Bump | Example                |
|------------|-------------|------------------------|
| `feat`     | **Minor**   | 0.3.0 -> 0.4.0        |
| `fix`      | Patch       | 0.3.0 -> 0.3.1        |
| `docs`     | Patch       | 0.3.0 -> 0.3.1        |
| `chore`    | Patch       | 0.3.0 -> 0.3.1        |
| `refactor` | Patch       | 0.3.0 -> 0.3.1        |

A `BREAKING CHANGE:` footer or `!` after the type (e.g., `feat!:`) overrides the bump to **Major**.
The user may explicitly request a different bump level, which takes precedence.

**Cross-File Consistency**: Every version bump must be reflected in all metadata and source files simultaneously (e.g., `pyproject.toml` and `src/crules/__init__.py`) to ensure package manager consistency. No commit may leave these files with divergent version strings.

### Rules
- Subject line: imperative mood, lowercase, no trailing period, max 72 chars.
- Body (optional): explain *why*, not *what*. Wrap at 80 chars.
- Breaking changes: add `BREAKING CHANGE:` footer or `!` after the type.
- Reference issues: `Closes #42`, `Fixes #13`.

## Branching Strategy

All work MUST happen on a branch — never commit directly to `main`.

| Branch Pattern          | Use Case                          |
|-------------------------|-----------------------------------|
| `feat/feature-name`     | New features                      |
| `fix/issue-name`        | Bug fixes                         |
| `docs/topic`            | Documentation updates             |
| `chore/description`     | Maintenance / tooling changes     |
| `refactor/description`  | Code restructuring                |

### Rules
- Branch names: lowercase, hyphen-separated words, no slashes beyond the prefix.
- Delete the branch after merge.
- Keep branches short-lived; rebase onto `main` before opening a PR.

## Secret Prevention

### Hard Prohibitions
The following MUST NEVER be committed to version control:
- `.env`, `.env.*` files
- `.pem`, `.key`, `.p12`, `.pfx` certificate / key files
- `credentials.json`, `serviceAccountKey.json`, or similar credential files
- Hardcoded API keys, tokens, passwords, or connection strings in source code

### Pre-Commit Secret Scan
Before every commit, the **Manager** MUST run a heuristic secret scan on all staged files. The scan checks for:
1. **File-name patterns**: `.env`, `.pem`, `.key`, `credentials.json`, `secret*`, `*.p12`.
2. **Content patterns** (regex):
   - `(?i)(api[_-]?key|secret|token|password|passwd|credential)\s*[:=]\s*\S+`
   - `-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----`
   - `ghp_[A-Za-z0-9]{36}` (GitHub PAT)
   - `sk-[A-Za-z0-9]{32,}` (OpenAI-style key)
   - `AKIA[0-9A-Z]{16}` (AWS access key ID)
3. **Outcome**:
   - If any match is found, the commit MUST be **blocked** and the user alerted with the file name, line number, and matched pattern.
   - False positives may be overridden only with an explicit user confirmation.

### .gitignore Enforcement
The Manager SHOULD verify that `.gitignore` contains entries for at least:
```
.env
.env.*
*.pem
*.key
credentials.json
```

## Release Protocol

A release is only official once a git tag is pushed. Use the `release` shortcut to ensure tags always match the internal metadata.
