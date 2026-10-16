# Repository layout and configuration filenames

BardBox instrument repositories use the RKC Monitor layout:

```text
hardware/
  ecad/                 # KiCad electronics, libraries and fabrication exports
  mcad/                 # mechanical/enclosure CAD and manufacturing exports
software/
  app/                  # server/application code, templates and static assets
  firmware/<project>/   # separate PlatformIO projects when more than one exists
scripts/
deploy/
docs/
data/                   # measurements; private runtime data stays ignored
```

A single firmware project may live directly in `software/firmware`, as in the
project template. Shared libraries may have a separate documented source location;
do not move them blindly and break consumers. Software-only tools and standards
repositories do not need artificial ECAD/MCAD folders. Existing legacy archives
retain their historical paths; active project entry points use this layout.

ECAD contains KiCad schematics, boards, libraries and revisioned fabrication
exports. MCAD contains enclosure/mechanical source and exports. Do not treat an
empty folder or README as proof that drawings exist or an assembly is validated.

## Firmware configuration

Use tracked `src/config.example.h` for safe placeholder configuration and ignored
`src/config.h` for the local deployment values. Configuration includes pins,
sampling choices and identity as well as credentials; `secrets.h` is therefore
not the preferred filename. Existing private `secrets.h` must be locally renamed,
not overwritten with example defaults. Keep both private names ignored during
migration. Never commit real credentials. Firmware version and hardware revision
remain independent; a header rename alone does not change deployed behavior.

## Migration checks

Update imports, relative data/config paths, scripts, service entry points, tests,
CI, documentation and ignores together. Compare firmware bytes across pure moves
and run path-sensitive tests/builds. Inventory untracked private config and runtime
data before deploying; repository moves must not overwrite or strand them. Prepare
service rollback to the old commit/entry point and verify real data roots after
migration. Source layout adoption does not itself authorize production migration.

The user is the sign-off owner for consequential merges. Branding and part-number
allocation remain with the user; a future initial-flashing app may assign instance
identifiers after that policy is defined. Do not allocate or rename deployed IDs
as part of repository reorganization.
