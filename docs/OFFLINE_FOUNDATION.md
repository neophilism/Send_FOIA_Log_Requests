# SFL-01 offline foundation

Runtime requires Python 3.11+ and the pinned setuptools 84.0.0 build backend. There are no third-party runtime dependencies. Install with `python -m pip install .`; run `foia-requests --help`, `foia-requests --config fixtures/offline-config.json draft`, `python scripts/check_foundation.py`, and `python scripts/validate_plan.py`. The product check rejects zero-test discovery. An editable install is also supported for development.

All command families except help are placeholders, not completed services. Dispatch always fails closed and no network credentials, messages, or fees are configured. The strict JSON config rejects unknown fields and transport enablement. The SQLite migration creates only schema version tracking; the durable request ledger is a later unit. No live operation is authorized by this code.

Existing GitHub Actions workflows validate policy and registry files, not the Python product suite. Run `python scripts/check_foundation.py` in an isolated Python environment until a product CI job is available. A passing policy workflow does not certify runtime behavior.

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
The plan validator passed. The pinned setuptools 84.0.0 isolated package build
was not exercised in this runtime (installed backend: 84.1.0); no exact-backend
reproducibility claim is made. Existing protected product CI workflow owner action
remains unresolved; no protected-path workaround was attempted.
