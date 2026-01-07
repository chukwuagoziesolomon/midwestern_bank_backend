# 📅 Custom Transaction Date Ranges Guide

## Overview

The admin can now specify custom date ranges when approving users. Instead of transactions always being generated from Dec 1, 2023 to today, the admin dashboard will prompt for start and end dates.

---

## Backend Changes

### 1. Updated DummyTransactionGenerator

**File:** `bankapp/transaction_generator.py`

Both methods now accept optional date parameters:

```python
@staticmethod
def generate_transactions_for_user(
    user, 
    num_transactions=15, 
    start_date=None,      # NEW: Optional YYYY-MM-DD string or datetime
    end_date=None         # NEW: Optional YYYY-MM-DD string or datetime
):
    # Generates 15 realistic transfers within the date range
    # Defaults: Dec 1, 2023 to today if dates not provided

@staticmethod
def generate_deposit_history_for_user(
    user, 
    num_deposits=5, 
    start_date=None,      # NEW: Optional YYYY-MM-DD string or datetime
    end_date=None         # NEW: Optional YYYY-MM-DD string or datetime
):
    # Generates 5 realistic deposits within the date range
    # Defaults: Dec 1, 2023 to today if dates not provided
```

**Date Format:** `YYYY-MM-DD` (e.g., "2024-06-15")

### 2. Updated AdminApproveUserView

**File:** `bankapp/views.py` - `AdminApproveUserView` class

Now accepts custom dates in the request body:

```python
POST /api/admin/users/{id}/approve/

Request Body:
{
    "action": "approve",
    "start_date": "2024-01-01",    # Optional - defaults to 2023-12-01
    "end_date": "2025-12-31"       # Optional - defaults to today
}
```

---

## API Usage Examples

### Example 1: Approve with Default Dates (Dec 1, 2023 - Today)

```bash
curl -X POST http://localhost:8000/api/admin/users/5/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```

**Response:**
```json
{
  "message": "User john@bank.com has been approved and can now login. Transaction history generated.",
  "user": {
    "id": 5,
    "email": "john@bank.com",
    "is_approved": true,
    "initial_balance": "70000",
    "transactions_generated": 15,
    "start_date": "2023-12-01",
    "end_date": "Today"
  }
}
```

### Example 2: Approve with Custom Dates (1 Year Ago - Today)

```bash
curl -X POST http://localhost:8000/api/admin/users/5/approve/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve",
    "start_date": "2025-01-07",
    "end_date": "2026-01-07"
  }'
```

**Response:**
```json
{
  "message": "User john@bank.com has been approved and can now login. Transaction history generated (Transactions from 2025-01-07 to 2026-01-07).",
  "user": {
    "id": 5,
    "email": "john@bank.com",
    "is_approved": true,
    "initial_balance": "70000",
    "transactions_generated": 15,
    "start_date": "2025-01-07",
    "end_date": "2026-01-07"
  }
}
```

### Example 3: Approve with Just Start Date (to Today)

```bash
curl -X POST http://localhost:8000/api/admin/users/5/approve/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve",
    "start_date": "2023-06-01"
  }'
```

---

## React Integration

### Simple Version: Using Prompts

The `approveUser` function has been updated to prompt for dates:

```javascript
const approveUser = async (userId, userName) => {
  // Prompt for start date
  const startDate = prompt(
    'Enter start date for transaction history (YYYY-MM-DD):\n\nExample: 2024-01-01\nLeave blank for Dec 1, 2023',
    '2023-12-01'
  );
  
  if (startDate === null) return; // User cancelled
  
  // Prompt for end date
  const endDate = prompt(
    'Enter end date for transaction history (YYYY-MM-DD):\n\nExample: 2025-12-31\nLeave blank for today',
    new Date().toISOString().split('T')[0]
  );
  
  if (endDate === null) return; // User cancelled
  
  try {
    const payload = { action: 'approve' };
    if (startDate.trim()) payload.start_date = startDate;
    if (endDate.trim()) payload.end_date = endDate;
    
    const response = await axios.post(
      `${API_BASE}/admin/users/${userId}/approve/`,
      payload
    );
    
    alert(
      `✅ ${userName} Approved!\n\n` +
      `🎉 15 transactions generated\n` +
      `💰 Initial Balance: $${response.data.user.initial_balance}\n` +
      `📅 Transactions from ${response.data.user.start_date} to ${response.data.user.end_date}`
    );
    
    fetchUsers();
  } catch (error) {
    alert(`❌ Error: ${error.response?.data?.error || error.message}`);
  }
};
```

### Advanced Version: Modal Dialog (Optional)

For a better UX, create a `DateRangeModal.jsx` component with date input fields and validation.

**Features:**
- Professional modal UI with gradient design
- Date input fields with validation
- Prevents invalid date ranges (start > end)
- Matches Midwestern Bank color scheme (white/blue)

See [REACT_ADMIN_COMPONENTS.md](REACT_ADMIN_COMPONENTS.md) section 7 for full implementation.

---

## Testing Workflow

### Step 1: Start Django
```bash
python manage.py runserver
```

### Step 2: Create Admin Account
```bash
python manage.py create_admin --email admin@bank.com --password admin123
```

### Step 3: Create Test User (via API)
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@bank.com",
    "password": "temp123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Step 4: Approve User with Custom Dates

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/admin/users/2/approve/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve",
    "start_date": "2024-06-01",
    "end_date": "2025-12-31"
  }'
```

**Using React Admin Dashboard:**
1. Go to admin dashboard
2. Click "Approve" button on test user
3. Enter start date: `2024-06-01`
4. Enter end date: `2025-12-31`
5. Confirm approval
6. View generated transactions for that date range

### Step 5: Verify Transactions

```bash
# Get user's transfers
curl http://localhost:8000/api/transfers/?user_id=2

# Get user's account details
curl http://localhost:8000/api/user-account/?user_id=2
```

---

## Key Features

✅ **Flexible Date Ranges** - Admin can choose any start and end date
✅ **Realistic Transactions** - 15 transfers + 5 deposits randomly distributed in date range
✅ **Backward Compatible** - If dates not provided, uses defaults (Dec 2023 - Today)
✅ **Date Validation** - Backend validates that start_date < end_date
✅ **String or Datetime** - Accepts both YYYY-MM-DD strings and datetime objects
✅ **Automatic Timestamps** - Transactions get realistic times within the date range
✅ **$70K Initial Balance** - Still applied to all approved users
✅ **API Transparency** - Response shows which dates were used for generation

---

## Common Use Cases

### Case 1: New Employee (6-Month History)
```json
{
  "action": "approve",
  "start_date": "2025-07-07",  // 6 months ago
  "end_date": "2026-01-07"      // Today
}
```

### Case 2: Historical Backfill (Full 2-Year History)
```json
{
  "action": "approve",
  "start_date": "2024-01-01",
  "end_date": "2026-01-07"
}
```

### Case 3: Recent Account (3 Months)
```json
{
  "action": "approve",
  "start_date": "2025-10-07",  // 3 months ago
  "end_date": "2026-01-07"     // Today
}
```

### Case 4: Just Recent Activity (Last Month)
```json
{
  "action": "approve",
  "start_date": "2025-12-07",  // 1 month ago
  "end_date": "2026-01-07"     // Today
}
```

---

## Error Handling

### Invalid Date Format
**Error:** Request with invalid date format (not YYYY-MM-DD)
**Response:** 400 Bad Request with error details

### Start Date After End Date
**Error:** start_date > end_date
**Response:** 400 Bad Request - "Start date must be before end date"

### User Not Found
**Error:** Invalid user ID
**Response:** 404 Not Found - "User not found"

### Account Not Found
**Error:** User exists but Account doesn't (rare)
**Response:** 500 Internal Server Error

---

## Summary of Changes

| Component | File | Change |
|-----------|------|--------|
| **Backend** | `bankapp/transaction_generator.py` | Added `start_date` and `end_date` parameters to both methods |
| **Backend** | `bankapp/views.py` | Updated `AdminApproveUserView.post()` to accept and pass dates |
| **Frontend** | `REACT_ADMIN_COMPONENTS.md` | Updated `approveUser()` function with date prompts |
| **Documentation** | `REACT_ADMIN_COMPONENTS.md` | Added section 7 for DateRangeModal advanced component |
| **API** | `/api/admin/users/{id}/approve/` | Now accepts optional `start_date` and `end_date` in request body |

---

## Next Steps

1. **Test the backend** with custom dates using cURL
2. **Implement React component** with date prompts (simple) or modal (advanced)
3. **Deploy and test** admin approval workflow
4. **Build user dashboard** to display transactions from custom date ranges

---

**You now have a fully flexible transaction date system!** 🎉
