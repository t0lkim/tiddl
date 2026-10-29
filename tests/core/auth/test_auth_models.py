"""Regression tests for the auth payload models.

Tidal changes the shape of the user object in its token response without
notice. These tests pin the rule that only the fields tiddl actually consumes
are required, so a removed or added key cannot break login.
"""

from tiddl.core.auth.models import AuthResponse, AuthResponseWithRefresh


BASE = {
    "token_type": "Bearer",
    "access_token": "access",
    "expires_in": 86400,
    "user_id": 42,
}

USER = {"userId": 42, "countryCode": "SG"}


def test_user_without_facebook_uid():
    """Tidal dropped `facebookUid`, which crashed login with a ValidationError."""

    auth = AuthResponse.model_validate({**BASE, "user": USER})

    assert auth.user.facebookUid is None
    assert auth.user.countryCode == "SG"
    assert auth.user_id == 42


def test_user_ignores_unknown_fields():
    """A key Tidal adds later must not be treated as an error."""

    auth = AuthResponse.model_validate(
        {**BASE, "user": {**USER, "someFutureField": "surprise"}}
    )

    assert auth.user.userId == 42


def test_optional_top_level_fields_absent():
    """`scope` and `clientName` are not consumed, so they may be missing."""

    auth = AuthResponse.model_validate({**BASE, "user": USER})

    assert auth.scope is None
    assert auth.clientName is None


def test_full_payload_still_parses():
    """A complete payload must keep populating every field."""

    auth = AuthResponseWithRefresh.model_validate(
        {
            **BASE,
            "refresh_token": "refresh",
            "scope": "r_usr w_usr",
            "clientName": "tiddl",
            "user": {
                **USER,
                "email": "music@example.com",
                "username": "listener",
                "facebookUid": 7,
                "appleUid": "apple",
                "googleUid": "google",
                "acceptedEULA": True,
                "emailVerified": True,
                "newUser": False,
                "created": 1700000000,
                "updated": 1700000001,
                "channelId": 1,
                "parentId": 0,
                "accountLinkCreated": False,
                "birthday": 1234567890,
            },
        }
    )

    assert auth.refresh_token == "refresh"
    assert auth.user.facebookUid == 7
    assert auth.user.email == "music@example.com"
    assert auth.user.acceptedEULA is True
