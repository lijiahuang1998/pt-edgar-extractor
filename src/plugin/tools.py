"""The two tools: get_filing (what the agent sees) and pin_fields (the answer key, out of its sight)."""

from pathlib import Path

from contract import FieldsOutput, FilingInput, FilingOutput, PinOutput
from plugin import rules
from plugin.data import FILINGS


def get_filing(given: FilingInput, workspace: Path) -> FilingOutput:
    filing = FILINGS[given.filing.value]
    return FilingOutput(filing=given.filing, form=filing["form"], text=filing["text"])


def pin_fields(given: FilingInput, workspace: Path) -> PinOutput:
    return PinOutput(filing=given.filing, expected=FieldsOutput(filing=given.filing, **rules.expected(given.filing.value)))
