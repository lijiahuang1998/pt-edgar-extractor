import re

import pytest

from contract import Filing, FilingInput
from plugin import IMPLEMENTATIONS, rules
from plugin.data import ANSWERS, FILINGS
from plugin.tools import get_filing, pin_fields

SCALE = {"in thousands": 1_000, "in millions": 1_000_000, "in dollars": 1}


def number(token: str) -> int:
    """'1,234' -> 1234 and '(1,234)' -> -1234."""
    value = int(token.strip("()").replace(",", ""))
    return -value if token.startswith("(") else value


def independent_oracle(text: str, form: str) -> dict:
    """Read the text the way a careful person does, without using the answer key."""
    scale = SCALE[re.search(r"\((in thousands|in millions|in dollars)", text).group(1)]
    token = r"(\(?[\d,]+\)?)"
    lines = text.split("\n")

    def row(label: str) -> list[str] | None:
        for line in lines:
            if line.startswith(label):
                return re.findall(token, line[len(label):])
        return None

    if form == "10-Q":  # the three-month 2025 column is first; the balance sheet's Sep 30, 2025 is first
        pick = {"rev": 0, "ni": 0, "ta": 0}
    else:
        header = next(line for line in lines if "Fiscal 2025" in line and "Fiscal 2024" in line)
        pick = dict.fromkeys(("rev", "ni", "ta"), 0 if header.index("Fiscal 2025") < header.index("Fiscal 2024") else 1)
    out = {}
    for name, label, key in (("revenue_usd", "Total revenues", "rev"), ("net_income_usd", "Net income (loss)", "ni"),
                             ("total_assets_usd", "Total assets", "ta")):
        found = row(label)
        out[name] = None if found is None else number(found[pick[key]]) * scale
    return out


@pytest.mark.parametrize("name", sorted(FILINGS))
def test_the_key_equals_an_independent_reading_of_the_text(name: str) -> None:
    assert independent_oracle(FILINGS[name]["text"], FILINGS[name]["form"]) == ANSWERS[name]


def test_known_values() -> None:
    assert ANSWERS["f1"]["revenue_usd"] == 4_218_330_000  # in thousands
    assert ANSWERS["f2"]["revenue_usd"] == 18_452_000_000  # in millions, prior year printed first
    assert ANSWERS["f3"]["net_income_usd"] == -54_307_000  # a loss in parentheses
    assert ANSWERS["f4"]["revenue_usd"] == 2_845_190  # in dollars
    assert ANSWERS["f5"]["total_assets_usd"] is None  # no balance sheet in the excerpt
    assert ANSWERS["f6"]["revenue_usd"] == 1_503_220_000  # the three-month column of a 10-Q


def test_tools() -> None:
    assert len(IMPLEMENTATIONS) == 2
    out = get_filing(FilingInput(filing=Filing.F3), None)
    assert out.form == "10-K" and "(54,307)" in out.text
    assert get_filing(FilingInput(filing=Filing.F6), None).form == "10-Q"
    assert pin_fields(FilingInput(filing=Filing.F5), None).expected.total_assets_usd is None
    assert rules.expected("f1") == ANSWERS["f1"]
