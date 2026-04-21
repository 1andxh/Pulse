from fastapi import status


class DomainError(Exception):
    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class DuplicateMonitorError(DomainError):
    def __init__(self) -> None:
        super().__init__("Monitor already exists", status_code=status.HTTP_409_CONFLICT)


class MonitorNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("Monitor not found", status_code=status.HTTP_404_NOT_FOUND)
