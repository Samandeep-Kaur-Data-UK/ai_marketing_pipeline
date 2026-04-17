# Project 2 Retrospective

## What Went Well

- The final repo tells a clear business story: ingest customer text, score sentiment, surface complaint themes, and package the outputs for reporting and dashboarding.
- Comparing VADER against DistilBERT made the modelling choice stronger because the recommendation is supported by class-level business impact, not just headline accuracy.
- The Day 57 extension turned the repo into a more realistic analytics pipeline by combining review data with a second source and preserving source-level comparison.
- The project now includes reports, notes, visuals, and a Power BI asset, which makes it much easier for a recruiter or hiring manager to review quickly.

## What Was Hard

- Local compute was the biggest constraint. Heavier local LLM workflows were not reliable enough to keep in the final version.
- The repository drifted while the project evolved, so script names, documentation, and output locations needed a cleanup pass before the repo felt portfolio-ready.
- The binary DistilBERT checkpoint is still a limitation for mixed review and social data because neutral-style posts are forced into positive or negative labels.

## What I Would Do Differently

- Lock the final repo structure earlier so naming and file layout stay stable across the project.
- Move provider settings, file paths, and runtime options into a configuration layer rather than repeating them across scripts.
- Add lightweight tests and validation checks for row counts, schema expectations, and report generation.

## Next Improvements

- Replace or fine-tune the sentiment model with a three-class model better suited to multi-source customer text.
- Move the pipeline into a scheduled cloud workflow with automated refreshes.
- Add simple monitoring around source mix, negative-theme spikes, and failed report generation.
