# 🏦 Midwestern Bank - Admin Dashboard & User Management API

Complete API documentation for user signup, login, and admin dashboard endpoints.

---

## 📋 Table of Contents

1. [User Endpoints](#user-endpoints)
2. [Admin Dashboard Endpoints](#admin-dashboard-endpoints)
3. [Database Changes](#database-changes)
4. [Authentication Flow](#authentication-flow)
5. [Example Requests & Responses](#example-requests--responses)
6. [React Implementation Guide](#react-implementation-guide)

---

## 👤 User Endpoints

### 1. **Sign Up** (No Auth Required)
Create a new user account. Any user can sign up.

**Endpoint:** `POST /api/signup/`

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "anypassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "password": "TempPass123"
}
```

**Status:** 
- `201 Created` - User created successfully
- `400 Bad Request` - Email already exists or validation failed

---

### 2. **Login** (No Auth Required)
Login with email and password. **Account must be approved by admin first!**

**Endpoint:** `POST /api/login/`

**Request:**
```json
{
  "email": "john@example.com",
  "password": "TempPass123"
}
```

**Response (200 OK):**
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

**Responses:**
- `200 OK` - Login successful
- `403 Forbidden` - Account not approved by admin
- `401 Unauthorized` - Invalid password
- `404 Not Found` - User not found

---

## 🛡️ Admin Dashboard Endpoints

### 1. **List All Users** 
Get all users with their approval status and account details.

**Endpoint:** `GET /api/admin/users/`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_joined": "2025-01-06T10:30:00Z",
    "account": {
      "is_approved": true,
      "total_balance": "70000.00",
      "available_balance": "69500.00",
      "transfer_count": 1,
      "created_at": "2025-01-06T10:30:00Z",
      "updated_at": "2025-01-06T14:00:00Z"
    }
  },
  {
    "id": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "date_joined": "2025-01-07T09:15:00Z",
    "account": {
      "is_approved": false,
      "total_balance": "70000.00",
      "available_balance": "70000.00",
      "transfer_count": 0,
      "created_at": "2025-01-07T09:15:00Z",
      "updated_at": "2025-01-07T09:15:00Z"
    }
  }
]
```

---

### 2. **Get User Details**
Get detailed information about a specific user.

**Endpoint:** `GET /api/admin/users/<user_id>/`

**Example:** `GET /api/admin/users/1/`

**Response (200 OK):**
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "date_joined": "2025-01-06T10:30:00Z",
  "account": {
    "is_approved": true,
    "total_balance": "70000.00",
    "available_balance": "69500.00",
    "transfer_count": 1,
    "created_at": "2025-01-06T10:30:00Z",
    "updated_at": "2025-01-06T14:00:00Z"
  }
}
```

---

### 3. **Approve/Reject User** ⭐ **ACTIVATION BUTTON**
Approve a user account to allow login, or reject it.

**Endpoint:** `POST /api/admin/users/<user_id>/approve/`

**Example:** `POST /api/admin/users/2/approve/`

**Request:**
```json
{
  "action": "approve"
}
```

**Response (200 OK):**
```json
{
  "message": "User jane@example.com has been approved and can now login",
  "user": {
    "id": 2,
    "email": "jane@example.com",
    "is_approved": true
  }
}
```

**To Reject User:**
```json
{
  "action": "reject"
}
```

**Response (200 OK):**
```json
{
  "message": "User jane@example.com has been rejected",
  "user": {
    "id": 2,
    "email": "jane@example.com",
    "is_approved": false
  }
}
```

---

### 4. **Reset Transfer Count** ⭐ **RESET BUTTON**
Reset the transfer count back to 0 to allow more transfers.

**Endpoint:** `POST /api/admin/users/<user_id>/reset-transfers/`

**Example:** `POST /api/admin/users/1/reset-transfers/`

**Request:** (No body required)
```json
{}
```

**Response (200 OK):**
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

---

### 5. **Delete User**
Permanently delete a user account.

**Endpoint:** `POST /api/admin/users/<user_id>/delete/`

**Example:** `POST /api/admin/users/2/delete/`

**Request:** (No body required)
```json
{}
```

**Response (200 OK):**
```json
{
  "message": "User jane@example.com has been deleted",
  "deleted_user_id": 2
}
```

---

## 🗄️ Database Changes

### New Field Added to Account Model

```python
class Account(models.Model):
    # ... existing fields ...
    is_approved = models.BooleanField(default=False)  # NEW
    created_at = models.DateTimeField(auto_now_add=True)  # NEW
    updated_at = models.DateTimeField(auto_now=True)  # NEW
```

### Migration Required

Run these commands to apply database changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔄 Authentication Flow

### New User Registration & Approval Flow

```
1. User Signs Up
   ↓
2. Account Created with is_approved = False
   ↓
3. User Cannot Login (receives: "Account not approved" error)
   ↓
4. Admin Reviews User in Dashboard
   ↓
5. Admin Clicks "Activate" Button
   ↓
6. is_approved = True
   ↓
7. User Can Now Login ✅
```

### Transfer Flow with Reset

```
1. User Makes Transfer (transfer_count = 1)
   ↓
2. User Makes Transfer (transfer_count = 2)
   ↓
3. User Cannot Make More Transfers
   ↓
4. Admin Clicks "Reset" Button
   ↓
5. transfer_count = 0
   ↓
6. User Can Make 2 More Transfers ✅
```

---

## 📝 Example Requests & Responses

### Complete User Flow Example

#### Step 1: User Signs Up
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "anypassword"
  }'
```

**Response:**
```json
{
  "message": "User created successfully",
  "password": "TempPass123"
}
```

#### Step 2: User Tries to Login (BEFORE Admin Approval)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

**Response (403 Forbidden):**
```json
{
  "error": "Your account is not yet approved. Please wait for admin approval."
}
```

#### Step 3: Admin Views All Users
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

#### Step 4: Admin Approves User
```bash
curl -X POST http://localhost:8000/api/admin/users/1/approve/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve"
  }'
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

#### Step 5: User Now Can Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

**Response (200 OK):**
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

---

## ⚛️ React Implementation Guide

### Admin Dashboard Component Structure

```javascript
// AdminDashboard.jsx
import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/admin/users/');
      const data = await response.json();
      setUsers(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
      setLoading(false);
    }
  };

  const approveUser = async (userId) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/admin/users/${userId}/approve/`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'approve' })
        }
      );
      if (response.ok) {
        alert('User approved successfully!');
        fetchUsers(); // Refresh list
      }
    } catch (error) {
      console.error('Error approving user:', error);
    }
  };

  const resetTransfers = async (userId) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/admin/users/${userId}/reset-transfers/`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        }
      );
      if (response.ok) {
        alert('Transfer count reset!');
        fetchUsers(); // Refresh list
      }
    } catch (error) {
      console.error('Error resetting transfers:', error);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/admin/users/${userId}/delete/`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          }
        );
        if (response.ok) {
          alert('User deleted successfully!');
          fetchUsers(); // Refresh list
        }
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <table className="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Transfer Count</th>
            <th>Balance</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.email}</td>
              <td>
                <span className={user.account?.is_approved ? 'approved' : 'pending'}>
                  {user.account?.is_approved ? 'Approved' : 'Pending'}
                </span>
              </td>
              <td>{user.account?.transfer_count || 0}</td>
              <td>${user.account?.available_balance || 0}</td>
              <td>
                {!user.account?.is_approved && (
                  <button 
                    onClick={() => approveUser(user.id)}
                    className="btn-approve"
                  >
                    ✓ Activate
                  </button>
                )}
                {user.account?.transfer_count >= 2 && (
                  <button 
                    onClick={() => resetTransfers(user.id)}
                    className="btn-reset"
                  >
                    🔄 Reset Transfers
                  </button>
                )}
                <button 
                  onClick={() => deleteUser(user.id)}
                  className="btn-delete"
                >
                  🗑️ Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
```

### CSS Styling

```css
.admin-dashboard {
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.users-table th {
  background: linear-gradient(135deg, #0066cc 0%, #004ba3 100%);
  color: white;
  padding: 15px;
  text-align: left;
  font-weight: 600;
}

.users-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.users-table tr:hover {
  background: #f0f7ff;
}

.btn-approve, .btn-reset, .btn-delete {
  padding: 8px 12px;
  margin: 5px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-approve {
  background: linear-gradient(135deg, #0066cc 0%, #004ba3 100%);
  color: white;
}

.btn-approve:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.btn-reset {
  background: #ff9800;
  color: white;
}

.btn-reset:hover {
  background: #e68900;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
}

.approved {
  background: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: 600;
}

.pending {
  background: #ff9800;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: 600;
}
```

---

## 🚀 Summary

### What Changed

1. ✅ **Sign Up** - Open to anyone (no approval required)
2. ✅ **Login** - Requires admin approval (`is_approved = True`)
3. ✅ **Admin List Users** - See all users and their status
4. ✅ **Admin Approve User** - Click "Activate" button
5. ✅ **Admin Reset Transfers** - Click "Reset" button
6. ✅ **Admin Delete User** - Remove users

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/signup/` | User registration |
| POST | `/api/login/` | User login (requires approval) |
| GET | `/api/admin/users/` | List all users |
| GET | `/api/admin/users/{id}/` | Get user details |
| POST | `/api/admin/users/{id}/approve/` | Approve/activate user |
| POST | `/api/admin/users/{id}/reset-transfers/` | Reset transfer count |
| POST | `/api/admin/users/{id}/delete/` | Delete user |

**Ready for React frontend development!** 🎉
