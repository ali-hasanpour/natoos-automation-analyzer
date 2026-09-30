# Remediation

The main issue was caused by missing authorization checks on placement receipt requests.

Before the fix, a valid report token could be used with a different `PlacementId`, allowing another user's receipt to be returned.

## Changes

The most important fix was to validate the requested receipt against the authenticated user's session.

A user should only be able to access receipts that belong to their own account.

Other important security improvements include:

- Perform object-level authorization checks on every receipt request
- Do not rely on a report token alone as proof of authorization
- Do not use national codes as default passwords
- Require users to create separate passwords
- Reduce the amount of personal information returned by API responses
- Add rate limiting to sensitive endpoints
- Monitor repeated or sequential access to receipt IDs
- Log failed authorization attempts

## Fixed Behavior

After remediation, requesting a receipt that does not belong to the authenticated user is rejected.

This prevents the original IDOR from being used to access another user's receipt.