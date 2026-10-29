# Changelog

All notable changes to this fork are documented here. This fork tracks
[oskvr37/tiddl](https://github.com/oskvr37/tiddl) and carries fixes that have
not landed upstream.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is [semver](https://semver.org/spec/v2.0.0.html), with the fork
suffix `+fork.N` on top of the upstream release it is based on.

## [3.4.4+fork.1] - 2026-10-29

Forked from upstream `v3.4.4` (`f5c8e96`). All changes are in the device
authentication path, which had three independent ways to fail.

### Fixed

- **`auth login` no longer crashes when Tidal omits a user field.** Every field
  in the token response's user object was hard-required, so Tidal dropping one
  raised a pydantic `ValidationError` and killed the login. Only `userId` and
  `countryCode` are read by tiddl, so the rest now default to `None`. The
  removal of `facebookUid` broke login on every release that still required it.
- **`auth login` no longer hangs in silence on an unrecognised error.** The poll
  loop handled only `authorization_pending` and `expired_token`; anything else
  fell through the `except` and span the loop with no output until the user gave
  up. Unknown errors, and `access_denied`, now report and exit (upstream #438).
- **`slow_down` is honoured.** Per RFC 8628 the poll interval now grows by 5s
  each time Tidal asks us to slow down, instead of being ignored and polling at
  a rate the server keeps rejecting.
- **The poll loop is bounded by the device code's own expiry.** It previously
  relied on the server reporting `expired_token`, and would otherwise poll a
  dead device code indefinitely.
- **A malformed auth error body raises an auth error.** `AuthClientError(**body)`
  raised `TypeError` on an unexpected key, and a non-JSON body raised a bare
  `JSONDecodeError`; both escaped the loop as unhandled crashes.

### Changed

- **A failed `auth login` now exits non-zero.** Expiry, denial and unknown
  errors exit `1`; previously expiry exited `0`, which left no way for a wrapper
  to tell a failed login from a successful one. Successful login still exits `0`.

### Added

- Tests covering the auth payload shape, `slow_down` backoff, denial, unknown
  errors and the error-body tolerance (113 tests, up from 104).

### Note on installation

Upstream requires Python >= 3.13 from `3.0.0` onwards. A `uv tool install` made
against an older interpreter silently resolves to `2.8.0` and stays there
through every `uv tool upgrade`, because that is the newest release compatible
with the environment. Install with an explicit interpreter:

```bash
uv tool install -p 3.13 --force tiddl
```
