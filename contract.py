"""Each tool's and task's typed input and output (see nanoagent.plugin.contract): declarations only."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    GET_FILING = "get_filing"
    PIN_FIELDS = "pin_fields"


class Task(Enum):
    EXTRACT_FIELDS = "extract-fields"


class Filing(Enum):
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"


FILING = "Which synthetic filing excerpt: f1 to f6"


@dataclass
class FilingInput(Output):
    filing: Annotated[Filing, FILING]


@dataclass
class FilingOutput(Output):
    filing: Annotated[Filing, "The filing that was read"]
    form: Annotated[str, "10-K or 10-Q"]
    text: Annotated[str, "The filing excerpt, as plain text"]


@dataclass
class FieldsOutput(Output):
    filing: Annotated[Filing, "The filing this report is for, copied from the task"]
    revenue_usd: Annotated[int | None, "Total revenues. Full US dollars as an integer (units already multiplied out); negative for a loss; null when the filing does not contain it"]
    net_income_usd: Annotated[int | None, "Net income (loss). Full US dollars as an integer (units already multiplied out); negative for a loss; null when the filing does not contain it"]
    total_assets_usd: Annotated[int | None, "Total assets at the period end. Full US dollars as an integer (units already multiplied out); negative for a loss; null when the filing does not contain it"]


@dataclass
class PinOutput(Output):
    filing: Annotated[Filing, "The filing pinned"]
    expected: Annotated[FieldsOutput, "The answer key for the filing"]


TOOLS = {
    Tool.GET_FILING: (FilingInput, FilingOutput),
    Tool.PIN_FIELDS: (FilingInput, PinOutput),
}
TASKS = {
    Task.EXTRACT_FIELDS: (FilingInput, FieldsOutput),
}
