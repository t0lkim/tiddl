from typing import Optional
from pydantic import BaseModel


class AuthResponse(BaseModel):
    class User(BaseModel):
        """Tidal's user payload.

        Only `userId` and `countryCode` are consumed by tiddl, so every other
        field defaults to None. Tidal removes and adds keys here without
        notice - `facebookUid` disappeared once already - and a hard-required
        field turns that into a login crash.
        """

        userId: int
        countryCode: str
        email: Optional[str] = None
        fullName: Optional[str] = None
        firstName: Optional[str] = None
        lastName: Optional[str] = None
        nickname: Optional[str] = None
        username: Optional[str] = None
        address: Optional[str] = None
        city: Optional[str] = None
        postalcode: Optional[str] = None
        usState: Optional[str] = None
        phoneNumber: Optional[str] = None
        birthday: Optional[int | str] = None
        channelId: Optional[int] = None
        parentId: Optional[int] = None
        acceptedEULA: Optional[bool] = None
        created: Optional[int | str] = None
        updated: Optional[int | str] = None
        facebookUid: Optional[int] = None
        appleUid: Optional[str] = None
        googleUid: Optional[str] = None
        accountLinkCreated: Optional[bool] = None
        emailVerified: Optional[bool] = None
        newUser: Optional[bool] = None

    user: User
    token_type: str
    access_token: str
    expires_in: int
    user_id: int
    scope: Optional[str] = None
    clientName: Optional[str] = None


class AuthResponseWithRefresh(AuthResponse):
    refresh_token: str


class AuthDeviceResponse(BaseModel):
    deviceCode: str
    userCode: str
    verificationUri: str
    verificationUriComplete: str
    expiresIn: int
    interval: int
