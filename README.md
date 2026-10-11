# Send FOIA Log Requests

Start with the [comprehensive development plan](docs/DEVELOPMENT_PLAN.md), then [handoff status](docs/HANDOFF_STATUS.md) and the [canonical structured PR registry](registry/prs.json).

The scope is official agency/component discovery, annual FOIA log request generation, a bounded dry run, controlled dispatch, deduplication, submission/fulfillment tracking and yearly continuation.

The specification is complete as a current engineering reconstruction. Original detailed campaign settings were not recovered. This repository has no application implementation or live dispatcher yet; the documentation does not authorize messages, fees or a future schedule. Large campaigns depend on the FOIA Aggregator corpus review and exact dispatch authorization described in the plan.

Validate the plan/registry using Python 3.11+ from this directory:

```bash
python scripts/validate_plan.py
```

Next work: **SFL-01 — Offline application foundation and configuration**, subject to the upstream priority recorded in the plan. Current documentation checks are separate from future runtime acceptance. `registry/roadmap.json` redirects to `registry/prs.json`; maintain work IDs, dependencies and real PR mappings there rather than inventing totals from observed PR numbers.
