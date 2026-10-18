# Send FOIA Log Requests

Start with the [comprehensive development plan](docs/DEVELOPMENT_PLAN.md), then [handoff status](docs/HANDOFF_STATUS.md) and the [canonical structured PR registry](registry/prs.json).

The scope is official agency/component discovery, annual FOIA log request generation, a bounded dry run, controlled dispatch, deduplication, submission/fulfillment tracking and yearly continuation.

The specification is complete as a current engineering reconstruction. Original detailed campaign settings were not recovered. SFL-01 provides an offline Python CLI and strict configuration scaffold; operational commands are placeholders and live dispatch is disabled. The documentation and code do not authorize messages, fees or a future schedule. Large campaigns depend on the FOIA Aggregator corpus review and exact dispatch authorization described in the plan.

Validate the plan/registry and offline product suite using Python 3.11+ from this directory:

```bash
python scripts/validate_plan.py
python scripts/check_foundation.py
```

The installed CLI is `foia-requests`. It exposes the planned command families but reports them as not implemented; `dispatch` fails closed. `registry/roadmap.json` redirects to `registry/prs.json`; maintain work IDs, dependencies and real PR mappings there rather than inventing totals from observed PR numbers.
