import pytest
from slimconfig import build_output, plain_output

import verifier
from contract import TASKS, TOOLS, FieldsOutput, Filing, FilingInput, Task, Tool
from plugin.tools import get_filing, pin_fields


# The verifier gets contract instances, as NanoAgent's sandbox builds them from JSON.
def verify_task(arguments: dict, output: dict, reference) -> dict:
    given, made = TASKS[Task.EXTRACT_FIELDS]
    return verifier.verify_task("extract-fields", build_output(arguments, given), build_output(output, made), reference, "ws")


def pinned(filing: str):
    return pin_fields(FilingInput(filing=Filing(filing)), None)


def perfect(filing: str) -> dict:
    return plain_output(pinned(filing).expected)


def failed(verdict: dict) -> set:
    return {c["name"] for c in verdict["details"]["checks"] if not c["ok"]}


@pytest.mark.parametrize("filing", ["f1", "f2", "f3", "f4", "f5", "f6"])
def test_the_answer_key_passes(filing: str) -> None:
    verdict = verify_task({"filing": filing}, perfect(filing), pinned(filing))
    assert verdict["valid"] is True and verdict["score"] == 1.0


def test_forgetting_the_unit_is_caught() -> None:
    out = perfect("f1") | {"revenue_usd": 4_218_330}  # still "in thousands"
    verdict = verify_task({"filing": "f1"}, out, pinned("f1"))
    assert failed(verdict) == {"revenue_usd"} and "4218330000" in verdict["message"]


def test_thousands_for_millions_is_caught() -> None:
    out = perfect("f2") | {"total_assets_usd": 41_330_000}
    assert failed(verify_task({"filing": "f2"}, out, pinned("f2"))) == {"total_assets_usd"}


def test_the_prior_year_column_is_caught() -> None:
    out = perfect("f2") | {"revenue_usd": 16_470_000_000}
    assert failed(verify_task({"filing": "f2"}, out, pinned("f2"))) == {"revenue_usd"}


def test_a_dropped_loss_sign_is_caught() -> None:
    out = perfect("f3") | {"net_income_usd": 54_307_000}
    assert failed(verify_task({"filing": "f3"}, out, pinned("f3"))) == {"net_income_usd"}


def test_the_nine_month_column_of_a_10q_is_caught() -> None:
    out = perfect("f6") | {"revenue_usd": 4_509_667_000}
    assert failed(verify_task({"filing": "f6"}, out, pinned("f6"))) == {"revenue_usd"}


def test_a_missing_value_must_be_null_not_zero_or_a_guess() -> None:
    assert perfect("f5")["total_assets_usd"] is None
    assert failed(verify_task({"filing": "f5"}, perfect("f5") | {"total_assets_usd": 0}, pinned("f5"))) == {"total_assets_usd"}
    guess = perfect("f5") | {"total_assets_usd": 12_000_000_000}
    assert failed(verify_task({"filing": "f5"}, guess, pinned("f5"))) == {"total_assets_usd"}


def test_null_for_a_value_that_is_there_fails() -> None:
    out = perfect("f4") | {"revenue_usd": None}
    verdict = verify_task({"filing": "f4"}, out, pinned("f4"))
    assert failed(verdict) == {"revenue_usd"} and "does contain" in verdict["message"]


def test_a_report_for_another_filing_fails() -> None:
    assert "filing" in failed(verify_task({"filing": "f1"}, perfect("f2"), pinned("f1")))


def test_partial_credit_is_reported_but_it_is_not_a_pass() -> None:
    verdict = verify_task({"filing": "f1"}, perfect("f1") | {"revenue_usd": 1}, pinned("f1"))
    assert verdict["valid"] is False and 0.5 < verdict["score"] < 1.0


@pytest.mark.parametrize(
    "bad",
    [
        {"revenue_usd": "4,218,330,000"},  # a string
        {"revenue_usd": 4_218_330_000.5},  # a float
        {"net_income_usd": True},  # a bool
        {"filing": "f9"},
    ],
)
def test_malformed_outputs_cannot_even_be_built(bad: dict) -> None:
    with pytest.raises(Exception):  # noqa: B017 - the sandbox refuses a value of the wrong type
        build_output(perfect("f1") | bad, FieldsOutput)


def test_a_missing_field_cannot_be_built() -> None:
    out = perfect("f1")
    del out["net_income_usd"]
    with pytest.raises(Exception):  # noqa: B017
        build_output(out, FieldsOutput)


def test_tool_checks() -> None:
    given = FilingInput(filing=Filing.F1)
    assert verifier.verify_input("get_filing", given)["valid"] is True
    assert verifier.verify_output("get_filing", given, get_filing(given, None), "ws")["valid"] is True
    other = get_filing(FilingInput(filing=Filing.F2), None)
    assert verifier.verify_output("get_filing", given, other, "ws")["valid"] is False
    assert verifier.verify_output("pin_fields", given, pinned("f1"), "ws")["valid"] is True
    assert verifier.verify_output("pin_fields", given, pinned("f2"), "ws")["valid"] is False
    assert set(TOOLS) == set(verifier.tools.INPUT_CHECKS) == set(verifier.tools.OUTPUT_CHECKS) == {Tool.GET_FILING, Tool.PIN_FIELDS}
