# Decisions

- Original stdlib single-step declared-policy model, rather than adopting/forking a
  transport client. Requests/HTTPX reviewed as policy comparisons; their method/body,
  URL recovery/session/dependency scope is broader. No security certification inferred.
- Exclude URLs/body bytes/header values. Origin relation and replayability remain supplied
  assumptions; URI-reference resolution is a separate deferred alternative.
- Make 301/302 POST choice explicit, preserve307/308 methods, choose303 HEAD-for-HEAD/
  GET-otherwise. Separate body action from replay availability and unsafe from idempotent.
- Collect independent gates even after known stops. Relevant unknowns still make status
  unsupported; known proposals remain visible. Unknown method choice prevents invented
  body/unsafe conclusions. A hypothetical step never grants authority.
- Freeze complete independent reports and exact diagnostics/bounds/order/nulls before
  app code. 40 reports26/14 plus15 diagnostics and six artifact hashes remain unchanged.
- Preserve exact native type/no-hook admission and trusted delivery patterns from owned
  MIT media/range labs with attribution, independent local adaptation and no sibling imports.
- Keep frozen cap524288, below conservative Markdown allocation envelope997376. Observed
  stress did not overflow ordinary cap; only reduced-cap seams claim rejection coverage.
- Bounded local qwen3.5:2b extraction accepted, Codex retained security/code judgment.
  No remote inference/billing/new service/model download/provider change. No Git mutation,
  publication, external messaging, new chat/scheduler/subagent or successor here.
