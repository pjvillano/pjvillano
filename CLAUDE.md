# CLAUDE.md

## Repository Overview

This is **pjvillano/pjvillano**, a GitHub special profile repository. GitHub automatically renders the `README.md` in this repository as the public profile page for the account `pjvillano`. There is no application code, build system, or test suite — the entire project is a single Markdown file.

## Repository Structure

```
pjvillano/
└── README.md   # GitHub profile page content (the sole file)
```

## Purpose

The `README.md` serves as a professional bio and contact card displayed at the top of https://github.com/pjvillano. It introduces Pete Villano — his professional focus, current employer, consulting firms, and contact details.

### Current content summary (as of last update)

- **Name:** Pete Villano
- **Focus areas:** Quantum computing & networking, applied AI, next-generation cybersecurity
- **Employer:** IonQ Quantum (aligning applied projects with U.S. government agencies)
- **Consulting firms:** New Harbor Collective, Villano Ventures (emerging tech and space)
- **Contact:** pjvillano+github@gmail.com / villano@ionq.co
- **Website:** https://pjvillano.com/

## Development Workflow

### Making changes

There is only one file to edit: `README.md`. No build step, linter, or test runner is required.

```bash
# Edit the profile
$EDITOR README.md

# Stage and commit
git add README.md
git commit -m "Update README.md"

# Push to master (the branch GitHub uses for profile rendering)
git push origin master
```

### Branch strategy

| Branch | Purpose |
|--------|---------|
| `master` | Production — rendered live on GitHub profile |
| `claude/*` | AI-assistant working branches; open a PR to merge into `master` |

Always develop on a `claude/` branch and open a pull request targeting `master`. Never force-push to `master`.

### Commit conventions

All historical commits use the message `"Update README.md"`. Follow this convention unless a more descriptive message is clearly appropriate (e.g., `"Add quantum networking section"`).

## Editing Guidelines for AI Assistants

1. **Preserve voice and tone.** The bio is written in first person, present tense, with a professional but approachable tone. Match that style in any additions or edits.
2. **Keep it concise.** GitHub profiles render in a narrow column. Avoid long paragraphs; use short sentences and, where helpful, bullet points.
3. **Do not add code blocks, badges, or images** unless explicitly requested — the current style is plain prose.
4. **Do not restructure** the existing sections without instruction; only add or update specific requested content.
5. **Maintain the HTML comment block** at the bottom of the file (the `<!--- ... --->` note about this being a special repo); it is informational and harmless.
6. **Do not create additional files** (configuration, scripts, etc.) unless explicitly asked. This repo intentionally contains only `README.md`.

## Key Facts

- **Default branch rendered by GitHub:** `master`
- **No CI/CD, no tests, no linter**
- **No dependencies or package managers**
- **Single contributor:** Peter Villano (pjvillano@gmail.com)
- **Git history:** ~16 commits, all `README.md` updates since initial creation
