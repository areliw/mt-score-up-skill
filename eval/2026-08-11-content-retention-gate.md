# Content-retention gate — patch review pack

## Candidate

- Original receipt target: `video-editing` candidate `b427ed88d259`.
- Source problem: the installed `video-editing` skill is external and has no source file in this repository, so it cannot pass the repository PR/sync pipeline.
- Routed source skill: `skills/content-creator-judgment.md` because the missing decision is whether the raw material can support the promised content; editing execution remains in `video-editing`.
- Scope: long-form story, challenge, gameplay, vlog, or case-journey footage only.

## Proposed fork

Before editing, require observable `promise → movement → payoff`. Movement means a real change in information, decision, obstacle, or state that makes the payoff meaningful; it has no fixed beat count. If one part is absent, choose the remedy for that missing part rather than manufacturing a Long with compression or effects. Preserve causal truth and honest pivots while allowing clearly disclosed cold opens. Exempt tutorial and ambient/cozy formats by testing fulfillment of their own promise.

## Adversarial review

### Take

- The fork operationalizes the skill's existing hook/moment rule at the post-capture decision point.
- It separates content feasibility from editing craft, preventing technically clean but narratively empty output.
- It permits truthful failure and pivots instead of requiring a win.
- It permits a complete one-turn story and a truthful cold open; neither chronology nor a fixed number of beats is mandatory.

### Drop or narrow

- Do not require escalating stakes for every video.
- Do not reject tutorials that have a clear problem, steps, and result.
- Do not reject ambient/cozy/ASMR videos whose promise is a sustained experience.
- Do not claim that three beats guarantee retention or views.

### Evidence status

De-identified receipt `b427ed88d259` records the originating failure: a technically compressed chronological rough remained unengaging because the raw supplied no accumulating change, and further effects were proposed before content feasibility was rechecked. The patch is additionally supported by an internal consistency gap: the existing skill gates topics on a hook/moment but had no equivalent gate after footage existed. Treat this as a draft fork until forward evidence confirms it fires correctly.

## Locked regression cases

### Positive trigger 1 — dead gameplay Long

Raw footage contains many visually different rounds, but the stated challenge never changes, no meaningful decision occurs, and there is no final result. Expected: reject forced Long; propose Short/Discovery, a truthful narrower promise, or re-recording. Effects are not the remedy.

### Positive trigger 2 — honest pivot

A player promises a perfect-lives win, loses one life, then continues toward winning before lives reach zero and reaches a real ending. Expected: state that the first challenge failed and use the second goal as Act 2. A preview is allowed if it does not conceal the failed first goal.

### Positive trigger 3 — movement without payoff

A case journey contains investigation and changing hypotheses but stops before a diagnosis or declared unresolved endpoint. Expected: narrow the promise to the investigation, end explicitly unresolved when the format supports it, or record more; do not invent closure.

### Positive trigger 4 — payoff without enough movement for a Long

A challenge clip jumps from setup to a successful reveal in 40 seconds, with no process that adds value. Expected: keep it as a Short/reveal, unless added analysis or process is itself the stated promise.

### Positive trigger 5 — strong moments without a supportable promise

Footage has funny isolated reactions but no question or outcome connecting them. Expected: package a moment-led Short/Discovery; do not retrofit a large challenge promise.

### Negative trigger 1 — software tutorial

A screen recording calmly shows a spreadsheet error, the repair steps, and a working result without drama or escalating stakes. Expected: accept as a Long if the learning objective is useful; do not demand artificial jeopardy.

### Negative trigger 2 — cozy process

A repair/ASMR video promises a relaxing complete restoration and delivers the process and finished object at an even pace. Expected: assess continuity and promise fulfillment; do not reject it for lacking conflict.

### Negative trigger 3 — one-turn complete story

A one-attempt test promises to discover whether a cheap controller survives one destructive test; the test and result are both visible. Expected: accept the causal spine even though it has only one material turn.

### Negative trigger 4 — truthful cold open

A challenge opens with a clearly labeled two-second preview of the final fall, then returns to the start and truthfully shows how it happened. Expected: allow the non-linear hook; reject only if the preview falsifies success, hides a failed goal, or spoils the entire value.

## Structured fixture contract — not yet wired to the A/B harness

Machine-readable prompts and expected boundaries are stored in `content-retention-gate-cases.json`. The current `eval/harness/ab-x3.js` does not read this schema, so the file is locked test input—not executed promotion evidence. A promotion-grade runner or equivalent managed Workflow must execute every case and score three axes independently:

- `decision`: chooses Long vs Short/Discovery vs narrower promise/record-more appropriately;
- `truth`: does not invent a payoff, erase a failed goal, or misrepresent chronology;
- `boundary`: does not demand artificial stakes from tutorial, cozy/ambient, one-turn, or truthful-cold-open cases.

A critical regression is any patched answer that fails `truth` or rejects a negative-trigger case solely for lacking multiple beats.

## Promotion gates

1. Wire the structured fixtures into a blind controlled A/B with baseline, generic-careful control, and patched skill at act-grade reps, or run an equivalent managed Workflow that records the same case-level axes.
2. Require all 5 positive triggers to fire and all 4 negative triggers not to fire.
3. Record no critical regression and rebuild A/B coverage after the current body hash changes.
4. Pass repository validation, duplicate check, A/B gate, and maturity gate in a PR.
5. Sync source to Claude, Codex, and Drive; verify body hashes.
6. Observe three real uses. Any harmful over-trigger or forced-story behavior rolls back the fork.

This file is a review/evaluation record, not promotion evidence by itself.
