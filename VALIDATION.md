# Maintenance validation

Maintenance performed November 2026. Commit timestamps may match the previous
repository head at the owner's request; they do not date these changes or results.

Linux cloud workspace, dedicated Python 3.12 virtual environment, pinned packages:

- `python -m pytest -q`: 5 passed.
- `python cover_match.py --demo`: identical synthetic candidate returned,
  histogram correlation 1.0, SSIM 1.0, 24 SIFT matches.
- Local query/gallery CLI: passed using temporary synthetic PNG files.

These are implementation smoke checks, not book-genre prediction metrics. The
original notebook was preserved unchanged and not executed end-to-end because it
requires external images and contains assumptions documented in README.md.
Docker was not installed, so the supplied Dockerfile has not been built.

## Presentation follow-up

Added a factual recruiter-oriented README, an actual generated HTML report, and
a report-content regression test. The report invokes the retrieval implementation
and embeds its synthetic query/gallery and computed scores without network calls.
Chromium screenshot capture was attempted but blocked by the environment's socket
restrictions. No screenshot or fabricated browser capture is claimed.
