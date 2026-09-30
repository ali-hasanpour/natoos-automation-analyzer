# Security

This repository is a write-up of a security issue I found in the Natoos platform.

The testing was done with permission from the owner, and I also had permission to publish the project after the issue was fixed.

## Status

The issue described in this repository has already been fixed.

Before the fix, it was possible to access another user's placement receipt by changing the receipt ID.

The receipt contained the user's national code, and because the national code was also being used as both the username and password, it could be used to log in and retrieve more account information.

After the fix, receipt access is checked against the logged-in user's session. If the receipt does not belong to that user, the request is rejected.

## Privacy

I removed or redacted personal information from the public version of this project.

This includes:

- Names
- National codes
- Phone numbers
- Addresses
- Emails
- Authentication tokens
- Internal user identifiers

The original data is not included in this repository.

## Authorization

All testing shown in this repository was authorized.

This project is only being shared as a security research write-up and for educational purposes.

Do not test these methods on systems you do not own or have permission to test.