# SFL-01 offline foundation

Runtime requires Python 3.11+ and the pinned setuptools 84.0.0 build backend. There are no third-party runtime dependencies. Install with `python -m pip install .`; run `foia-requests --help`, `foia-requests --config fixtures/offline-config.json draft`, `python scripts/check_foundation.py`, and `python scripts/validate_plan.py`. The product check rejects zero-test discovery. An editable install is also supported for development.

All command families except help are placeholders, not completed services. Dispatch always fails closed and no network credentials, messages, or fees are configured. The strict JSON config rejects unknown fields and transport enablement. The SQLite migration creates only schema version tracking; the durable request ledger is a later unit. No live operation is authorized by this code.

Existing GitHub Actions workflows validate policy and registry files, not the Python product suite. Run `python scripts/check_foundation.py` in an isolated Python environment until a product CI job is available. A passing policy workflow does not certify runtime behavior.
