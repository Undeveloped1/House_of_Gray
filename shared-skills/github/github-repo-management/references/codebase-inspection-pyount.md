# Codebase Inspection with pygount

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

## Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## Basic Summary

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

Always exclude dependency/build directories — without `--folders-to-skip`, pygount will crawl them and may hang.

## Common Folder Exclusions

| Project Type | Exclusions |
|---|---|
| Python | `.git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache` |
| JavaScript/TypeScript | `.git,node_modules,dist,build,.next,.cache,.turbo,coverage` |
| General catch-all | `.git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party` |

## Output Formats

```bash
# Summary table (default)
pygount --format=summary .

# JSON for programmatic use
pygount --format=json .

# Per-file breakdown, sorted by code lines
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## Filtering

```bash
# Only Python files
pygount --suffix=py --format=summary .

# Only Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## Interpreting Results

Summary table columns: **Language**, **Files**, **Code** (executable/declarative lines), **Comment** (comment/doc lines), **%** (percentage of total).

Special pseudo-languages: `__empty__` (empty files), `__binary__` (binary files), `__generated__` (auto-generated), `__duplicate__` (identical content), `__unknown__` (unrecognized types).

## Pitfalls

- Markdown shows 0 code lines — pygount classifies all Markdown as comments
- JSON files show low counts — use `wc -l` for accurate JSON line counts
- Large monorepos — use `--suffix` to target specific languages
