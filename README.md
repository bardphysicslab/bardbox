# BardBox

BardBox is Bard College Physics' shared monitoring-platform repository. It defines common protocols, driver expectations, recovery behavior, and project conventions used by BardBox deployments.

## Project workflow

BardBox project repositories should be created from or kept aligned with `bardbox-project-template` for shared infrastructure and conventions.

For configuration-schema changes and deployment diagnostics, follow [`docs/config-report-workflow.md`](docs/config-report-workflow.md). Every BardBox project should include the standard `scripts/sync_app_config.py` and `scripts/generate_reports.py` tooling; if a project is missing that workflow, add or sync it from `bardbox-project-template` before substantive configuration or deployment work continues.

See the documents under `docs/` for protocol, driver, transport-recovery, and deployment guidance.
