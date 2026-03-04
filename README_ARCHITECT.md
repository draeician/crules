### ## The Swarm Architect: Meta-Management Protocol

The **Swarm Architect** is the specialized operational mode for the `crules` repository itself. While standard Swarm modes (Manager, Coder) are designed to build *applications*, the Architect is designed to build *the system that builds applications*.

---

### ### 🎯 When to Use the Architect

You should engage the Swarm Architect when you are working **inside** the `crules` source repository to:

* **Modify Personas:** Updating the core logic in `MANAGER.md`, `CODER.md`, or `AUDITOR.md`.
* **Evolve Workflows:** Adding new project templates or logic to `GIT_POLICY.md`.
* **Expand the CLI:** Adding new flags (like `--sync` or `--bootstrap`) to the `crules` Python package.
* **Debug the Swarm:** Troubleshooting why a project isn't syncing or why the AI is ignoring a specific rule.

---

### ### 🛠️ How to Use the Architect

The Architect is triggered by the `.cursorrules` file in the `crules` root. It expects a specific "Dogfooding" workflow to ensure changes are safely deployed across your system.

#### **1. Brainstorming Mode**

When you have a new idea for the Swarm, ask the Architect to "Brainstorm."

* **Example:** *"Architect, brainstorm a way to add an 'Audit' step that runs before every commit."*
* **Action:** It will analyze the impact on `file_ops.py` and the `default_cursorrules` without writing code yet.

#### **2. Construction Mode**

When you are ready to implement, the Architect manages the file synchronization.

* **Example:** *"Implement the Audit logic we discussed."*
* **Action:** It will update the source templates in `src/crules/rules/workflows/` and ensures they are mirrored in the local `.crules/modes/` for testing.

#### **3. The Trinity Update (Post-Change)**

Because `crules` is a global tool, a code change doesn't take effect until you "re-home" it. The Architect will remind you to run:

1. **`pipx install . --force`**: Updates the global binary.
2. **`crules --setup --force`**: Updates your `~/.config/crules` templates.
3. **`crules -S`**: Updates the current project's local rules.

---

### ### 🚀 Core Use Cases

| Use Case | Architect Action | Benefit |
| --- | --- | --- |
| **Adding a New Mode** | Updates `file_ops.py` and creates a new `.md` template. | Ensures `crules -b` includes the new mode in all future projects. |
| **Updating Shortcuts** | Modifies `src/crules/rules/default_cursorrules`. | Globally updates the "Shortcuts" (like `next` or `commit`) for all projects. |
| **Fixing Version Drift** | Enforces the "Monotonic Principle" across TOML and Code. | Prevents `pipx` and the CLI from reporting different versions. |
| **Environment Safety** | Blocks `--break-system-packages` logic. | Protects your Linux Mint OS from accidental corruption by the AI. |

---

### ### 🛡️ Safety & Integrity Rules

The Architect operates under a strict "Safety-First" policy tailored for Linux Mint:

* **No Sledgehammers:** It will never use `pip` to install packages system-wide.
* **Triangulated Truth:** It never trusts a single version number; it checks the TOML, the Code, and the Git Tags.
* **Validation First:** It will attempt to execute `python3 -m crules --version` before finalizing any commit to ensure the "Brain" and the "Metadata" match.

