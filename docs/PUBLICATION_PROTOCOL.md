# Publication Protocol

This public repository receives only approved materials.

## Before Publication

Check:

— no secrets;
— no passwords;
— no API keys;
— no private contact data;
— no partner-sensitive data;
— no unapproved drafts;
— license notice is present;
— attribution to Landau Fund is present;
— source repository link is present;
— changes are indicated if material was adapted.

## Publication Record

Important releases should be supported by:

— a public commit;
— a changelog entry;
— a public GitHub issue or discussion;
— citation metadata in `CITATION.cff`;
— document-level license notice when the release is a standalone document.

## Release Candidate 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_RELEASE_CANDIDATE_1_0_0/` package is a technical release-candidate gate. It does not state that antigravity is proven. A final `RELEASE_1_0_0` requires scientific, data, license, patent, and security/privacy review after the strict manifest check passes.

## Release Review 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_REVIEW_RELEASE_1_0_0/` package records the review gates that must close before final release 1.0.0: scientific review, data review, license review, patent review, and security/privacy review. Until these gates are closed, the package remains a release candidate and no final `RELEASE_1_0_0` should be announced.

## Operational Closure 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_ОПЕРАЦИОННОЕ_ЗАКРЫТИЕ_ПРОВЕРКИ_РЕЛИЗА_1_0_0/` package converts the review gate into an auditable decision workflow: assigned roles, evidence log, nonconformity/corrective-action log, reviewer conclusion template, and GO/NO-GO protocol. The default state remains `NO-GO` until the required roles are assigned, evidence is recorded, blocking nonconformities are closed, hashes are verified, and the final decision is documented.

## Machine Evidence 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_МАШИННЫЕ_ДОКАЗАТЕЛЬСТВА_REVIEW_1_0_0/` package records machine-checkable evidence for review 1.0.0: local file hashes, Bitrix24 folder/file IDs, public/private GitHub snapshot commits, automated SHA-256 verification, review-role task handoff, and the boundary between machine checks and human review. This gate improves traceability only. It does not prove antigravity, does not close scientific/data/license/patent/security review, and does not authorize final `RELEASE_1_0_0`.

## Human Review Execution 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_ИСПОЛНЕНИЕ_ЧЕЛОВЕЧЕСКОЙ_ПРОВЕРКИ_1_0_0/` package defines the execution layer for human review: role assignment registry, independence and conflict-of-interest declaration, reviewer material handoff, conclusion intake log, `NC-001..NC-006` closure matrix, and release board protocol. This gate does not assign real people automatically, does not replace signed conclusions, and preserves `NO-GO` by default until review roles, conclusions, nonconformities, and the release decision are closed.

## Outreach Execution And Reviewer Access 1.0.0 Gate

The `docs/АНТИГРАВИТАЦИЯ_ЖУРНАЛ_ИСПОЛНЕНИЯ_OUTREACH_И_ДОПУСКА_РЕЦЕНЗЕНТОВ_1_0_0/` package records the auditable execution layer for reviewer and grant outreach: first-contact tracking, candidate response handling, NDA/COI checks, access-control status, grant opportunity tracking, private-material access protocol, and refusal/silence handling. It does not send messages, does not confirm reviewer participation, does not grant private access, and preserves `NO-GO` by default until real signed conclusions and nonconformity closure exist.
