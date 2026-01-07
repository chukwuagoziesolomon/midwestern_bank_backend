# 🏦 Midwestern Bank - Admin System Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Create Admin Account
```bash
python manage.py create_admin
```

**Interactive prompts:**
- Enter admin email: `admin@midwesternbank.com`
- Enter admin password: `SecurePass123`
- Enter first name: `John` (optional, default: Admin)
- Enter last name: `Doe` (optional, default: User)

**Or with arguments:**
```bash
python manage.py create_admin --email admin@midwesternbank.com --password SecurePass123 --first-name John --last-name Doe
```

### Step 2: Start Django Server
```bash
python manage.py runserver
```

Server running at: `http://localhost:8000`

---

## 📋 Admin System Flow

### What Admins Can Do:
1. **View All Users** - See list of pending and approved users
2. **Approve Users** - Click approve to activate an account
3. **Auto-Generate Transactions** - 15 backdated transactions created automatically
4. **Reset Transfers** - Allow users to make more transfers
5. **Delete Users** - Remove user accounts
6. **Manage Approvals** - Accept or reject users

### What Users Get When Approved:
- ✅ **$70,000 Initial Balance** (already set at signup)
- ✅ **15 Dummy Transactions** (backdated from Dec 2023 to Jan 2026)
- ✅ **5 Dummy Deposits** (backdated from Dec 2023 to Jan 2026)
- ✅ **Full Transaction History** (visible in dashboard)
- ✅ **Login Access** (can now access the app)

---

## 🔄 Complete User Journey

```
1. NEW USER SIGNS UP
   ↓
   POST /api/signup/
   {
     "first_name": "John",
     "last_name": "Doe",
     "email": "john@example.com",
     "password": "TempPass123"
   }
   ↓
   Account Created:
   - Balance: $70,000
   - is_approved: False
   - Status: PENDING APPROVAL

2. USER TRIES TO LOGIN
   ↓
   POST /api/login/
   {
     "email": "john@example.com",
     "password": "TempPass123"
   }
   ↓
   Response: 403 Forbidden
   Error: "Your account is not yet approved. Please wait for admin approval."

3. ADMIN REVIEWS IN DASHBOARD
   ↓
   Admin sees list of pending users
   Clicks "Approve" button for john@example.com

4. SYSTEM AUTO-GENERATES
   ↓
   - Sets is_approved = True
   - Creates 15 realistic transactions (Dec 2023 - Jan 2026)
   - Creates 5 realistic deposits (Dec 2023 - Jan 2026)
   - Returns 200 OK response

5. USER LOGS IN SUCCESSFULLY
   ↓
   POST /api/login/
   {
     "email": "john@example.com",
     "password": "TempPass123"
   }
   ↓
   Response: 200 OK
   {
     "message": "Login successful",
     "user": {
       "id": 2,
       "email": "john@example.com",
       "is_approved": true
     }
   }

6. USER SEES DASHBOARD
   ↓
   - Balance: $70,000
   - Transactions: 15 items (backdated)
   - Deposits: 5 items (backdated)
   - Can now make real transfers
```

---

## 🎯 Admin Dashboard Endpoints

### Get All Users
```bash
GET /api/admin/users/
```

### Get Specific User
```bash
GET /api/admin/users/{user_id}/
```

### Approve User ⭐ (Generates Transactions)
```bash
POST /api/admin/users/{user_id}/approve/
{
  "action": "approve"
}
```

**Response includes:**
- message
- user.is_approved = true
- transactions_generated: 15

### Reject User
```bash
POST /api/admin/users/{user_id}/approve/
{
  "action": "reject"
}
```

### Reset Transfer Count 🔄
```bash
POST /api/admin/users/{user_id}/reset-transfers/
```

Use when user has made 2 transfers and is blocked.

### Delete User
```bash
POST /api/admin/users/{user_id}/delete/
```

---

## 💻 React Frontend Example

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const API = 'http://localhost:8000/api';

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    const { data } = await axios.get(`${API}/admin/users/`);
    setUsers(data);
    setLoading(false);
  };

  const approveUser = async (userId) => {
    await axios.post(`${API}/admin/users/${userId}/approve/`, { action: 'approve' });
    alert('✅ User approved! 15 transactions generated.');
    fetchUsers();
  };

  const resetTransfers = async (userId) => {
    await axios.post(`${API}/admin/users/${userId}/reset-transfers/`);
    alert('🔄 Transfer count reset!');
    fetchUsers();
  };

  return (
    <div>
      <h1>👨‍💼 Admin Dashboard</h1>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
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
                <strong style={{
                  color: user.account?.is_approved ? 'green' : 'orange'
                }}>
                  {user.account?.is_approved ? '✓ Approved' : '⏳ Pending'}
                </strong>
              </td>
              <td>${user.account?.available_balance}</td>
              <td>
                <button 
                  onClick={() => approveUser(user.id)}
                  disabled={user.account?.is_approved}
                >
                  Approve
                </button>
                <button onClick={() => resetTransfers(user.id)}>
                  Reset Transfers
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

## 🧪 Testing Steps

### 1. Create Admin
```bash
python manage.py create_admin --email admin@bank.com --password Pass123
```

### 2. Start Server
```bash
python manage.py runserver
```

### 3. User Signs Up
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"TempPass123"}'
```

### 4. User Tries Login (Will Fail)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"TempPass123"}'
```
Result: `403 Forbidden` ❌

### 5. Admin Approves User (ID=2)
```bash
curl -X POST http://localhost:8000/api/admin/users/2/approve/ \
  -H "Content-Type: application/json" \
  -d '{"action":"approve"}'
```
Result: `200 OK` ✅ + 15 transactions generated!

### 6. User Logs In (Will Succeed)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"TempPass123"}'
```
Result: `200 OK` ✅

### 7. Check Transaction History
```bash
curl -X GET http://localhost:8000/api/transfer/?user_id=2
```
Result: 15 transactions visible ✅

---

## 📊 Generated Transactions Details

When admin approves a user:

**15 Transfers Created:**
- Random dates from December 2023 to January 2026
- Amounts: $100 - $5000
- Types: Local or International
- Realistic receiver names and banks
- Real-looking descriptions (Salary, Invoice, etc.)
- Status: Completed

**5 Deposits Created:**
- Random dates from December 2023 to January 2026
- Amounts: $500 - $3000
- Via credit card (existing card details used)
- Status: Completed

**Total Timeline:** 2+ years of transaction history visible!

---

## 🔐 Security Notes

✅ **Admins are Superusers** - Created with `is_superuser=True`
✅ **Users are Regular Users** - Can only access their own account
✅ **Passwords** - Use strong passwords for admin
✅ **Approval Process** - Prevents unauthorized access
✅ **Open Signup** - Anyone can register, but needs approval to login

---

## 🚀 Ready to Use!

Your admin system is complete and ready for:
- ✅ User management
- ✅ Account approval
- ✅ Transfer resets
- ✅ Realistic transaction history

**Next Steps:**
1. Create your admin account
2. Build your React frontend using the admin endpoints
3. Test the full user journey
4. Deploy to production

**Happy Banking!** 🏦
