# Shop PDF reports

This repository is a reconstruction begun on 2026-11-05. It preserves the original repository and records newly executed, incremental checkpoints; this is not a claim of historical student development.

Python lane, little-shop dataset. Work is progressing through the seven required stages of the supplied PDF assignment; optional extras and AI rematch are excluded.

I would move rendering out of the request when report size or concurrent traffic makes the wait exceed the response-time target.

The daily check protects against double clicks creating duplicate PDFs; the in-process lock covers simultaneous requests when running the documented single worker. Without idempotency, a report-and-email feature could email the same customer twice and incur duplicate delivery charges. Use one worker; multi-process deployments would need a database-level lock.
