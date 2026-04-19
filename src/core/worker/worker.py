from dataclasses import dataclass


@dataclass
class CheckResult:
    is_upd: bool
    latency: float | None
    error_message: str | None
