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
