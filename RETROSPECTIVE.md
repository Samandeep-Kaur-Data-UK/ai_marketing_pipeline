# Project 2 Retrospective

## What Went Well

- The project now tells a clear business story: ingest customer text, score sentiment, surface complaint themes, and package the outputs for reporting and dashboarding.
- Comparing VADER against DistilBERT made the modelling choice much stronger than a single-model pipeline. The final recommendation is based on class-level business impact, not just headline accuracy.
- The Day 57 extension turned the repo into a more realistic analytics pipeline by combining review data with a second source and preserving source-level comparison.

## What Was Hard

- Local compute was the biggest constraint. Running heavier local LLM workflows alongside the rest of the pipeline was not a reliable long-term approach.
- The repository drifted while the project evolved. Script names, documentation, and output locations needed a cleanup pass before the repo felt professional enough to share.
- The binary DistilBERT checkpoint is a limitation for mixed review and social data because neutral-style posts still get forced into positive or negative labels.

## What I Would Do Differently

- Lock the final repo structure earlier so naming and file layout stay stable across the project.
- Move settings such as model provider, file paths, and runtime options into a configuration layer rather than keeping them only in individual scripts.
- Add lightweight tests and validation checks for row counts, schema expectations, and report generation so regressions are caught earlier.

## Next Improvements

- Replace or fine-tune the sentiment model with a three-class model better suited to multi-source customer text.
- Move the pipeline into a scheduled cloud workflow with an automated Power BI refresh.
- Add simple monitoring around source mix, negative-theme spikes, and failed report generation.
