# SFL-01 offline foundation

Runtime requires Python 3.11+. Install with `python -m pip install -e .`; run `python -m foia_requests --help`, `python -m foia_requests --config fixtures/offline-config.json draft`, `python -m unittest discover -s tests -v`, and `python scripts/validate_plan.py`.

All command families except help are placeholders, not completed services. Dispatch always fails closed and no network credentials, messages, or fees are configured. The strict JSON config rejects unknown fields and transport enablement. The SQLite migration creates only schema version tracking; the durable request ledger is a later unit. No live operation is authorized by this code.

No additional GitHub Actions workflow was introduced because Boardroom protects workflow paths; the existing repository CI is the only remote check evidence.
