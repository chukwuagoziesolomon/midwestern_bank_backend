# Admin Balance Increase Feature

## Overview
Admins can now increase an account's total balance and available balance from the admin dashboard.

## API Endpoint

### Increase Account Balance

**Endpoint:** `POST /api/admin/users/<user_id>/increase-balance/`

**Description:** Increases both the total balance and available balance for a specific user account.

### Request Body

```json
{
  "amount": 5000.00
}
```

**Parameters:**
- `amount` (required, decimal): The amount to add to the account. Must be greater than 0.

### Response

**Success Response (200 OK):**

```json
{
  "message": "Successfully increased balance for user@example.com",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "increase_amount": "5000.00",
    "old_total_balance": "70000.00",
    "new_total_balance": "75000.00",
    "old_available_balance": "70000.00",
    "new_available_balance": "75000.00"
  }
}
```

**Error Responses:**

- **400 Bad Request** - Amount is missing or invalid:
```json
{
  "error": "Amount is required"
}
```
or
```json
{
  "error": "Amount must be greater than 0"
}
```
or
```json
{
  "error": "Invalid amount format"
}
```

- **404 Not Found** - User or account doesn't exist:
```json
{
  "error": "User not found"
}
```
or
```json
{
  "error": "Account not found"
}
```

- **500 Internal Server Error**:
```json
{
  "error": "Error message"
}
```

## Usage Examples

### Example 1: Increase Balance by $5,000

**Request:**
```bash
curl -X POST http://localhost:8000/api/admin/users/1/increase-balance/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.00
  }'
```

**Response:**
```json
{
  "message": "Successfully increased balance for john@example.com",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "increase_amount": "5000.00",
    "old_total_balance": "70000.00",
    "new_total_balance": "75000.00",
    "old_available_balance": "70000.00",
    "new_available_balance": "75000.00"
  }
}
```

### Example 2: Using JavaScript/React

```javascript
const increaseBalance = async (userId, amount) => {
  try {
    const response = await fetch(`/api/admin/users/${userId}/increase-balance/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: amount
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      console.log('Balance increased successfully:', data);
      return data;
    } else {
      console.error('Error:', data.error);
      throw new Error(data.error);
    }
  } catch (error) {
    console.error('Failed to increase balance:', error);
    throw error;
  }
};

// Usage
increaseBalance(1, 5000.00)
  .then(result => {
    console.log('New balance:', result.user.new_total_balance);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

## User-Facing Balance Display

When an admin increases a user's balance, the change is **immediately reflected** in the user's dashboard. Users can see their updated balance by calling the dashboard endpoint:

**User Dashboard Endpoint:** `GET /api/dashboard/?user_id=<user_id>`

**Response:**
```json
{
  "total_balance": "75000.00",
  "available_balance": "75000.00",
  "loans_due": "0.00",
  "mortgage_due": "0.00"
}
```

The `DashboardView` endpoint uses the `AccountSerializer` which reads directly from the database, ensuring users always see their current balance including any admin adjustments.

## Implementation Details

### Backend Changes

1. **New View Class:** `AdminIncreaseBalanceView` in `bankapp/views.py`
   - Validates the amount input
   - Ensures amount is positive
   - Increases both `total_balance` and `available_balance`
   - Returns detailed information about the change

2. **URL Route:** Added in `bankapp/urls.py`
   - Pattern: `admin/users/<int:user_id>/increase-balance/`
   - Name: `admin-increase-balance`

3. **Imports:** Added `Decimal` and `InvalidOperation` from Python's decimal module

4. **Existing Endpoints (No Changes Required):**
   - `DashboardView` automatically displays updated balances
   - `AccountSerializer` includes `total_balance` and `available_balance` fields

### Key Features

- **Atomic Operation:** Both balances are updated in a single transaction
- **Validation:** Ensures amount is numeric and positive
- **Error Handling:** Comprehensive error messages for all failure cases
- **Audit Trail:** Returns old and new balances for record keeping
- **Type Safety:** Uses Decimal type for precise financial calculations

## Frontend Integration Suggestions

### Admin Dashboard Button

Add a button in the user detail view:

```jsx
const [increaseAmount, setIncreaseAmount] = useState('');
const [loading, setLoading] = useState(false);

const handleIncreaseBalance = async () => {
  if (!increaseAmount || parseFloat(increaseAmount) <= 0) {
    alert('Please enter a valid amount');
    return;
  }
  
  setLoading(true);
  try {
    const response = await fetch(`/api/admin/users/${userId}/increase-balance/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: parseFloat(increaseAmount) })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert(`Balance increased by $${data.user.increase_amount}`);
      // Refresh user data
      fetchUserDetails();
      setIncreaseAmount('');
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (error) {
    alert('Failed to increase balance');
  } finally {
    setLoading(false);
  }
};

return (
  <div className="balance-increase-section">
    <h3>Increase Balance</h3>
    <input
      type="number"
      placeholder="Enter amount"
      value={increaseAmount}
      onChange={(e) => setIncreaseAmount(e.target.value)}
      min="0"
      step="0.01"
    />
    <button 
      onClick={handleIncreaseBalance}
      disabled={loading}
    >
      {loading ? 'Processing...' : 'Increase Balance'}
    </button>
  </div>
);
```

## Security Considerations

1. **Admin Authentication:** Ensure this endpoint is protected and only accessible to admin users
2. **Authorization:** Add permission checks before allowing balance increases
3. **Audit Logging:** Consider logging all balance increase operations for compliance
4. **Rate Limiting:** Implement rate limiting to prevent abuse

## Testing

Test the endpoint with various scenarios:

1. Valid increase amount
2. Negative amount (should fail)
3. Zero amount (should fail)
4. Non-numeric amount (should fail)
5. Non-existent user ID (should fail)
6. Very large amounts (test decimal precision)

## Future Enhancements

- Add option to decrease balance
- Add reason/notes field for audit purposes
- Send email notification to user when balance is increased
- Add transaction history entry for balance adjustments
- Implement two-factor authentication for balance changes
- Add daily/monthly limits for balance increases
