# Scenario timing comparison

1. Read the baseline named by the previous report and the later execution registry. Follow pointers until actual measured runs are found; a seed scenario registry can contain no execution data.
2. Inspect top-level values and per-run values separately. A registry can retain an old top-level duration while appending a later result. Select the intended run explicitly using date, revision, question and conditions.
3. Extract allowlisted fields with code: case identifier, execution date/revision, outcome, timing value, unit and measurement description. Inspect keys first, then reduce output; printing entire runs can expose private mail and flood context.
4. Compare the same metric: completed-screen observation with completed-screen observation, server duration with server duration, or the same processing stage. Label other measurements separately. Result-saving duration cannot replace total judgment time.
5. Preserve measurement semantics. Call UI upper bounds '완료 확인 시간'; preserve observed intervals as intervals. Exclude observer reconnect delays from response-duration claims.
6. Name baseline and later environments above the table. Local and production runs, changed dates or sources can explain differences; avoid assigning their full difference to the code change or calculating an unsupported improvement percentage.
7. Compute rounding, differences and row totals with code. Keep each selected run and metric in the working evidence. Validate evidence-link targets and Markdown table counts, accounting for header and separator syntax.
8. Put outcome beside duration. Faster answers that omit requested prices, dates, mail comparisons or final amounts remain unfinished. Recovered failures can be slower and still represent useful progress. Omit cases lacking the requested paired times instead of filling the table with '미측정'; report material recovered failures separately using their measured later duration.

Suggested columns: 질문 | 이전 완료 확인 시간 | 이후 완료 확인 시간 | 실제 답변·남은 확인. Use concrete dates in headers when several execution rounds exist. Keep source references in the evidence section and private raw data in protected project records.
