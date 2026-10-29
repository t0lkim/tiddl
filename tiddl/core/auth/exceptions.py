from typing import Any


class AuthClientError(Exception):
    """Error body returned by Tidal's OAuth endpoints.

    Unknown keys are kept rather than rejected: Tidal adds fields to these
    bodies, and a TypeError here used to escape the login poll loop as an
    unhandled crash instead of a readable auth error.
    """

    def __init__(
        self,
        status: int | None = None,
        error: str | None = None,
        sub_status: str | None = None,
        error_description: str | None = None,
        **extra: Any,
    ):
        self.status = status
        self.error = error
        self.sub_status = sub_status
        self.error_description = error_description
        self.extra = extra

        super().__init__(str(self))

    def __str__(self):
        return (
            f"{self.error}, {self.error_description}, {self.status}/{self.sub_status}"
        )
