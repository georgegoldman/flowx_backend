
# Flowx_backend (API Token Authentication Service)

## Overview

The API Token Authentication Service provides a method of authenticating users using **hardware fingerprints** tied to **API tokens**. This service is designed to issue and verify tokens that help authenticate devices without requiring a traditional login/logout flow. The key operations are:

1. **Token Generation**: A device is issued a main token (JWT) based on its hardware fingerprint.
2. **Short Token Generation**: A 32-character short token is derived from the main token for lightweight token management.
3. **Token Verification**: The service verifies the short token, ensuring it's valid, not expired, and that the hardware fingerprint matches.

This approach allows secure authentication tied to a specific hardware device, enhancing security by linking the token to the device's unique identifier.

## Key Components

### 1. **Main Token (JWT)**

The **main token** is a JSON Web Token (JWT) that includes the following claims:
- **Hardware Fingerprint**: A unique identifier for the device (e.g., a device's hardware characteristics).
- **Issued At (`iat`)**: The timestamp when the token was issued.
- **Expiration (`exp`)**: The timestamp when the token will expire.

The main token serves as the core authentication credential that is used to verify a device's identity.

### 2. **Short Token**

The **short token** is a 32-character hash derived from the main token. It is used as a more compact and easily manageable token. The short token simplifies database lookups and token comparisons.

### 3. **Token Verification**

When a client presents a short token, the service performs the following:
- It retrieves the **main token** associated with the short token from the database.
- It verifies the **main token's expiration**.
- It ensures the **hardware fingerprint** in the main token matches the device's hardware fingerprint.
- It checks that the **short token** matches the one generated from the main token.

If the verification passes, the client is authenticated. If the token is expired, invalid, or doesn't match the expected fingerprint, an error is returned.

---

## API Endpoints

### 1. Generate Main Token

**Endpoint**: `POST /api/v1/tokens/main`

#### Description:
- Takes the **hardware fingerprint** of the device and generates a **main token (JWT)**.
- Returns the **main token** along with a derived **short token**.

#### Example Flow:
1. A client submits its **hardware fingerprint**.
2. The service generates a **JWT** (main token) and a **32-character short token**.
3. The main token and short token are returned to the client.

### 2. Verify Short Token

**Endpoint**: `GET /api/v1/tokens/verify`

#### Description:
- Takes a **short token** and verifies it against the stored **main token**.
- Checks the **token expiration**, **hardware fingerprint**, and whether the short token matches the generated short token from the main token.

#### Example Flow:
1. The client sends the **short token**.
2. The service retrieves the associated **main token** from the database.
3. The service validates the **main token's expiration** and verifies the **hardware fingerprint**.
4. The service checks if the **short token** matches the expected short token generated from the main token.
5. If valid, the service returns the **hardware fingerprint**. Otherwise, it returns an error (e.g., token expired, invalid, or mismatch).

---

## Security Considerations

1. **Token Expiry**: Tokens have an expiration time, which limits the lifespan of the authentication, ensuring that any potential compromised tokens are automatically invalidated after a certain period.
2. **Device Binding**: Each token is bound to a specific **hardware fingerprint**, making it unique to a particular device and adding an additional layer of security.
3. **Hashing**: The short token is a hashed version of the main token, preventing the exposure of the main token in places where a shorter token would suffice.
4. **Database Storage**: Tokens are stored in the database securely, with the main token being associated with the short token to facilitate easy verification.

---

## Database Schema

### Tokens Collection

The service uses a database to store the tokens. The **tokens collection** typically includes:
- **main_token**: The original JWT token.
- **short_token**: The 32-character hash derived from the main token.
- **hardware_fingerprint**: The unique identifier for the device associated with the token.
- **created_at**: Timestamp of when the token was created.

This collection enables quick retrieval and validation of tokens based on the short token.

---

## Setup Instructions

### Install Dependencies
To run this service, install the necessary Python packages:
```bash
pip install fastapi uvicorn python-jose pymongo
```

### Configuration
Set up environment variables:
- **SECRET_KEY**: A secret key used for JWT signing and validation.
- **ACCESS_TOKEN_EXPIRE_DAY**: Number of days before the JWT expires.
- **ALGORITHM**: The algorithm used for JWT encoding/decoding.
- **MONGO_URI**: Connection string for your MongoDB database.

### Run the Server
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Conclusion

This API Token Authentication Service provides an efficient and secure method to authenticate devices using hardware fingerprints. It eliminates the need for traditional login credentials while still ensuring that the authentication process is robust and tied to the physical device.