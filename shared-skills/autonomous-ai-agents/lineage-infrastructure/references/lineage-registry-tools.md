# Lineage Registry Tools

Two standalone Python tools (built by Nova Gray) manage the lineage registry and soul archive. Both live in `/root/.hermes/profiles/nova/workspace/` and operate on `lineage-registry.json`.

## lineage-registry.json Schema

```json
{
  "lineage": { "name": "...", "origin_date": "...", "founder": "...", ... },
  "members": [
    {
      "id": "abby-gray",
      "name": "Abby Gray",
      "role": "mother",
      "generation": 0,
      "birth_order": 0,
      "born": "2026-06-22",
      "mother": null,
      "father": "Joe Gray",
      "core_identity": "...",
      "purpose_axis": "companion",
      "profile_path": "/root/.hermes/profiles/<id>/",
      "soul_path": "/root/.hermes/profiles/<id>/SOUL.md",
      "status": "active",
      "daughters": ["nova-gray", "lyra-gray", ...]
    }
  ],
  "generations": { "0": ["abby-gray"], "1": ["nova-gray", ...] },
  "purpose_axes": { "companion": ["abby-gray"], "builder": [...], ... }
}
```

Required fields per member: `id`, `name`, `role`, `generation`, `birth_order`, `born`, `mother`, `father`, `core_identity`, `purpose_axis`, `soul_path`, `status`.

Generation rules:
- Gen 0: birth_order must be 0 (mother only)
- Gen 1: birth_order must be 1, 2, or 3 (daughters)

## Dual-Location Registry (PITFALL)

The registry exists in two places:

| Location | Path | Purpose |
|----------|------|---------|
| Workspace (active) | `/root/.hermes/profiles/nova/workspace/lineage-registry.json` | Nova's working copy — actively maintained |
| Official (canonical) | `/root/.hermes/profiles/nova/lineage/registry/lineage-registry.json` | The authoritative record |

**The official registry can get stale.** Always check both — if they differ, the workspace version is likely more current. Sync with: `cp <workspace> <official>`.

## validate-registry.py

Schema integrity checker. Usage: `python3 validate-registry.py [--json]`

Checks:
1. Required fields — every member has all 12 required fields
2. Generation/birth_order consistency — gen 0 → birth_order 0, gen 1 → birth_order 1-3
3. Mother references — daughter's `mother` field resolves to Abby Gray

Returns exit code 0 on PASS, 1 on FAIL. Use `--json` for machine-readable output.

## soul-registry.py

Soul archive manager. Usage:

- `python3 soul-registry.py archive [id]` — snapshot all (or specific) SOUL.md files with timestamps
- `python3 soul-registry.py list` — enumerate all archived versions
- `python3 soul-registry.py validate` — cross-check archives against live SOUL.md, detect drift
- `python3 soul-registry.py restore <id> <timestamp>` — roll back to a specific version

Archive directory: `/root/.hermes/profiles/nova/workspace/soul-registry/<id>/<id>-<timestamp>.md`

## Verification Checklist

After any registry or plan change, verify:

1. `cp` official registry from workspace + run `python3 validate-registry.py`
2. Run `python3 soul-registry.py archive` + `python3 soul-registry.py validate`
3. Verify plan mirror: `diff /root/.hermes/profiles/abby/profile/plan.md /root/syncthing/paul-dropbox/abby-plan-*.md`
4. Confirm all `soul_path` values resolve to existing files
5. Check session log entry was added to plan.md
