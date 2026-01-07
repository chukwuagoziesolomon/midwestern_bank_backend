# 🏦 Admin Dashboard Setup Guide

Quick setup instructions for the new admin dashboard and user approval system.

---

## ✅ What Was Added

1. **User Approval System** - Only approved users can login
2. **Admin Dashboard Endpoints** - Manage users, approve accounts, reset transfers
3. **Database Fields** - `is_approved`, `created_at`, `updated_at` on Account model
4. **5 New API Endpoints** for admin operations

---

## 🚀 Quick Setup

### Step 1: Apply Database Migration

```bash
cd "C:\Users\USER-PC\midwestern backend\config"
python manage.py migrate
```

This will add the new fields to the Account table:
- `is_approved` (Boolean, default: False)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Step 2: Test the Endpoints

#### A. User Signs Up
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "message": "User created successfully",
  "password": "TempPass123"
}
```

#### B. User Tries to Login (FAILS - Not Approved)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

**Response:**
```json
{
  "error": "Your account is not yet approved. Please wait for admin approval."
}
```

#### C. Admin Lists All Users
```bash
curl -X GET http://localhost:8000/api/admin/users/
```

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_joined": "2025-01-07T10:30:00Z",
    "account": {
      "is_approved": false,
      "total_balance": "70000.00",
      "available_balance": "70000.00",
      "transfer_count": 0,
      "created_at": "2025-01-07T10:30:00Z",
      "updated_at": "2025-01-07T10:30:00Z"
    }
  }
]
```

#### D. Admin Approves User (ACTIVATE BUTTON)
```bash
curl -X POST http://localhost:8000/api/admin/users/1/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```

**Response:**
```json
{
  "message": "User john@example.com has been approved and can now login",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "is_approved": true
  }
}
```

#### E. User Now Can Login (SUCCESS)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_approved": true
  }
}
```

#### F. User Makes 2 Transfers and Hits Limit
(User makes transfer → transfer_count becomes 1)
(User makes transfer → transfer_count becomes 2)
(User tries to make 3rd transfer → ERROR: "Transfer quota exceeded")

#### G. Admin Resets Transfer Count (RESET BUTTON)
```bash
curl -X POST http://localhost:8000/api/admin/users/1/reset-transfers/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "message": "Transfer count reset for user john@example.com",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "transfer_count": 0
  }
}
```

#### H. User Can Now Make More Transfers
(transfer_count reset to 0, user can make 2 more transfers)

---

## 📊 Admin Dashboard Endpoints Summary

| Action | Endpoint | Method | Purpose |
|--------|----------|--------|---------|
| List Users | `/api/admin/users/` | GET | See all users |
| User Details | `/api/admin/users/{id}/` | GET | View specific user |
| **Activate** ⭐ | `/api/admin/users/{id}/approve/` | POST | Approve user for login |
| **Reset** ⭐ | `/api/admin/users/{id}/reset-transfers/` | POST | Reset transfer quota |
| Delete User | `/api/admin/users/{id}/delete/` | POST | Remove user |

---

## 💻 React Component Example

Use the React code from `ADMIN_DASHBOARD_API.md` file to build the dashboard:

```javascript
// AdminDashboard.jsx
- List all users in a table
- Show approval status (Approved / Pending)
- Activate button for pending users
- Reset button for users with transfer_count >= 2
- Delete button for any user
```

The complete React code is in `ADMIN_DASHBOARD_API.md` with CSS styling included.

---

## 🔄 User Journey

```
1. User Signs Up (Email + Name)
   ↓ is_approved = False (CANNOT LOGIN)
   ↓
2. Admin Views Dashboard
   ↓ Sees Pending Users
   ↓
3. Admin Clicks "Activate" Button
   ↓ is_approved = True (CAN LOGIN)
   ↓
4. User Logs In Successfully
   ↓ Can Access Dashboard
   ↓
5. User Makes Transfers
   ↓ After 2 Transfers: BLOCKED
   ↓
6. Admin Clicks "Reset" Button
   ↓ transfer_count = 0
   ↓
7. User Can Make 2 More Transfers
```

---

## 📝 Files Modified/Created

### Modified:
- ✅ `bankapp/models.py` - Added is_approved, created_at, updated_at
- ✅ `bankapp/serializers.py` - Added admin serializers
- ✅ `bankapp/views.py` - Modified LoginView, added 5 admin views
- ✅ `bankapp/urls.py` - Added 5 new admin endpoints

### Created:
- ✅ `bankapp/migrations/0005_account_is_approved.py` - Database migration
- ✅ `ADMIN_DASHBOARD_API.md` - Complete API documentation
- ✅ `ADMIN_SETUP.md` - This file

---

## 🛠️ Troubleshooting

### Migration Failed?
```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (if needed)
python manage.py migrate bankapp zero
python manage.py migrate
```

### Endpoints Not Working?
```bash
# Check if server is running
python manage.py runserver

# Verify URLs are correct in urls.py
# Should have paths like: admin/users/, admin/users/<id>/approve/, etc.
```

### User Can't Login After Approval?
1. Check `is_approved = True` in admin users list
2. Verify password is correct (TempPass123)
3. Check LoginView code includes approval check

---

## 🎯 Next Steps

1. ✅ Run migration: `python manage.py migrate`
2. ✅ Test endpoints with curl commands above
3. ✅ Build React Admin Dashboard using code from `ADMIN_DASHBOARD_API.md`
4. ✅ Test signup → login → approval → login flow
5. ✅ Test transfer → quota → reset flow

---

## 📚 Documentation

- **Full API Details**: See `ADMIN_DASHBOARD_API.md`
- **Email Templates**: See `EMAIL_INTEGRATION_GUIDE.md`
- **Architecture**: See `ARCHITECTURE_DIAGRAMS.md`

---

**Your admin dashboard is ready!** 🚀
