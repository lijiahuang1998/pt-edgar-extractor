"""The extract-fields verdict: each reported number must equal the answer key exactly (or both be null)."""

from .checks import finish


def verify_task(arguments, output, reference, workspace):
    expected = reference.expected
    pairs = (
        ("revenue_usd", output.revenue_usd, expected.revenue_usd),
        ("net_income_usd", output.net_income_usd, expected.net_income_usd),
        ("total_assets_usd", output.total_assets_usd, expected.total_assets_usd),
    )
    checks = [("filing", output.filing == arguments.filing, f"report is for {output.filing.value}, task is {arguments.filing.value}")]
    for name, got, want in pairs:
        if want is None:
            checks.append((name, got is None, f"the filing has no such value: expected null, got {got!r}"))
        elif got is None:
            checks.append((name, False, f"expected {want}, got null: the filing does contain it"))
        else:
            checks.append((name, got == want, f"expected {want}, got {got}"))
    return finish(checks, f"all three fields of filing {arguments.filing.value} are right")
