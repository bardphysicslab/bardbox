# BardBox Config and Report Workflow

Every BardBox project repository must include the standard configuration synchronization and diagnostic reporting workflow. If a repository does not yet contain this infrastructure, add or sync it from `bardbox-project-template` before substantive configuration or deployment work continues.

## Required project tooling

Each BardBox project should provide:

- `scripts/sync_app_config.py`
- `scripts/generate_reports.py`
- a repository-owned example/default config such as `software/app/config/app_config.example.json` (older projects: `raspi/config/`)
- an ignored live config such as `software/app/config/app_config.json`
- a disposable `reports/` directory for generated diagnostic text files

When this tooling is absent or outdated, treat synchronizing it from `bardbox-project-template` as an early repository setup task.

## Module-owned configuration (accepted direction)

Folder locations for each module's configuration, and how tracked non-secret
settings are kept apart from private overrides, are in the
[repository layout](repository-layout.md#configuration-files)
([BB-004](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6271296848)).

October 19, 2026 ([BB-003](https://github.com/bardphysicslab/bardbox/issues/31#issuecomment-6269561991) item 5): each owning module validates, persists and
applies its own settings, and new reference configuration physically lives in
the owning module's subtree (for example alarm settings under the Alarm module).
This refines the earlier single-file allowance for new reference structures.
Existing pilot configuration is not moved by this decision. Before any layout
change, the synchronizer and reports must handle per-module files while still
preserving deployment values, local-only fields and protected secrets. Each
setting declares who may edit it and when a change takes effect; authorized web
edits save through the owner and then re-read the saved value
([configuration ownership](architecture-map.md#configuration-ownership)).

## Standard report command

The normal project diagnostic workflow is:

```bash
export BARDBOX_REPORTS_RCLONE_TARGET='<rclone-remote>:<project>/reports'
python3 scripts/generate_reports.py
```

Projects may equivalently pass the destination directly:

```bash
python3 scripts/generate_reports.py \
  --rclone-target '<rclone-remote>:<project>/reports'
```

The report generator should:

1. Run `scripts/sync_app_config.py --dry-run` to produce `reports/config_sync_report.txt`.
2. Produce `reports/active_config_report.txt`, a readable snapshot of the current ignored live config with credentials and other sensitive values redacted. This report exists so maintainers and authorized remote tools can review the actual preserved deployment values rather than only the structural comparison result.
3. Produce `reports/git_diff.txt` containing the current branch, HEAD, short status, unstaged diff, and staged diff.
4. When an rclone target is configured, upload the generated `.txt` reports from `reports/` to the project report destination.

The live config itself must remain ignored and must not be uploaded verbatim merely for diagnostics. Report generation must redact values whose keys identify credentials or secrets, including tokens, passwords, API keys, access/refresh tokens, and client secrets. Projects may extend the redaction set when they contain additional sensitive config fields.

The project-specific rclone path must not be hard-coded into the shared BardBox standard. Configure it per deployment through `BARDBOX_REPORTS_RCLONE_TARGET` or `--rclone-target`.

## Config synchronization

Use a dry run before changing the live config:

```bash
python3 scripts/sync_app_config.py --dry-run
```

A dry run compares the repository-owned example config with the ignored live config, writes `reports/config_sync_report.txt`, and must not modify the live config.

To apply structural additions:

```bash
python3 scripts/sync_app_config.py --write
```

The synchronization implementation must preserve deployment-specific local values, add newly required fields from the example config, preserve local-only fields, match `nodes` and `drivers` by UID, and avoid silently inserting example-only nodes or drivers into an existing deployment. Before replacing an existing live config, it must create a timestamped backup and write the replacement atomically.

For automated checks or deployment gates:

```bash
python3 scripts/sync_app_config.py --check
```

`--check` should return a non-zero exit status when structural migration is required.

## Interpretation and safety

A clean config-sync report means the live config is structurally aligned with the repository-owned example. It does **not** prove that preserved local values are semantically correct, scientifically valid, or safe for the attached hardware. Hardware limits, calibration values, network settings, credentials, UIDs, and other deployment-specific settings must still be reviewed on their own merits before deployment.

Use `active_config_report.txt` when the actual deployment values need review without exposing secrets. The redacted snapshot is diagnostic material, not a deployable config file and must not be copied back over the live config.

Never replace an ignored live config wholesale with the example config merely to make a report clean.

## Agent and maintainer checklist

At the beginning of work in a BardBox project repository:

1. Verify that the standard config/report tooling exists.
2. If it is missing or stale, sync it from `bardbox-project-template` before continuing config/deployment work.
3. After config-schema changes, run the standard report workflow.
4. Review `config_sync_report.txt` and `active_config_report.txt` before editing or deploying the active config.
5. Apply needed structural migrations deliberately with `sync_app_config.py --write`, then review the resulting live config.
6. Run the report workflow again after migration.
7. Upload reports to the project's configured BardBox report destination when available.

A future convenience wrapper such as `./scripts/report` may be provided by the project template, but the canonical underlying commands above remain the source of truth.
