# EDGAR Extractor

Give the agent a synthetic SEC-style filing excerpt; it extracts revenue, net income and total assets in full US dollars. Part of PersonalTrader's use of 10-K and 10-Q fundamentals.

## Tools

- `get_filing`: read one of six fictional filing excerpts (`f1` to `f6`).
- `pin_fields`: the answer key. NanoAgent runs it out of the model's sight; its output is the ground truth the verifier compares with. Not in the task's tools.

Task `extract-fields` (agent): read the filing with `get_filing`, then report the three numbers as integers in USD, `null` for a value the filing does not contain. The verifier requires an exact match per field.

All companies are fictional. The text was rendered from chosen values, so the answer key does not depend on a parser. Traps: units, column order, a loss in parentheses, a 10-Q quarter vs nine months, a missing balance sheet.

## Layout

- `nanoagent.yaml`: the manifest (tools, task, instructions).
- `contract.py`: typed input and output of every tool and task.
- `src/plugin/`: the MCP server (`__main__.py`), the tools (`tools.py`), the rules (`rules.py`) and the fixed data (`data.py`).
- `verifier/`: the deterministic verifier: one module for the tools (`tools.py`), one for the task (`task.py`), shared `checks.py`.
- `tests/`: tests of the rules, the tools and the verifier (correct, wrong, missing, malformed and boundary results).
- `ui/`, `product/`: how outputs are drawn, and the product page.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
```

The data is fixed and there is no network access, so every run gives the same result.
