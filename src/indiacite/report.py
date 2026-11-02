from indiacite.cascade import Report

DISCLAIMER = (
    "A flag means a human should check. needs_review means no stage could decide. "
    "pass is not a certificate that a citation is correct."
)


def render_markdown(reports: list[Report], title: str = "Citation check report") -> str:
    lines = [
        f"# {title}",
        "",
        DISCLAIMER,
        "",
        "| status | citation | case name | decided by | type | reason |",
        "|---|---|---|---|---|---|",
    ]
    for r in reports:
        lines.append(
            f"| {r.outcome} | {r.citation.raw} | {r.case_name or '-'} | {r.decided_by or '-'} | "
            f"{r.error_type or '-'} | {r.reason} |"
        )
    flagged = sum(1 for r in reports if r.outcome == "flag")
    review = sum(1 for r in reports if r.outcome == "needs_review")
    lines += ["", f"citations {len(reports)}, flagged {flagged}, needs review {review}", ""]
    return "\n".join(lines)
