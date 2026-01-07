# 🚀 React Admin Dashboard Component Examples

## Installation

```bash
npm install axios
```

---

## 1. Admin Dashboard Component

```javascript
// AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminDashboard.css';

const API_BASE = 'http://localhost:8000/api';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'approved'

  useEffect(() => {
    fetchUsers();
    // Refresh every 10 seconds
    const interval = setInterval(fetchUsers, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/users/`);
      setUsers(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching users:', error);
      setLoading(false);
    }
  };

  const approveUser = async (userId, userName) => {
    // Get custom date range from admin
    const startDate = prompt(
      'Enter start date for transaction history (YYYY-MM-DD):\n\nExample: 2024-01-01\nLeave blank for Dec 1, 2023',
      '2023-12-01'
    );
    
    if (startDate === null) return; // User cancelled
    
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

  const rejectUser = async (userId, userName) => {
    if (window.confirm(`Reject ${userName}?`)) {
      try {
        await axios.post(
          `${API_BASE}/admin/users/${userId}/approve/`,
          { action: 'reject' }
        );
        alert(`❌ ${userName} has been rejected`);
        fetchUsers();
      } catch (error) {
        alert(`Error: ${error.response.data.error}`);
      }
    }
  };

  const resetTransfers = async (userId, userName) => {
    try {
      const response = await axios.post(
        `${API_BASE}/admin/users/${userId}/reset-transfers/`
      );
      alert(`🔄 Transfer count reset for ${userName}`);
      fetchUsers();
    } catch (error) {
      alert(`Error: ${error.response.data.error}`);
    }
  };

  const deleteUser = async (userId, userName) => {
    if (window.confirm(`Delete ${userName}? This cannot be undone!`)) {
      try {
        await axios.post(
          `${API_BASE}/admin/users/${userId}/delete/`
        );
        alert(`🗑️ ${userName} has been deleted`);
        fetchUsers();
      } catch (error) {
        alert(`Error: ${error.response.data.error}`);
      }
    }
  };

  const filteredUsers = users.filter(user => {
    if (filter === 'pending') return !user.account?.is_approved;
    if (filter === 'approved') return user.account?.is_approved;
    return true;
  });

  const pendingCount = users.filter(u => !u.account?.is_approved).length;
  const approvedCount = users.filter(u => u.account?.is_approved).length;

  if (loading) {
    return (
      <div className="admin-dashboard loading">
        <div className="spinner">Loading...</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="header">
        <h1>👨‍💼 Midwestern Bank Admin Dashboard</h1>
        <div className="stats">
          <div className="stat-card">
            <h3>{users.length}</h3>
            <p>Total Users</p>
          </div>
          <div className="stat-card pending">
            <h3>{pendingCount}</h3>
            <p>Pending Approval</p>
          </div>
          <div className="stat-card approved">
            <h3>{approvedCount}</h3>
            <p>Approved Users</p>
          </div>
        </div>
      </div>

      <div className="filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Users ({users.length})
        </button>
        <button
          className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => setFilter('pending')}
        >
          Pending ({pendingCount})
        </button>
        <button
          className={`filter-btn ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => setFilter('approved')}
        >
          Approved ({approvedCount})
        </button>
      </div>

      <div className="table-container">
        <table className="users-table">
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
            {filteredUsers.map(user => {
              const fullName = `${user.first_name} ${user.last_name}`;
              const isApproved = user.account?.is_approved;
              const joinDate = new Date(user.date_joined).toLocaleDateString();
              
              return (
                <tr key={user.id} className={isApproved ? 'approved' : 'pending'}>
                  <td className="name">{fullName}</td>
                  <td className="email">{user.email}</td>
                  <td className="status">
                    <span className={`badge ${isApproved ? 'approved' : 'pending'}`}>
                      {isApproved ? '✓ Approved' : '⏳ Pending'}
                    </span>
                  </td>
                  <td className="balance">
                    ${user.account?.available_balance}
                  </td>
                  <td className="transfers">
                    {user.account?.transfer_count}/2
                  </td>
                  <td className="date">{joinDate}</td>
                  <td className="actions">
                    <div className="action-buttons">
                      {!isApproved ? (
                        <>
                          <button
                            className="btn btn-approve"
                            onClick={() => approveUser(user.id, fullName)}
                            title="Approve user and generate 15 transactions"
                          >
                            ✓ Approve
                          </button>
                          <button
                            className="btn btn-reject"
                            onClick={() => rejectUser(user.id, fullName)}
                            title="Reject user"
                          >
                            ✗ Reject
                          </button>
                        </>
                      ) : (
                        <button
                          className="btn btn-reject"
                          onClick={() => rejectUser(user.id, fullName)}
                          title="Revoke approval"
                        >
                          🔒 Revoke
                        </button>
                      )}
                      
                      <button
                        className="btn btn-reset"
                        onClick={() => resetTransfers(user.id, fullName)}
                        title="Reset transfer count to 0"
                      >
                        🔄 Reset
                      </button>
                      
                      <button
                        className="btn btn-delete"
                        onClick={() => deleteUser(user.id, fullName)}
                        title="Delete user permanently"
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {filteredUsers.length === 0 && (
          <div className="no-users">
            <p>No users found in this category</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
```

---

## 2. CSS Styling

```css
/* AdminDashboard.css */
.admin-dashboard {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.header {
  background: white;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 51, 102, 0.1);
}

.header h1 {
  color: #0066cc;
  margin: 0 0 20px 0;
  font-size: 28px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: linear-gradient(135deg, #f8fbff 0%, #f0f7ff 100%);
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #0066cc;
}

.stat-card.pending {
  border-left-color: #ff9800;
}

.stat-card.approved {
  border-left-color: #4caf50;
}

.stat-card h3 {
  color: #0066cc;
  font-size: 28px;
  margin: 0 0 10px 0;
}

.stat-card p {
  color: #666;
  margin: 0;
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.filter-btn.active {
  border-color: #0066cc;
  color: #0066cc;
  background: #f0f7ff;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 51, 102, 0.1);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: linear-gradient(135deg, #0066cc 0%, #004ba3 100%);
  color: white;
}

.users-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
}

.users-table td {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.users-table tbody tr:hover {
  background: #f9f9f9;
}

.users-table tbody tr.approved {
  background: #f0fdf4;
}

.name {
  font-weight: 600;
  color: #2c3e50;
}

.email {
  color: #0066cc;
}

.status {
  text-align: center;
}

.badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
}

.badge.approved {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.pending {
  background: #fff3e0;
  color: #e65100;
}

.balance, .transfers, .date {
  text-align: center;
  color: #666;
}

.actions {
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-approve {
  background: #4caf50;
  color: white;
}

.btn-approve:hover {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-reject {
  background: #ff9800;
  color: white;
}

.btn-reject:hover {
  background: #e68900;
  transform: translateY(-2px);
}

.btn-reset {
  background: #2196f3;
  color: white;
}

.btn-reset:hover {
  background: #0b7dda;
  transform: translateY(-2px);
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover {
  background: #da190b;
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.no-users {
  padding: 40px;
  text-align: center;
  color: #999;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.spinner {
  font-size: 20px;
  color: #0066cc;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .users-table {
    font-size: 12px;
  }

  .users-table th,
  .users-table td {
    padding: 10px;
  }

  .stats {
    grid-template-columns: 1fr;
  }
}
```

---

## 3. API Client Helper

```javascript
// api/adminClient.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const adminAPI = {
  // Get all users
  getUsers: () => axios.get(`${API_BASE}/admin/users/`),

  // Get specific user
  getUser: (userId) => axios.get(`${API_BASE}/admin/users/${userId}/`),

  // Approve user (generates 15 transactions)
  approveUser: (userId) => 
    axios.post(`${API_BASE}/admin/users/${userId}/approve/`, { action: 'approve' }),

  // Reject user
  rejectUser: (userId) => 
    axios.post(`${API_BASE}/admin/users/${userId}/approve/`, { action: 'reject' }),

  // Reset transfer count
  resetTransfers: (userId) => 
    axios.post(`${API_BASE}/admin/users/${userId}/reset-transfers/`),

  // Delete user
  deleteUser: (userId) => 
    axios.post(`${API_BASE}/admin/users/${userId}/delete/`),

  // Auth
  signup: (data) => axios.post(`${API_BASE}/signup/`, data),
  login: (data) => axios.post(`${API_BASE}/login/`, data),
};

export default adminAPI;
```

---

## 4. Usage in Your App

```javascript
// App.jsx
import React from 'react';
import AdminDashboard from './components/AdminDashboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <AdminDashboard />
    </div>
  );
}

export default App;
```

---

## 5. Key Features in React Component

✅ **Real-time Updates** - Auto-refresh every 10 seconds
✅ **Filter Users** - Show all, pending, or approved
✅ **Quick Stats** - Show count of pending and approved
✅ **One-Click Approve** - Generates 15 transactions instantly
✅ **Reset Transfers** - Click button to reset transfer count
✅ **Delete Users** - Remove users completely
✅ **Responsive Design** - Works on mobile and desktop
✅ **User Feedback** - Alerts and visual indicators

---

## 6. Testing the React Component

1. Start Django server:
```bash
python manage.py runserver
```

2. Create admin:
```bash
python manage.py create_admin
```

3. Start React app:
```bash
npm start
```

4. Create test user at `/signup`

5. Go to Admin Dashboard

6. Click "Approve" on test user

7. Watch 15 transactions generate automatically!

---

**Your React Admin Dashboard is ready to build!** 🚀
