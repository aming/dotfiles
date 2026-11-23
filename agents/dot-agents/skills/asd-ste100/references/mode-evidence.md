# Evidence for the 80% Default

This file records why the skill defaults to 80% and what the evidence does and does not show. It is not part of ASD-STE100.

## What the tests measured

- **Strict STE shortens text reliably.** Lucian Ghinda's August 2026 test of 60 code explanations found average sentence length fell from 17.8 words with no style instruction to roughly 9–10 words with either a loose plain-English instruction or a strict ASD-STE100 instruction. Kasra Aminiyeganeh's October 2026 test of 224 agent replies found sentences over 20 words fell from 8–9% to under 1%, and passive voice fell by more than half.
- **Strict STE did not improve model comprehension in those tests.** Aminiyeganeh's blind judges found no clarity gain, a 1.2-point naturalness loss and a 0.8-point nuance loss out of 5, and no improvement when a small model answered questions from the replies. Output tokens rose 55–106%, and Codex replies scored 0.85 of 10 lower.
- **Strict STE can lose facts.** Ghinda measured 46.8% of scored facts missing from Claude's strict ASD-STE100 explanations, against 8.5% for a loose "simple technical English" instruction. Codex lost about 40% under either instruction. The sample is small and informal, but it matches the qualifier loss reported by Aminiyeganeh's judges.
- **Human evidence supports STE for difficult procedures.** Shubert et al. (1996) found Simplified English improved comprehension and content-location accuracy for a complex procedure, with the largest gain for non-native readers, and no effect for a simpler procedure. Chervak et al. (1996) found the same pattern with aircraft maintenance technicians: a clear gain on difficult workcards, no significant change on easy ones.
- **Compliance is not verifiable from model output.** The ASD Simplified Technical English Maintenance Group's June 2026 white paper warns that AI-generated text can appear clear, authoritative, and consistent with STE without correctly applying its rules.

## What this does not show

No study compares 80% and 100% head to head. Karpathy's October 2026 "80% of the way" line was a compromise with a stringent specification, not a measured optimum. The default is defensible because it keeps the checkable structural rules and avoids the fact loss that strict prompting showed. It is not a claim that 80% is mathematically optimal.

## Sources

- Andrej Karpathy, post on X, 2 October 2026: <https://x.com/karpathy/status/2105819303471976479>
- Kasra Aminiyeganeh, "ASD-STE100 and LLMs: the myth, the legend, and what the evals say", 13 October 2026: <https://blog.thakay.dev/asd-ste100-and-llms/>
- Lucian Ghinda, "Explain to me in Simple Technical English", 14 August 2026: <https://allaboutcoding.ghinda.com/explain-to-me-in-simple-technical-english>
- Heather Holmback et al., "Issues in Conducting Empirical Evaluations of Controlled Languages", CLAW 1996: <https://mt-archive.net/90/CLAW-1996-Holmback.pdf>
- ASD STEMG, "ASD-STE100 Simplified Technical English and Artificial Intelligence (AI)", June 2026: <https://www.asd-ste100.org/assets/files/WhitePaper-ASD-STE100_and_AI.pdf>
