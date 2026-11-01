# SFL-01 offline foundation

Runtime requires Python 3.11+ and the pinned setuptools 84.0.0 build backend. There are no third-party runtime dependencies. Install with `python -m pip install .`; run `foia-requests --help`, `foia-requests --config fixtures/offline-config.json draft`, `python scripts/check_foundation.py`, and `python scripts/validate_plan.py`. The product check rejects zero-test discovery. An editable install is also supported for development.

All command families except help are placeholders, not completed services. Dispatch always fails closed and no network credentials, messages, or fees are configured. The strict JSON config rejects unknown fields and transport enablement. The SQLite migration creates only schema version tracking; the durable request ledger is a later unit. No live operation is authorized by this code.

The `offline-foundation` GitHub Actions job now runs the 20 offline Python product tests, validates the plan, builds a wheel with pinned setuptools 84.0.0, installs it into a fresh virtual environment and verifies normal CLI startup and fail-closed dispatch. See `.github/workflows/offline-foundation.yml`. Product acceptance requires this job **and** repository source/registry checks to pass on the exact PR head. This is not a live campaign or dispatch certification.

## Private local files

Configuration must be a regular file; symlinks, FIFOs/devices, oversized files,
non-finite numbers, duplicate keys and deeply nested invalid JSON fail before a
command runs. Configuration reads are bounded and do not wait on FIFO writers.

Persistent migration databases must be regular owned 0600 files in owned 0700
directories. Newly created nested directories use 0700 individually. Linked or
permissively accessible existing files/directories are rejected without changing
their permissions or contents. Directory symlinks are rejected before creating
children. Choose a private location explicitly; migration never silently opens
an existing shared ledger. The in-memory database path remains supported.
These filesystem controls were exercised on the POSIX test runtime.

Migration startup serializes the schema check and initialization. It validates
the tracking table shape and event history instead of trusting user_version
alone. Future/inconsistent schemas are rejected without being rewritten.

Validation for this change: 20 product tests passed on Python 3.12.14, including
four independent initializer processes, FIFO rejection with a process deadline,
symlink/hard-link safety, private modes and rollback on incompatible schema.
The plan validator passed. The pinned setuptools 84.0.0 package build and fresh-env install are now exercised by the `offline-foundation` CI job. This is limited to the exact runtime, environment and head reported by GitHub Actions; a local development test alone is not a release gate.
