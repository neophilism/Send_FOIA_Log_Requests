# Send FOIA Log Requests — development and independent-account handoff plan

Plan version 2 · 2026-10-11 · Repository: `neophilism/Send_FOIA_Log_Requests`

Read this document and [HANDOFF_STATUS.md](HANDOFF_STATUS.md) first. [registry/prs.json](../registry/prs.json) is the canonical structured PR/work register. This plan makes an empty implementation repository independently developable. It is not a record of sent requests or an authorization to contact any agency.

## 1. Authority, source recovery and limitations

The owner's October 11 instruction requests comprehensive plans, recoverable requirements, executable milestones, acceptance tests, operational constraints, registry integration and an accurate update to [Engine Room's 26-repository audit #71](https://github.com/neophilism/Engine-Room/issues/71). It expressly identifies annual FOIA request generation, agency-directory discovery, controlled dispatch, submission tracking, deduplication and continuation as required scope. These are verified **current owner requirements**, even where earlier original wording cannot be recovered.

Evidence vocabulary:

| Class | What can be asserted |
|---|---|
| U | Direct October 11 owner instruction, summarized above; authorizes this planning/integration task. |
| A | October 10 audit #71: secondary recovery of intended scope, including automated component directory, annual requests, strict small dry run, contacts, dispatch/dedupe, submission/fulfillment proof, yearly continuation and source/rate controls. |
| R | Actual repository content/PR or pinned upstream document. Implementation evidence is not historical approval. |
| C | October 11 recovery of prior conversation summaries; records continuation constraints with source dates, not verbatim original transcripts. |
| E | This plan's reconstructed architecture, numbered work packages, data contracts, defaults and acceptance tests. Authorized engineering planning, not invented historical decisions. |

**Inspected baseline:** [`33acf4a4c78102092e9653984bb50b09199e5385`](https://github.com/neophilism/Send_FOIA_Log_Requests/tree/33acf4a4c78102092e9653984bb50b09199e5385). Only `README.md` (project title), `registry/roadmap.json` and `registry/prs.json` existed. There were **zero PRs, zero application files, zero tests, zero workflows**, and no verified runtime/deployment. The old registry's empty/unverified classification was accurate for that snapshot; it is preserved in git history and superseded by this plan.

No original numbered plan, original annual-request template, approved request years, complete recipient list, sender identity, fee authorization or transport/provider decision was recovered from the repository. Prior-context search also did not establish those details. Do not import assumptions from similarly named FOIA projects. Do not present a new template, database or milestone count as something the owner approved historically.

### Requirement and decision ledger

| ID | Scope that must survive handoff | Source and status | Work mapping |
|---|---|---|---|
| SR-01 | Discover agencies and individual FOIA components, with usable official contact/submission-directory evidence. | U/A; discovery sources and data model below are E | SFL-02, 03 |
| SR-02 | Generate annual FOIA log requests with explicit agency/component and year/period scope. | U/A; original years and calendar-vs-fiscal convention unresolved | SFL-03, 04 |
| SR-03 | Conduct a strict, small, reviewable dry run before any live dispatch. | A; exact historical sample size unavailable | SFL-06 |
| SR-04 | Controlled dispatch with validated destinations, rate controls and an explicit authorization record. | U/A; provider, live batch size and credentials unresolved | SFL-07–09 |
| SR-05 | Deduplicate requests, contacts and retries; preserve historical tracking. | U/A | SFL-02, 05, 07, 09 |
| SR-06 | Record submission evidence, agency acknowledgment/tracking, responses and fulfillment separately. | U/A | SFL-09, 10, 12 |
| SR-07 | Resume interrupted work and continue annually without losing prior years or sending duplicates. | U/A | SFL-05, 07, 11, 13 |
| SR-08 | Respect lawful access, official submission routes, provider/source limits and privacy. | A; engineering controls specified here as E | SFL-02, 07–10, 13 |
| SR-09 | Prioritize substantial Aggregator corpus expansion; check existing public logs before large campaigns. | R: pinned Aggregator plan; C: owner direction 2026-10-10 14:01 UTC | EXT-CORPUS and SFL-03, 12, 14 |
| SR-10 | Independent-account instructions and factual structured progress; no false historical/production certification. | U, audit #71 | All units and section 8 |

**Pinned upstream contract:** [FOIA_Aggregator development plan at `62fe82950963dcc0dde2003f094047d65bf79a9d`](https://github.com/neophilism/FOIA_Aggregator/blob/62fe82950963dcc0dde2003f094047d65bf79a9d/docs/DEVELOPMENT_PLAN.md), especially FC-01 source census, FC-03 logs, FC-08 identity, FC-13 exports, FC-14 broad-corpus review and downstream gating. This is a planning dependency, not proof those stages are done or an implemented endpoint exists. Require a concrete producer commit, export/schema version, source/period coverage, hashes, observation time and FC-14 evidence before a large live campaign.

Substantial implementation and campaign operations remain subordinate to that upstream priority. This plan-completion task, directory/data-format preparation and offline fixtures may proceed; no corpus gate is satisfied merely by writing documentation. Avoid coupling to an unverified live API or directly writing the Aggregator database.

## 2. Product behavior and boundaries

Build a reproducible request workflow: discover components → verify contacts → compare public log coverage → generate component-period drafts → deduplicate → dry-run/review → authorize an exact batch → submit through supported routes → reconcile proof and acknowledgment → track responses/fulfillment → export acquired log evidence → prepare the next annual cycle.

Primary users are the authorized requester/operator and a new coding account continuing the project. Initial deliverables are an operator CLI and durable ledger with reviewable exports; a public website, public requester directory, mass civic campaign, political analysis and integration into The Public Record are not recovered requirements. No need to build them to finish this repository. No live transport or scheduler exists today.

An annual request asks for existing FOIA request logs for the specified component/period. It is not the agency's statistical annual report, a demand to create a new database, or automatically a request for every underlying released document. Template design must make this distinction. Requested fields may include request/tracking identifier, receipt/closure dates, subject/description, disposition, processing status and fee fields **if maintained and releasable**; that field list is E and must be previewable. Do not require private requester names/contact details merely to collect operational log statistics.

Drafts contain exact date bounds, recipient/component, requester identity/contact, delivery preference, record description, fee instructions and applicable optional language. Never invent facts supporting a fee waiver, preferred requester category, expedited handling, standing authority or legal entitlement. Current law/agency instructions must be verified from official sources when implementing legal text or deadlines; this software plan makes no legal sufficiency guarantee or universal statutory countdown.

### Required campaign inputs — missing is a blocked live action, not a guessed value

| Input | Resolution/default |
|---|---|
| Jurisdiction and component allowlist | Begin engineering against U.S. federal component discovery indicated by the audit/upstream census; live batch requires an explicit reviewed list. State/local/international expansion is a new scope decision. No invented number of agencies. |
| Periods | Require explicit start/end dates and calendar/fiscal/custom basis. No inference of 1993–2025 from FOIA_Bias_Analysis. Annual recurrence does not authorize historical backfill. |
| Requester/sender | Obtain a verified requester profile, authorized identity/organization representation, reply route and sender credentials securely. Never pull personal contact information from chat memory into live requests. |
| Fees and representations | Unset fee authorization prevents sending a fee commitment. E safe setting is zero authorized spend until an explicit approved limit exists; fee waiver/expedition claims disabled until truthful basis supplied. This is not a recovered historical budget. |
| Delivery method | Verified official portal/API/email/postal route per component. No email provider or paid hosting is selected by this plan. Unsupported/manual routes remain tracked tasks. |
| Batch and rate | Dry-run E default: at most 3 explicitly selected component-period drafts, zero outbound messages; configurable lower. Live batch/rate caps require explicit values consistent with source/provider rules and authorization. Three was not recovered as an original requirement. |
| Annual continuation | Store a schedule specification, timezone, due-period rule and expiry in the campaign. Execution stays disabled until authorized. Preparing next year's drafts does not renew send authority automatically. |

Inputs must be fillable through a documented configuration/profile process when the app exists, not by editing code. Missing operational inputs do not block writing tests, schemas or the dry-run workflow.

## 3. Reconstructed architecture and data contracts (E)

Initial design: Python 3.11+ CLI, standard-library `unittest`, typed/versioned configuration, SQLite single-writer transactional ledger, local private artifact directory and adapter interfaces. This is a conservative engineering baseline for a repository without a stack; it is not an approved historical architecture or a current implementation. SFL-01 must lock and test concrete dependencies. Keep migration to another durable store possible but do not purchase/provision Render, Neon, a mail provider or object storage through a planning change.

Modules: directory discovery/verification; coverage comparison; templates/generation; request registry; approval and durable outbox; transport adapters; receipts/reconciliation; response/fulfillment intake; continuation scheduler; export/reporting. Separate pure draft generation from any network side effect. Dispatch code must require both an authorized frozen batch and an enabled transport; a scheduler cannot bypass those controls.

| Record | Contract/invariants |
|---|---|
| Component | Stable namespaced component ID, parent agency, jurisdiction, aliases/merger history, official source URLs and snapshot hash, observed/verified timestamps, current/inactive/unknown state. Agency and component are not interchangeable. |
| Contact route | Component, route kind, official destination, source proof, verification date, limitations, redirect history, verified/stale/invalid/manual state. Contact changes invalidate affected unsent batch authorization. |
| Coverage | Component + record class + exact period, source log artifact/hash, full/partial/unknown availability, missing fields/date gaps, retrieval evidence and reviewer decision. A link or annual statistical report is not a full log. |
| Campaign | ID/version, requester reference, explicit scope/periods, template revision, fee policy, caps, source/corpus version, scheduler configuration, draft/live mode, created/reviewed dates and authority expiry. |
| Request | Stable UUID; semantic dedupe key; component/period/record class/requester; exact rendered subject/body/attachments and hashes; source route version; current state plus append-only transition events. |
| Authorization | Authorizer/reference, time, expiry, exact recipient and request IDs, content/attachment hashes, sender, transport, batch/rate/fee caps and revocation state. Edits invalidate it; do not treat a PR merge as dispatch approval. |
| Dispatch attempt | Immutable attempt ID/idempotency key, leased job/worker, timestamp, provider request/message ID, status, bounded error class, receipt hash/reference, reconciliation state. Store no tokens in logs. |
| Response/fulfillment | Correlation evidence, agency tracking number, acknowledgment and response events, received artifact hashes, period/field coverage, partial/final/no-records/denied/referred classification, action required and provenance. |
| Continuation/export | Prior cycle link, new explicit due interval, dedupe/coverage decision, frozen manifest and export/schema version, downstream acknowledgment and unresolved errors. |

**Deduplication:** stable semantic key = requester principal + jurisdiction + canonical component + record class + exact period. Changing wording, provider or template version must not create a fresh send entitlement. Record overlapping intervals and predecessor/component aliases for review. Amendment/replacement/supersession needs an explicit event and reason; do not delete old evidence. Publicly available full coverage can suppress a redundant draft; partial/unknown coverage must not silently count as fulfilled.

**Request state machine:** `draft → validated → dry_run_reviewed → authorized → queued → submitting → submitted → acknowledged → response_received → fulfilled/partially_fulfilled/closed_unfulfilled`. Branch states include `blocked`, `rejected`, `cancelled`, `delivery_failed` and `submission_unknown`. Maintain independent response events so a genuine response can be correlated even if the submission callback was lost. Every transition has evidence and actor/time. Provider acceptance, transport delivery, agency acknowledgment and actual fulfillment are distinct facts.

**Ambiguous sends:** timeout after the provider may have accepted a submission enters `submission_unknown`. Reconcile using provider idempotency/status or agency receipt; never blindly resend. SMTP and many web forms cannot guarantee exactly-once delivery; the honest safety property is durable intent, bounded attempts and no automatic resend of unknown outcomes. Hold an exclusive/leased outbox claim and audit revocation/expiry immediately before dispatch.

## 4. Executable milestones

`SFL-01`–`SFL-14` are E work packages created October 11, not historical PR numbers. No application work was present to mark complete. New commands/test files described below are required deliverables, not currently runnable tools. All units require `python scripts/validate_plan.py` and, once SFL-01 creates it, a nonempty `python -m unittest discover -s tests -v` suite. Test transports never contact a real person/agency.

### SFL-01 — Offline application foundation and configuration

**Prerequisites:** this plan and current branch/PR inspection. **Deliver:** package/CLI, tested lock/environment, explicit modes, strict typed configuration, migration framework, deterministic fixtures, standard test/CI entry point, no-network help and default dry-run behavior. Document exact installed CLI spelling; use command families `directory`, `campaign`, `draft`, `review`, `dispatch`, `receipt`, `response`, `continue`, `export` without pretending they exist now. **Acceptance:** fresh clone installs and runs fixture suite/help with no credentials/network; missing or invalid configuration fails before side effects; live transport disabled by default; zero tests is a failure.

### SFL-02 — Official agency/component and contact discovery

**Prerequisites:** SFL-01. **Deliver:** ingest official directory data and pinned Aggregator census fixture; source-specific official contact verification; pagination, aliases, parent/child identity, source snapshots and route freshness states. Verify current official endpoint/auth/schema before live adapter work. **Acceptance:** multi-page directory fixture with redirects, duplicate names, renamed/retired/unknown components and multiple routes yields stable distinct IDs; unsafe URLs/redirects and nonofficial unsupported contacts are rejected or unverified; 403/429/backoff leaves an actionable queue. No hard-coded universal agency count or guessed addresses.

### SFL-03 — Annual period selection and public-log gap analysis

**Prerequisites:** SFL-02; upstream export fixture contract. **Deliver:** component-period inventory, calendar/fiscal/custom interval semantics, existing published logs comparison, overlap/coverage report and explicit live scope manifest. **Acceptance:** leap year, cross-year/fiscal-year, overlapping/backfill periods, full/partial/missing logs and component mergers; annual totals cannot satisfy log coverage; unknown coverage remains unknown; no implicit Bias-analysis year range. Offline implementation may proceed while EXT-CORPUS evidence remains absent.

### SFL-04 — Versioned request templates and deterministic generation

**Prerequisites:** SFL-03. **Deliver:** editable templates and validated requester/fee profile; rendering to UTF-8 text plus review manifest; correct component/period and available-record description; output hashes and missing-input reasons. Keep optional legal representations off without supported inputs. **Acceptance:** golden fixtures preserve exact date/recipient/record scope; missing identity, fee policy or route prevents live-ready status; safe escaping and length/attachment bounds; no fake signature, promises of payment or private requester-field demand added automatically. Template changes create revisions, not new dedupe keys.

### SFL-05 — Durable request ledger and semantic deduplication

**Prerequisites:** SFL-04. **Deliver:** entities/state events in section 3, migrations, unique semantic request keys, interval-overlap and historical-import checks, idempotent draft creation and backup. **Acceptance:** repeated/reordered imports, simultaneous workers, changed template, changed contact aliases and restored database cannot produce duplicate canonical requests; old receipt history survives; an intentional amendment records its link/reason without erasing prior events.

### SFL-06 — Strict small dry-run and review packet

**Prerequisites:** SFL-05. **Deliver:** bounded selected-component preview (E default maximum 3), exact recipients/content/attachments, fees, duplicate/coverage decisions, missing-input report, run manifest and audit trail. Use injected transports that cannot send. **Acceptance:** outbound send functions are never called; attempted live mode is denied; count cap holds under parallel generation; packet hashes reproduce; obvious address/date/template mistakes are visible. Full-scope dry-run expansion is a separate explicit operator setting, never a reason to contact agencies.

### SFL-07 — Exact-batch authorization and transactional outbox

**Prerequisites:** SFL-06. **Deliver:** immutable authorization envelope, preview-to-send hash binding, explicit revocation/expiry/caps, least-privilege operator roles, transactionally queued intent, leasing and emergency stop. **Acceptance:** unapproved/expired/revoked batch denied; editing text, destination, attachments, sender, fees or scope invalidates approval; race tests preserve caps and one claim; stop prevents future sends; recovery retains evidence. No documentation/CI/GitHub merge implicitly authorizes transport.

### SFL-08 — Controlled submission adapters and rate limits

**Prerequisites:** SFL-02, SFL-07; EXT-DISPATCH for any real message. **Deliver:** transport interface and mock; implement only actually verified official routes, with separate API/email adapters when supported and manual portal/postal task export otherwise. Provider credentials remain external. Per-destination/global limits and retry classification apply with and without authentication. **Acceptance:** fake-provider success, rejection, 429/Retry-After, 401/403, bounce, invalid redirects, timeout and stop tests; exact frozen content is transmitted only once per safe intent; unsupported portal/CAPTCHA stays manual/blocked. A success fixture is not a live dispatch test. Do not automate around access controls.

### SFL-09 — Submission receipts, acknowledgments and uncertain outcomes

**Prerequisites:** SFL-08. **Deliver:** durable provider receipts and original evidence artifacts, agency tracking IDs, delivery/acknowledgment states, bounded reconciliation and manual evidence import with provenance. **Acceptance:** crash after remote acceptance/before local commit enters unknown; duplicate callbacks are idempotent; failed receipt save never claims proven submission; transport acceptance cannot mark acknowledged or fulfilled; no blind retry of uncertain sends. Verify manual receipt authenticity/source as a reviewable operator claim, not an invented API response.

### SFL-10 — Response intake and fulfillment accounting

**Prerequisites:** SFL-09. **Deliver:** import responses and attachments with exact hashes/correlation, partial/no-records/denial/referral/fee/clarification states, missing periods/fields report and operator follow-up tasks. Intake remains manual/upload-first until a provider integration is evidenced. **Acceptance:** wrong-request and duplicate responses do not overwrite cases; malicious/oversize attachments quarantined; partial response does not close all periods; referral retains both agencies and original request; fee demand pauses without paying; no automatic appeal, legal deadline or follow-up message is invented. Any legal deadline rule must carry current official authority and configuration.

### SFL-11 — Restart and yearly continuation

**Prerequisites:** SFL-05, SFL-07, SFL-10. **Deliver:** recoverable job cursor/leases, next-cycle draft generation, timezone/date policy and explicit scope rollover; preserve old cycles and check current contacts, existing public logs, duplicates and authorization validity again. **Acceptance:** crash/restore/repeated annual trigger yields one set of next-cycle drafts; leap years and missed cycles handled explicitly; earlier periods remain auditable; prior-year approval never silently authorizes a new campaign unless a real standing authorization expressly includes it. Scheduler disabled by default; only a deliberate authorized configuration enables it.

### SFL-12 — Aggregator interchange and completion reporting

**Prerequisites:** SFL-03, SFL-10, SFL-11; EXT-CORPUS for large-campaign readiness. **Deliver:** versioned export/import manifests for directory/coverage and fulfilled logs; no shared-database writes; source/receipt relationships, checksums, privacy filtering and idempotent downstream acknowledgment. **Acceptance:** fixture import/export round trip preserves component/period/file provenance; retry does not duplicate objects; requester contact/credentials absent from public export; upstream unavailable state explicit. Real integration pins producer/consumer commits and export schema/hash; Aggregator plan existence alone is insufficient.

### SFL-13 — Secure durable operation, monitoring and recovery

**Prerequisites:** SFL-07, SFL-09, SFL-11, SFL-12. **Deliver:** private operator access, durable storage/backup, migration/rollback, secrets procedure, sensitive-log minimization, source/provider budgets and health/status reports. Hosted runtime/scheduler must be actually authorized and persistent; no ephemeral CI artifact as sole request/receipt ledger. **Acceptance:** isolated restore preserves every request/event/receipt hash and dedupe key; restart never resends submitted/unknown requests; concurrent worker exclusion, key rotation, permission denial, low disk and provider outage tests; evidence of deployment/service revision only if deployed. No new paid service or spending through this unit without authorization.

### SFL-14 — Authorized bounded pilot and independent-account acceptance

**Prerequisites:** SFL-01–13; EXT-CORPUS, EXT-DISPATCH and any chosen hosting/transport credentials. **Deliver:** dry-run evidence first; if separately authorized, a precisely bounded live pilot, proof/reconciliation report, operator handoff and release manifest. **Acceptance:** verify only the approved recipient/scope/count, match each sent attempt to actual evidence, account for unresolved/no-response cases, restore safely, and let a fresh account reproduce fixture workflow from repository instructions. Agency response latency is an external dependency; a submission pilot cannot certify fulfillment. Large campaigns remain blocked until corpus review and applicable authority exist. If gates absent, record “implementation/dry-run only; live pilot blocked,” not unconditional completion.

## 5. Acceptance matrix and external gates

| Gate | Evidence needed | What can continue without it |
|---|---|---|
| EXT-CORPUS | Current Aggregator census/log dedupe + broad coverage review (FC-14), export schema/commit/hash and gap report. Verify scope actually covers the intended components/periods. | Documentation, directory/data-format preparation and deterministic tests; do not promote a large live campaign or claim all public alternatives checked. |
| EXT-DISPATCH | Explicit authority for concrete recipients, requester, frozen content/attachments, periods, transport, time/caps/fees, valid contact evidence and credential access. | All dry-run/review/mock transport work. No message is authorized by this plan. |
| EXT-RUNTIME | For a chosen host: legitimate owner/access, approved resource/budget, durable ledger/artifacts, secret locations, release revision, restore and worker liveness. | Local tests/CLI and runbook. A Render project/Neon link does not prove a service exists. |
| EXT-RESPONSE | Actual agency acknowledgment/response/receipt, verified against request and period; no guessed deadlines or fulfillment. | Submission tracking and response fixtures; unresolved cases remain visible. |

Required automated fixture groups: component identity/pagination/contact changes; period and coverage comparison; exact template output; missing configuration and false claims; semantic/overlap dedupe; dry-run zero sends; approval tampering/expiry/revocation; concurrent outbox/limits; ambiguous send/restart; receipt correlation and duplicate callbacks; partial/denied/referred responses; safe attachments and redaction; annual rollover; backup/restore and export round trip. SFL-14 alone adds an explicitly authorized real-world pilot. Do not send a “test” to a government official from CI.

Test gates verify behavior, not that FOIA law, provider terms or agency handling will accept a particular request. Link any implemented legal/template rules to verified official sources at implementation time and preserve their review date; stale contact/policy rules block affected sends until refreshed.

## 6. Operating constraints and incident response

**Durability:** one authoritative ledger and artifact store; exclusive writer or tested transaction/lease coordination. Scheduled runs must restore/attach that state before preparing work. Version backups with checksums and private permissions; only an isolated restore target can prove recovery. Never overwrite a more complete receipt ledger with an older runner snapshot.

**Privacy/secrets:** least-privilege authorized operator access; separate public component information from private requester profiles/correspondence. Encrypt transport where supported and protect backups with keys stored separately; do not claim end-to-end encryption for server-readable mail/records. Maintain a recorded retention/access policy without fabricating a legal retention period. Redact keys, personal addresses, bodies and sensitive attachments from logs/PR artifacts; private source material does not become publishable just because a request is fulfilled.

**Rate/cost:** maintain per-host discovery limits and per-provider/global dispatch caps; honor retry and access failures. No bypass of authentication, CAPTCHA or source restrictions. A paid API, postage, records fee, new service plan or additional storage needs actual authorization. Exhausted caps pause affected jobs with counts and next action; do not drop or silently retry the whole campaign.

**Monitoring:** show directory freshness and unknown contacts; drafts/duplicates/suppressed-by-coverage; authorized/queued/submitting/unknown/submitted/acknowledged/fulfilled/partial/blocked counts; oldest stuck job; last durable checkpoint; response correlation failures; backup age and restore result. Distinguish `not configured`, `never run`, `degraded` and `healthy`. A process-up flag cannot certify submissions.

**Incident actions:** disable dispatch first on duplicates, compromised credentials, unexpected recipients or ambiguous remote outcomes; preserve ledger and receipts; revoke affected authorization/keys; reconcile provider state before resume. For migration/release failure, stop writers and restore a verified copy without losing newer sent attempts. Prefer forward-compatible migrations; irreversible migrations require a reviewed backup/restore plan. Never “roll back” a sent message by deleting its record.

## 7. Canonical registry and progress interpretation

`registry/prs.json` conforms to Engine Room schema v1, with `roadmapVersion: 2` and exactly **14** completion units. `origin: addition` identifies a newly reconstructed numbered plan; the requirement ledger distinguishes inherited scope. `planVerified: true` means the current plan/registry have been checked and enumerated under the current owner instruction, **not** that historical conversations, implementation, live dispatch or unconditional handoff are certified. `historicalPlanVerified: false` and `handoffCertified: false` retain those limits.

Initially there is no historical application PR evidence and each completion `prs` array is empty. The documentation PR itself does not fulfill runtime milestones. Preserve real observed PR records as they appear; do not invent GitHub PR IDs, merge times or progress. `plannedPrCount` must equal unit count; only explicitly associated, actually merged completion PRs count green. A unit needing several PRs includes all prerequisites necessary for its acceptance, not just the first scaffold PR. Add scope through a dated amendment/version increment.

`registry/roadmap.json` is a compatibility redirect, not a competing editable plan. Never infer the plan denominator from open/merged PR counts or from Markdown titles. Engine Room should read the repository registry and live GitHub observations; do not manually edit its dashboard or bundled progress data for routine updates. Consumer parser validation does not establish that the live dashboard refreshed.

## 8. Independent-account start and handoff protocol

1. Use your own authorized GitHub connection to clone, inspect current main, all open PRs/branches and checks. Read this plan, handoff status, README and `registry/prs.json`. No `AGENTS.md` was present at the inspected baseline; follow any later-added instructions. Do not duplicate another account's active work or trust October 11 PR counts indefinitely.
2. Current command available after this documentation change:

   ```bash
   python scripts/validate_plan.py
   ```

   It validates documentation/registry consistency using the standard library. There is currently **no application install, dispatcher, database migration, test suite or deployment command**. Do not run guessed commands or report zero tests as success. SFL-01 must supply exact setup and `python -m unittest discover -s tests -v` with a nonempty suite. Treat section 4's command families as future interfaces.
3. Next package: **SFL-01**, within the upstream priority constraints; SFL-02/03 directory and data contracts follow. Until Aggregator's coverage gate is evidenced, keep preparation offline/read-only and record the block on substantial operations. Start with fixture directory, private dummy requester profile, fake transport and explicit sample periods; they are synthetic test data, never production-ready drafts.
4. For each unit, create a scoped PR with work ID, source requirement IDs, real prerequisite commits/versions, tests, data effect and rollback. Under the owner's standing workflow, chain/merge passing conflict-free work. Stop only affected work for failed gates, conflicting changes, missing credentials/authority or consequential unanswered scope; continue independent preparation. Never substitute a previous account's hidden state for a committed contract.
5. Before transport implementation, inventory verified official route, secure sender/provider access, exact authorized requester/campaign and fee/rate caps. Before hosting, verify actual service ownership and persistence; no Render or Neon deployment was established by this audit. Keep secret values out of the repository and handoff; record where the next authorized account obtains access.
6. Before release, stop the outbox, back up ledger/artifacts, pin release and dependencies, migrate an isolated copy, run fixture acceptance/restore, compare request/receipt hashes, then re-enable only valid authorized work. A real pilot requires EXT-DISPATCH and EXT-CORPUS evidence. No autonomous future schedule is created by documenting annual continuation.
7. Record the deployed/local release commit, test command/result, upstream export version, real submission/response evidence or honest absence, blockers, current open/merged PR mapping and next-ready ID in HANDOFF_STATUS with UTC verification time. Recheck current official source requirements when implementing templates/contact validation, not from stale chat memory.
8. Historical fidelity requires original source recovery or owner ratification of a new dated baseline. Operational readiness requires tested software and actual credentialed evidence. Independent-account certification requires a fresh account to reproduce setup/dry-run and exercise applicable recovery/integration gates. This document completes the missing specification; it does not close those separate certification requirements.
