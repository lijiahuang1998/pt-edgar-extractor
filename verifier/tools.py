"""Per-tool checks: what a tool's input and output must mean, beyond their types."""

from contract import Tool

from .checks import result


def get_filing_input(value):
    return result(True, "get_filing reads one of the six filings")


def get_filing_output(input_value, output_value, workspace):
    if output_value.filing != input_value.filing:
        return result(False, "get_filing returned another filing than the one asked for")
    if output_value.form not in ("10-K", "10-Q") or not output_value.text.strip():
        return result(False, "a filing needs a form (10-K or 10-Q) and non-blank text")
    return result(True, "get_filing returned the filing's text")


def pin_fields_input(value):
    return result(True, "pin_fields pins one of the six filings")


def pin_fields_output(input_value, output_value, workspace):
    if output_value.filing != input_value.filing or output_value.expected.filing != input_value.filing:
        return result(False, "the pinned answer is for another filing")
    return result(True, "the answer key is pinned")


INPUT_CHECKS = {Tool.GET_FILING: get_filing_input, Tool.PIN_FIELDS: pin_fields_input}
OUTPUT_CHECKS = {Tool.GET_FILING: get_filing_output, Tool.PIN_FIELDS: pin_fields_output}
