# Session Close Documentation Standard

When Joe closes a session, the Daily Handover must include:

1. **Summary** — What was accomplished in one paragraph
2. **Deliverables** — Every file produced with full absolute paths and version numbers
3. **Pipeline artifacts** — All intermediate files (validator reports, critic reports, batch outputs)
4. **Process improvements** — What changed in skills/specs/playbooks during the session (kaizen)
5. **Files modified** — Any existing documents that were updated
6. **Timeline** — Phase-by-phase with iteration counts and results
7. **Lessons learned** — What worked, what broke, what to change next time
8. **Next for Joe** — What Joe needs to review, decisions pending

Every file reference must use the full absolute path:
```
/root/.hermes/docs/Paul/workspace/trigger-card-design/card-design/iter-3/assembled.md
```

Not short names or relative paths. This ensures cross-session discoverability
even when context is compressed.
