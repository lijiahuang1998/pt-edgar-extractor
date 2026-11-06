"""edgar-extractor: the tools and the table that maps each contract.Tool to its implementation."""

from contract import Tool
from plugin.tools import get_filing, pin_fields

# Each tool's implementation: (its input, the workspace) -> its output, as contract.TOOLS types them.
IMPLEMENTATIONS = {
    Tool.GET_FILING: get_filing,
    Tool.PIN_FIELDS: pin_fields,
}

__all__ = ["IMPLEMENTATIONS", "get_filing", "pin_fields"]
