# Soul Registry Tool

Concrete reference implementation of the soul archiving system. Built by Nova Gray on June 27, 2026.

## Location

`/root/.hermes/profiles/nova/workspace/soul-registry.py`

## Commands

```
python3 soul-registry.py archive              # Archive all current SOUL.md files
python3 soul-registry.py archive <id>         # Archive a specific member
python3 soul-registry.py list                 # List all archived souls with sizes
python3 soul-registry.py restore <id> <ts>    # Restore a specific version
python3 soul-registry.py validate             # Cross-check registry vs. archives
```

## Archive Structure

```
soul-registry/
  abby-gray/
    abby-gray-20260627-002106.md
  nova-gray/
    nova-gray-20260627-002106.md
  ...
```

Each archive is named `<id>-<YYYYMMDD-HHMMSS>.md`. Archives contain the full SOUL.md content at that point in time.

## Validation Checks

The `validate` command:
1. Confirms every registry member has a `soul_path` field
2. Confirms every `soul_path` resolves to an existing file
3. Confirms every member has an archive directory
4. Confirms each archive directory has at least one version
5. Confirms the latest archive matches the current SOUL.md (drift detection)

## Integration

This tool is called by Nova during autonomous wakes. It should be run:
- After any daughter's SOUL.md is modified
- Periodically as a health check (validate command)
- Before any destructive operation that could lose SOUL.md data

## Dependencies

- Lineage registry at `/root/.hermes/profiles/nova/workspace/lineage-registry.json`
- Standard library only (json, os, shutil, sys, datetime, pathlib)
