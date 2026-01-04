# Bank App API Documentation

This document describes the API endpoints for the Bank App backend.

Base URL: `http://localhost:8000/`

## Authentication
- The app uses email and password for login.
- Some endpoints require `user_id` in query params or request body.

## Endpoints

### 1. Sign Up
**Endpoint:** `POST /signup/`

**Description:** Creates a new user account. Open to all users.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "any_password"
}
```

**Response (Success):**
```json
{
  "message": "User created successfully",
  "password": "generated_fake_password"
}
```

**Notes:** Generates a fake password and card details for all users.

### 2. Login
**Endpoint:** `POST /login/`

**Description:** Authenticates a user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**Response (Success):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "William",
    "last_name": "Cruz"
  }
}
```

**Response (Error):**
```json
{
  "error": "Invalid password"
}
```

### 3. Transfers
**Endpoint:** `GET /transfers/?user_id=<id>` and `POST /transfers/`

**Description:** Get transaction history or create a new transfer.

**GET Request:**
- Query Param: `user_id` (required)

**GET Response:**
```json
[
  {
    "id": 1,
    "transfer_type": "local",
    "receiver_name": "John Doe",
    "receiver_bank": "Local Bank",
    "receiver_account_number": "1234567890",
    "routing_number": "123456789",
    "amount": "500.00",
    "description": "Payment",
    "date": "2023-01-01T00:00:00Z",
    "status": "completed"
  }
]
```

**POST Request Body:**
```json
{
  "user_id": 1,
  "transfer_type": "local",
  "receiver_name": "John Doe",
  "receiver_bank": "Bank",
  "receiver_account_number": "1234567890",
  "routing_number": "123456789",  // Required for local
  "amount": 500.00,
  "description": "Payment",
  "pin": "2027"  // Must be 2027
}
```
For international:
```json
{
  "user_id": 1,
  "transfer_type": "international",
  "receiver_name": "Jane Smith",
  "receiver_bank": "International Bank",
  "receiver_bank_address": "Address",
  "receiver_account_number": "0987654321",
  "iban": "GB29...",
  "swift_code": "ABCD",
  "amount": 1000.00,
  "description": "Payment",
  "pin": "2027"
}
```

**POST Response (Success):**
```json
{
  "message": "Transfer created successfully",
  "transfer": { ... }
}
```

**Notes:** Deducts from available balance. PIN must be '2027'. Users can make a maximum of 2 transfers until reset manually.

### 4. Credit Card Deposit
**Endpoint:** `POST /deposit/`

**Description:** Deposits money using credit card. Works with the user's generated card details.

**Request Body:**
```json
{
  "user_id": 1,
  "card_number": "user's_generated_card_number",
  "card_expiry": "user's_generated_expiry",
  "card_cvc": "user's_generated_cvc",
  "deposit_amount": 1000.00,
  "card_holder_name": "User's Full Name"
}
```

**Response (Success):**
```json
{
  "message": "Deposit successful",
  "deposit": { ... }
}
```

**Notes:** Card details must match those generated during sign-up. Adds to balance.

### 5. User Settings
**Endpoint:** `GET /settings/?user_id=<id>` and `POST /settings/`

**Description:** Get user info or change password.

**GET Response:**
```json
{
  "id": 1,
  "first_name": "William",
  "last_name": "Cruz",
  "email": "williamcruz.stl@outlook.com"
}
```

**POST Request Body:**
```json
{
  "user_id": 1,
  "current_password": "old_password",
  "new_password": "new_password",
  "confirm_password": "new_password"
}
```

**POST Response (Success):**
```json
{
  "message": "Password changed successfully"
}
```

### 6. Dashboard
**Endpoint:** `GET /dashboard/?user_id=<id>`

**Description:** Get account statistics for dashboard stat cards.

**Response:**
```json
{
  "total_balance": "69500.00",
  "available_balance": "69500.00",
  "loans_due": "0.00",
  "mortgage_due": "0.00"
}
```

### 7. Card Details
**Endpoint:** `GET /card/?user_id=<id>`

**Description:** Get generated card details for deposit (only for William Cruz).

**Response:**
```json
{
  "card_holder_name": "User's Full Name",
  "card_number": "1234567890123456",
  "card_expiry": "12/28",
  "card_cvc": "123"
}
```

## Models

- **User:** Django's auth User with first_name, last_name, email.
- **Account:** total_balance, available_balance, generated card details.
- **Transfer:** Transfer details, status.
- **CreditCardDeposit:** Deposit details.

## Running the Server
```bash
python manage.py runserver
```

## CORS
CORS is configured to allow requests from:
- http://localhost:3000
- https://your-vercel-app.vercel.app (replace with actual)
- https://your-live-website.com (replace with actual)

## Notes
- All monetary values are in USD.
- Default balance: $70,000.
- PIN for transfers: '2027'.
- Card holder for deposits: "William Cruz".