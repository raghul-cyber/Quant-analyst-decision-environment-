# Final Submission Checklist 🚀

- [ ] `validate_local.py` passes all checks locally.
- [ ] `docker build -t qade .` builds safely without throwing layer errors natively.
- [ ] `docker run -p 7860:7860 qade` hosts environment securely without failing boots natively.
- [ ] `curl localhost:7860/health` executes returning exactly `{"status":"ok"}`.
- [ ] `curl -X POST localhost:7860/reset?task=easy` operates returning serialized `obs` block payload correctly.
- [ ] `python inference.py` connects with OpenAI bindings cleanly generating `[START]`, `[STEP]`, and `[END]` logging properly over all tasks.
- [ ] HuggingFace Space domain deployed and returns Code `200` successfully.
- [ ] Graders process outputs locally yielding mapped float ratios clamped accurately `[0.0, 1.0]`.
