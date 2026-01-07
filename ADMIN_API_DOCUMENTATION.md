# 🏦 Midwestern Bank - Admin Dashboard & Auth API Documentation

## 📋 Overview

This API provides:
- **Open User Signup** - Anyone can register
- **Admin Approval System** - Only approved users can login
- **Automatic Transaction History** - Dummy transactions from Dec 2023 to Jan 2026 generated on approval
- **Admin Dashboard** - Manage users, approve accounts, reset transfers
- **$70,000 Initial Balance** - Every new user starts with this amount

**Base URL:** `http://localhost:8000/api/`

---

## 🚀 Quick Start - Create Admin Account

Before you start, create a superuser/admin account:

```bash
python manage.py create_admin
```

Or with arguments:
```bash
python manage.py create_admin --email admin@midwesternbank.com --password SecurePassword123 --first-name John --last-name Admin
```

**Admin Features:**
- ✅ Can view all users
- ✅ Can approve/activate user accounts
- ✅ Can reset transfer counts
- ✅ Can delete user accounts
- ✅ Automatically approved for login

---

## 🔐 Authentication Flow

### 1. **User Signup** (Open to Everyone)
```
POST /signup/
```

**Request:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "TempPass123"
}
```

**Response:**
```json
{
    "message": "User created successfully",
    "password": "TempPass123"
}
```

**Status Code:** `201 Created`

**What Happens:**
- ✅ Account created with `is_approved = False`
- ✅ Initial balance set to $70,000
- ✅ Random card details generated
- ✅ User added to pending approval list

---

### 2. **User Login** (Requires Admin Approval)
```
POST /login/
```

**Request:**
```json
{
    "email": "john@example.com",
    "password": "TempPass123"
}
```

**Response (Success - User Approved):**
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

**Response (Not Approved):**
```json
{
    "error": "Your account is not yet approved. Please wait for admin approval."
}
```

**Status Code:** 
- `200 OK` - Login successful
- `403 Forbidden` - Account not approved
- `401 Unauthorized` - Invalid password
- `404 Not Found` - User not found

---

## 👨‍💼 Admin Dashboard Endpoints

### 1. **List All Users**
```
GET /admin/users/
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
    },
    {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "date_joined": "2025-01-07T11:00:00Z",
        "account": {
            "is_approved": true,
            "total_balance": "70000.00",
            "available_balance": "65000.00",
            "transfer_count": 1,
            "created_at": "2025-01-07T11:00:00Z",
            "updated_at": "2025-01-07T11:15:00Z"
        }
    }
]
```

**Status Code:** `200 OK`

---

### 2. **Get User Details**
```
GET /admin/users/<user_id>/
```

**Example:**
```
GET /admin/users/1/
```

**Response:**
```json
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
```

**Status Code:** 
- `200 OK` - User found
- `404 Not Found` - User not found

---

### 3. **Approve/Activate User Account** ⭐ (MOST IMPORTANT)
```
POST /admin/users/<user_id>/approve/
```

**Example:**
```
POST /admin/users/1/approve/
```

**Request:**
```json
{
    "action": "approve"
}
```

**Response (Approve):**
```json
{
    "message": "User john@example.com has been approved and can now login. Transaction history generated.",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "is_approved": true,
        "initial_balance": "70000.00",
        "transactions_generated": 15
    }
}
```

**What Happens When You Approve:**
1. ✅ `is_approved` set to `True`
2. ✅ **15 dummy transactions generated** (backdated from Dec 2023 to Jan 2026)
3. ✅ **5 dummy deposits generated** (backdated from Dec 2023 to Jan 2026)
4. ✅ User can now login
5. ✅ Dashboard shows full transaction history

**Request (Reject):**
```json
{
    "action": "reject"
}
```

**Response (Reject):**
```json
{
    "message": "User john@example.com has been rejected",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "is_approved": false
    }
}
```

**Status Code:** 
- `200 OK` - Action completed
- `400 Bad Request` - Invalid action
- `404 Not Found` - User not found

---

### 4. **Reset Transfer Count** 🔄
```
POST /admin/users/<user_id>/reset-transfers/
```

**Example:**
```
POST /admin/users/1/reset-transfers/
```

**Request:** (No body needed)

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

**Use Case:** User has made 2 transfers and is blocked. Click this to reset and allow more transfers.

**Status Code:** 
- `200 OK` - Reset successful
- `404 Not Found` - User not found

---

### 5. **Delete User Account** 🗑️
```
POST /admin/users/<user_id>/delete/
```

**Example:**
```
POST /admin/users/1/delete/
```

**Request:** (No body needed)

**Response:**
```json
{
    "message": "User john@example.com has been deleted",
    "deleted_user_id": 1
}
```

**Status Code:** 
- `200 OK` - User deleted
- `404 Not Found` - User not found

---

## 📱 React Frontend Integration

### **Admin Dashboard Component Example**

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_BASE = 'http://localhost:8000/api';

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/users/`);
      setUsers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const approveUser = async (userId) => {
    try {
      const response = await axios.post(
        `${API_BASE}/admin/users/${userId}/approve/`,
        { action: 'approve' }
      );
      alert('✅ ' + response.data.message);
      alert('🎉 15 transactions generated with $70,000 initial balance!');
      fetchUsers();
    } catch (error) {
      console.error('Error approving user:', error);
      alert('❌ Error: ' + error.response.data.error);
    }
  };

  const rejectUser = async (userId) => {
    try {
      const response = await axios.post(
        `${API_BASE}/admin/users/${userId}/approve/`,
        { action: 'reject' }
      );
      alert('❌ ' + response.data.message);
      fetchUsers();
    } catch (error) {
      console.error('Error rejecting user:', error);
    }
  };

  const resetTransfers = async (userId) => {
    try {
      const response = await axios.post(
        `${API_BASE}/admin/users/${userId}/reset-transfers/`
      );
      alert('🔄 ' + response.data.message);
      fetchUsers();
    } catch (error) {
      console.error('Error resetting transfers:', error);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        const response = await axios.post(
          `${API_BASE}/admin/users/${userId}/delete/`
        );
        alert('🗑️ ' + response.data.message);
        fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="admin-dashboard">
      <h1>👨‍💼 Admin Dashboard - Midwestern Bank</h1>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Balance</th>
            <th>Transfers</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.email}</td>
              <td>
                {user.account?.is_approved ? (
                  <span style={{ color: 'green', fontWeight: 'bold' }}>
                    ✓ Approved
                  </span>
                ) : (
                  <span style={{ color: 'orange', fontWeight: 'bold' }}>
                    ⏳ Pending
                  </span>
                )}
              </td>
              <td>${user.account?.available_balance}</td>
              <td>{user.account?.transfer_count}/2</td>
              <td>{new Date(user.date_joined).toLocaleDateString()}</td>
              <td>
                <button 
                  onClick={() => approveUser(user.id)}
                  disabled={user.account?.is_approved}
                  style={{ 
                    marginRight: '5px',
                    backgroundColor: user.account?.is_approved ? '#ccc' : '#4CAF50',
                    color: 'white',
                    padding: '8px 12px',
                    border: 'none',
                    cursor: user.account?.is_approved ? 'not-allowed' : 'pointer'
                  }}
                >
                  {user.account?.is_approved ? 'Already Approved' : 'Approve ✓'}
                </button>
                {user.account?.is_approved && (
                  <button 
                    onClick={() => rejectUser(user.id)}
                    style={{ 
                      marginRight: '5px',
                      backgroundColor: '#FF9800',
                      color: 'white',
                      padding: '8px 12px',
                      border: 'none',
                      cursor: 'pointer'
                    }}
                  >
                    Reject ✗
                  </button>
                )}
                <button 
                  onClick={() => resetTransfers(user.id)}
                  style={{ 
                    marginRight: '5px',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    padding: '8px 12px',
                    border: 'none',
                    cursor: 'pointer'
                  }}
                >
                  Reset 🔄
                </button>
                <button 
                  onClick={() => deleteUser(user.id)}
                  style={{ 
                    backgroundColor: '#f44336',
                    color: 'white',
                    padding: '8px 12px',
                    border: 'none',
                    cursor: 'pointer'
                  }}
                >
                  Delete 🗑️
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

---

## 🛡️ Key Features

✅ **Open Signup** - Anyone can create an account
✅ **Admin Approval** - Only approved users can login
✅ **Automatic Transactions** - 15 dummy transactions generated on approval
✅ **Backdated Transactions** - Transactions from December 2023 to January 2026
✅ **$70,000 Initial Balance** - Every new user starts with this amount
✅ **Reset Transfers** - Admin can reset transfer count (fixes the 2-transfer limit)
✅ **User Management** - View, approve, reject, and delete users
✅ **Superuser Admin** - Create admin with `create_admin` command
✅ **Easy Integration** - Simple REST API for React frontend

---

## 📊 User Account Lifecycle

```
1. User Signup
   └─> Account created (is_approved = False)
   └─> Balance = $70,000
   └─> No transactions

2. Admin Reviews & Approves
   └─> Click "Approve" button in admin dashboard

3. System Auto-Generates
   └─> 15 dummy transactions (Dec 2023 - Jan 2026)
   └─> 5 dummy deposits (Dec 2023 - Jan 2026)
   └─> is_approved = True

4. User Can Login
   └─> Dashboard shows full transaction history
   └─> Can make real transfers

5. Admin Can Reset
   └─> Click "Reset Transfers" to allow more transfers
```

---

## ⚡ Quick Setup Steps

### Step 1: Create Admin Account
```bash
python manage.py create_admin
```

Follow the prompts to enter:
- Admin email
- Admin password
- Admin name (optional)

### Step 2: Start Django Server
```bash
python manage.py runserver
```

### Step 3: User Signs Up
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

### Step 4: User Tries to Login (Will Fail)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```
Response: `403 Forbidden` - Not approved yet

### Step 5: Admin Approves User
```bash
curl -X POST http://localhost:8000/api/admin/users/2/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```
Response: `200 OK` - 15 transactions generated!

### Step 6: User Can Now Login
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```
Response: `200 OK` - Login successful!

### Step 7: User Sees Dashboard
User now has:
- ✅ $70,000 balance
- ✅ 15 transactions from Dec 2023 - Jan 2026
- ✅ Full transaction history

---

## 🔍 Testing with cURL

### Get All Users
```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Content-Type: application/json"
```

### Get Specific User
```bash
curl -X GET http://localhost:8000/api/admin/users/2/ \
  -H "Content-Type: application/json"
```

### Approve User
```bash
curl -X POST http://localhost:8000/api/admin/users/2/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```

### Reset Transfer Count
```bash
curl -X POST http://localhost:8000/api/admin/users/2/reset-transfers/ \
  -H "Content-Type: application/json"
```

### Delete User
```bash
curl -X POST http://localhost:8000/api/admin/users/2/delete/ \
  -H "Content-Type: application/json"
```

---

## 🚀 Production Deployment

1. Use environment variables for credentials
2. Enable Django CSRF protection
3. Use HTTPS for all API calls
4. Implement API rate limiting
5. Add JWT authentication (optional)
6. Monitor admin actions in logs
7. Backup database regularly

---

**Your Midwestern Bank Admin System is Ready!** 🎉


### 1. **User Signup** (Open to Everyone)
```
POST /signup/
```

**Request:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "TempPass123"
}
```

**Response:**
```json
{
    "message": "User created successfully",
    "password": "TempPass123"
}
```

**Status Code:** `201 Created`

---

### 2. **User Login** (Requires Admin Approval)
```
POST /login/
```

**Request:**
```json
{
    "email": "john@example.com",
    "password": "TempPass123"
}
```

**Response (Success):**
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

**Response (Not Approved):**
```json
{
    "error": "Your account is not yet approved. Please wait for admin approval."
}
```

**Status Code:** 
- `200 OK` - Login successful
- `403 Forbidden` - Account not approved
- `401 Unauthorized` - Invalid password
- `404 Not Found` - User not found

---

## 👨‍💼 Admin Dashboard Endpoints

### 1. **List All Users**
```
GET /admin/users/
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
    },
    {
        "id": 2,
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com",
        "date_joined": "2025-01-07T11:00:00Z",
        "account": {
            "is_approved": true,
            "total_balance": "70000.00",
            "available_balance": "65000.00",
            "transfer_count": 1,
            "created_at": "2025-01-07T11:00:00Z",
            "updated_at": "2025-01-07T11:15:00Z"
        }
    }
]
```

**Status Code:** `200 OK`

---

### 2. **Get User Details**
```
GET /admin/users/<user_id>/
```

**Example:**
```
GET /admin/users/1/
```

**Response:**
```json
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
```

**Status Code:** 
- `200 OK` - User found
- `404 Not Found` - User not found

---

### 3. **Approve/Activate User Account** ⭐
```
POST /admin/users/<user_id>/approve/
```

**Example:**
```
POST /admin/users/1/approve/
```

**Request:**
```json
{
    "action": "approve"
}
```

**Response (Approve):**
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

**Request (Reject):**
```json
{
    "action": "reject"
}
```

**Response (Reject):**
```json
{
    "message": "User john@example.com has been rejected",
    "user": {
        "id": 1,
        "email": "john@example.com",
        "is_approved": false
    }
}
```

**Status Code:** 
- `200 OK` - Action completed
- `400 Bad Request` - Invalid action
- `404 Not Found` - User not found

---

### 4. **Reset Transfer Count** 🔄
```
POST /admin/users/<user_id>/reset-transfers/
```

**Example:**
```
POST /admin/users/1/reset-transfers/
```

**Request:** (No body needed)

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

**Status Code:** 
- `200 OK` - Reset successful
- `404 Not Found` - User not found

---

### 5. **Delete User Account** 🗑️
```
POST /admin/users/<user_id>/delete/
```

**Example:**
```
POST /admin/users/1/delete/
```

**Request:** (No body needed)

**Response:**
```json
{
    "message": "User john@example.com has been deleted",
    "deleted_user_id": 1
}
```

**Status Code:** 
- `200 OK` - User deleted
- `404 Not Found` - User not found

---

## 📱 React Frontend Integration

### **Admin Dashboard Component Example**

```javascript
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
    }
  };

  const approveUser = async (userId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/admin/users/${userId}/approve/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: 'approve' })
      });
      const data = await response.json();
      alert(data.message);
      fetchUsers(); // Refresh list
    } catch (error) {
      console.error('Error approving user:', error);
    }
  };

  const resetTransfers = async (userId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/admin/users/${userId}/reset-transfers/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      const data = await response.json();
      alert(data.message);
      fetchUsers(); // Refresh list
    } catch (error) {
      console.error('Error resetting transfers:', error);
    }
  };

  const deleteUser = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        const response = await fetch(`http://localhost:8000/api/admin/users/${userId}/delete/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        const data = await response.json();
        alert(data.message);
        fetchUsers(); // Refresh list
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="admin-dashboard">
      <h1>👨‍💼 Admin Dashboard</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Transfers</th>
            <th>Balance</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.first_name} {user.last_name}</td>
              <td>{user.email}</td>
              <td>
                {user.account?.is_approved ? (
                  <span style={{ color: 'green' }}>✓ Approved</span>
                ) : (
                  <span style={{ color: 'red' }}>✗ Pending</span>
                )}
              </td>
              <td>{user.account?.transfer_count}/2</td>
              <td>${user.account?.available_balance}</td>
              <td>
                <button 
                  onClick={() => approveUser(user.id)}
                  disabled={user.account?.is_approved}
                >
                  Approve
                </button>
                <button 
                  onClick={() => resetTransfers(user.id)}
                >
                  Reset Transfers
                </button>
                <button 
                  onClick={() => deleteUser(user.id)}
                  style={{ color: 'red' }}
                >
                  Delete
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

---

## 🛡️ Key Features

✅ **Open Signup** - Anyone can create an account
✅ **Admin Approval** - Only approved users can login
✅ **Reset Transfers** - Admin can reset transfer count (solves the 2-transfer limit issue)
✅ **User Management** - View, approve, and delete users
✅ **Transaction Blocking** - Users without approval cannot access the system
✅ **Easy Integration** - Simple REST API for React frontend

---

## 📊 User Account Lifecycle

```
1. User Signup
   └─> Account created (is_approved = False)

2. Admin Review
   └─> Admin clicks "Approve" button

3. User Can Login
   └─> is_approved = True

4. User Makes Transfers
   └─> transfer_count increases

5. Admin Resets
   └─> transfer_count reset to 0
```

---

## ⚡ Quick Start for React

### **Install Axios** (for API calls)
```bash
npm install axios
```

### **Setup API Client**
```javascript
// api/client.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  // Auth
  signup: (data) => axios.post(`${API_BASE}/signup/`, data),
  login: (data) => axios.post(`${API_BASE}/login/`, data),
  
  // Admin
  getUsers: () => axios.get(`${API_BASE}/admin/users/`),
  getUserDetails: (id) => axios.get(`${API_BASE}/admin/users/${id}/`),
  approveUser: (id) => axios.post(`${API_BASE}/admin/users/${id}/approve/`, { action: 'approve' }),
  rejectUser: (id) => axios.post(`${API_BASE}/admin/users/${id}/approve/`, { action: 'reject' }),
  resetTransfers: (id) => axios.post(`${API_BASE}/admin/users/${id}/reset-transfers/`),
  deleteUser: (id) => axios.post(`${API_BASE}/admin/users/${id}/delete/`)
};
```

---

## 🔍 Testing

### **Test Signup**
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```

### **Test Login (Before Approval)**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```
Response: `403 Forbidden` - Not approved yet

### **Test Approve User**
```bash
curl -X POST http://localhost:8000/api/admin/users/1/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```

### **Test Login (After Approval)**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "TempPass123"
  }'
```
Response: `200 OK` - Login successful

### **Test Reset Transfers**
```bash
curl -X POST http://localhost:8000/api/admin/users/1/reset-transfers/ \
  -H "Content-Type: application/json"
```

---

## 🚀 Production Deployment

1. Use environment variables for database credentials
2. Enable Django CSRF protection
3. Use HTTPS for all API calls
4. Implement API rate limiting
5. Add proper authentication tokens (JWT recommended)
6. Monitor admin actions in logs

---

**Ready to build your React Admin Dashboard!** 🎉
