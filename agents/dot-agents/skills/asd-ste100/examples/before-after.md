# Before / After Examples

## Part 1 — STE Rule Illustrations

These are illustrative rewrites, not verified compliant documents. Consult the official Issue 9 and `references/rule-coverage.json` for each rule and its exceptions. Vocabulary, meanings, and terminology still need review.

| Rule | Before | After | Why |
|---|---|---|---|
| Consistent terms for the same action | "Check the cable connection. Verify the cable connection again after startup." | "Check the cable connection. Check the cable connection again after startup." | Use one term when the source refers to the same action. Preserve distinct actions and objects. Dictionary approval is not verified here. |
| Technical nouns are not verbs (1.7) | "Oil the valve." | "Apply oil to the valve." | “Oil” can qualify as a technical noun for a material. Do not use that technical noun as a verb. |
| Precise verb meaning | "Follow the safety instructions." | "Obey the safety instructions." | "Follow" can mean "come after" or "obey" — STE picks the unambiguous one. |
| Simple tense (3.2/3.4) | "We have received the technical reports from HQ." | "We received the technical reports from HQ." | The revision removes a complex tense. If present relevance carries necessary information, preserve it in a permitted construction or report the conflict. |
| Verb, not noun | "Perform an inspection of the filter." | "Inspect the filter." | The noun form hides the action and adds a filler verb that carries no meaning. |
| No phrasal verbs | "Take off the access panel." | "Remove the access panel." | "Take off" also means "depart" and "deduct" — the two words together do not predict the meaning. |

## Part 2 — 80% Mode Applied to Agent Output

These original examples use 80% mode, not the full STE review contract. They can retain necessary vocabulary and verb constructions that STE does not permit. An explicit STE request also needs the official dictionary, approved project terminology, all applicable rule reviews, and disclosure of remaining issues.

Word counts below are whitespace-separated tokens (`text.split()`), punctuation not counted separately. A different tokenizer will produce a different number.

### Example A — Tool description

**Before:**
> This tool will attempt to synchronize state across the various backends that have been configured, and if a conflict is detected it may resolve it automatically depending on the strategy that has been set, or otherwise it will surface the conflict for manual review.

**Violations flagged:**
- Multiple described behaviors in one long sentence (synchronize, resolve, and report).
- Present perfect in the relative clauses ("have been configured", "has been set").
- 44 words, far over the 25-word descriptive cap.

Note what is *not* flagged: "will attempt to" and "may resolve". Those are hedges, not violations. The tool is not promised to succeed, and the rewrite must not promise it either.

**After:**
> The tool will try to synchronize state across the configured backends. If it detects a conflict, it may resolve the conflict automatically, depending on the configured strategy. Otherwise, it will report the conflict for manual review.

The rewrite preserves "otherwise" because the source does not specify whether the fallback depends on the strategy or the resolution outcome. Ask for clarification if that distinction must be explicit. Do not invent a strategy-reading operation.

### Example B — Error message

**Before:**
> An error may have occurred while processing your request due to a possible mismatch in the expected data format, which could be caused by an outdated client version.

**Violations flagged:**
- One sentence carrying three separate claims (an error occurred, a format mismatch, a client version).
- 28 words, over the descriptive cap.

Not flagged: "may have occurred" and "could be caused by". The message is written by a system that does not know what went wrong. Both hedges are accurate reporting of that ignorance.

**After:**
> An error may have occurred while processing your request. A mismatch with the expected data format may have caused the error. An outdated client version could have caused this mismatch.

**This example is the reason the modality rule exists.** An earlier version of this file rewrote the first sentence as "The request failed", and the third as "an outdated client **is the most common cause**". Both read better. Both are wrong: the first asserts a failure the system only suspects, and the second invents a frequency claim that appears nowhere in the input. A rewrite that supplies a cause, a frequency, or a mechanism has stopped being a rewrite.

80% mode retains the compound form to protect meaning. In STE review, flag the construction under 3.2/3.4, then seek an approved construction with the same uncertainty. If none is established, preserve the source meaning and report that compliance is unresolved.

### Example C — Inter-agent instruction

**Before:**
> Once the upstream job has completed and assuming no errors were raised, the downstream agent should proceed to consume the output artifact, though it is worth noting that partial artifacts are sometimes produced under timeout conditions.

**Violations flagged:**
- Present perfect ("has completed") and subordinate-clause stacking ("assuming...", "though it is worth noting...").
- One sentence, three separate facts (completion condition, next action, edge-case warning).
- 36 words, over the 20-word instruction cap.

**After:**
> After the upstream job completes without errors, the downstream agent should read the output artifact. Partial artifacts are sometimes produced under timeout conditions.

The rewrite preserves "should" as a recommendation, "sometimes" as the stated frequency, and the passive because the source does not name who produces a partial artifact. It adds no completeness check or waiting instruction.

### Example D — README prose (80% mode)

**Before:**
> Our caching layer is designed to slot seamlessly into your existing stack with minimal friction and no vendor lock-in; it leverages semantic similarity to dramatically reduce the cache misses that traditionally plague LLM workloads.

**Violations flagged:**
- Marketing adjectives and claims without measurement ("seamlessly", "minimal friction", "dramatically").
- Semicolon joining two separate ideas.
- Nominalization and soft phrasing ("is designed to slot into", "leverages").
- 34 words, over the 25-word descriptive cap.

**After:**
> We designed our cache layer to fit into your current stack without vendor lock-in. It uses semantic similarity to reduce cache misses, a long-standing problem for LLM workloads.

80% mode did not force a fixed vocabulary. It removed marketing language and the semicolon, and shortened the sentences. It kept "designed to", because the input states a design goal, not a result.

An earlier version of this file added two facts. It said that a normal cache matches requests by exact text. It also said that this cache stores no data outside your stack. The input states neither fact. A rewrite that adds a fact is no longer a rewrite.

## How to Read These Examples

Part 1 illustrates selected STE principles. Part 2 illustrates meaning-preserving 80% rewrites. Neither part replaces the complete Issue 9 review or establishes official dictionary compliance.
