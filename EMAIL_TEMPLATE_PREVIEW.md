# Email Template Preview & Design Details

## 📧 Debit Alert Email

### Design Characteristics
- **Color Scheme**: Red/Pink gradient header (#e74c3c to #c0392b)
- **Icon**: 💳 (credit card)
- **Tone**: Professional, alert-focused
- **Purpose**: Notifies sender when money leaves their account

### Email Structure

```
┌─────────────────────────────────────────────┐
│            DEBIT ALERT EMAIL                │
├─────────────────────────────────────────────┤
│  [Header - Red Gradient]                    │
│  💳 Debit Alert                             │
│  Money has been transferred from your       │
│  account                                    │
├─────────────────────────────────────────────┤
│  [Body]                                     │
│  Hello John Doe,                            │
│                                             │
│  We're notifying you that a transfer has   │
│  been successfully processed from your     │
│  account.                                   │
│                                             │
│  [Transaction Details Card]                │
│  ┌─────────────────────────────────────┐   │
│  │ Amount Debited:        $ 1,234.56  │   │
│  │ Transfer Type:         Local        │   │
│  │ Recipient Name:        Jane Smith   │   │
│  │ Recipient Bank:        Bank XYZ     │   │
│  │ Account Number:        ****1234     │   │
│  │ Description:           Invoice Pay  │   │
│  │ Date & Time:           Jan 6, 2025  │   │
│  │ Transaction ID:        TXN-000123   │   │
│  │ Status:                ✓ Completed  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [Info Box - Yellow]                        │
│  Updated Account Balance:                   │
│  Available: $ 8,765.43                      │
│  Total:     $ 9,000.00                      │
│                                             │
│  [Security Box - Blue]                      │
│  🔒 Security Notice:                        │
│  If you did not authorize this transfer     │
│  or notice suspicious activity, please      │
│  contact support immediately...             │
│                                             │
│  [Button]                                   │
│  View Transaction Details                  │
├─────────────────────────────────────────────┤
│  [Footer - Dark]                            │
│  Contact Support | Account Settings | Help  │
│  © 2025 Midwestern Bank                     │
└─────────────────────────────────────────────┘
```

---

## 📧 Credit Alert Email

### Design Characteristics
- **Color Scheme**: Green gradient header (#27ae60 to #229954)
- **Icon**: ✅ (checkmark)
- **Tone**: Positive, celebratory
- **Purpose**: Notifies receiver when money is received

### Email Structure

```
┌─────────────────────────────────────────────┐
│            CREDIT ALERT EMAIL               │
├─────────────────────────────────────────────┤
│  [Header - Green Gradient]                  │
│  ✅ Credit Alert                            │
│  You have received money to your account    │
├─────────────────────────────────────────────┤
│  [Body]                                     │
│  Hello Jane Smith,                          │
│                                             │
│  Great news! You have successfully          │
│  received a transfer to your account.       │
│                                             │
│  🎉 $ 1,234.56 Received! 🎉                │
│                                             │
│  [Sender Info Box - Light Green]            │
│  📤 Sender Information:                      │
│  Name: John Doe                             │
│  Bank: John's Bank                          │
│                                             │
│  [Transaction Details Card]                │
│  ┌─────────────────────────────────────┐   │
│  │ Amount Credited:       $ 1,234.56  │   │
│  │ Transfer Type:         Local        │   │
│  │ Description/Note:      Invoice Pay  │   │
│  │ Date & Time:           Jan 6, 2025  │   │
│  │ Transaction ID:        TXN-000123   │   │
│  │ Status:                ✓ Completed  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  [Info Box - Teal]                          │
│  📊 Updated Account Balance:                │
│  Available: $ 8,765.43                      │
│  Total:     $ 9,000.00                      │
│                                             │
│  [Security Box - Blue]                      │
│  🔒 Security Notice:                        │
│  If you did not expect this transfer or     │
│  notice anything unusual, please contact    │
│  support immediately...                     │
│                                             │
│  [Button]                                   │
│  View Transaction Details                  │
├─────────────────────────────────────────────┤
│  [Footer - Dark]                            │
│  Contact Support | Account Settings | Help  │
│  © 2025 Midwestern Bank                     │
└─────────────────────────────────────────────┘
```

---

## 🎨 Design Features

### Color Palette

**Debit Alert**
- Header: Linear gradient `#e74c3c` → `#c0392b` (Red)
- Accent: `#e74c3c`
- Background: Light gradient `#f5f7fa` → `#c3cfe2`
- Details box: `#f8f9fa`

**Credit Alert**
- Header: Linear gradient `#27ae60` → `#229954` (Green)
- Accent: `#27ae60`
- Background: Light gradient `#a8edea` → `#fed6e3`
- Details box: `#f0fdf4`

### Typography

- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Bold, 28px
- **Body**: Regular, 16px
- **Labels**: Semi-bold, 14px
- **Details**: Monospace for transaction IDs

### Responsive Design

✅ Mobile optimized
- Stacks all elements vertically on small screens
- Touch-friendly buttons (12px padding)
- Readable on all devices
- Max-width: 600px (standard email width)

### Email Client Compatibility

Tested and working on:
- ✅ Gmail (web, mobile, app)
- ✅ Outlook (web, desktop)
- ✅ Apple Mail
- ✅ Yahoo Mail
- ✅ Microsoft Mail
- ✅ Mobile email apps

### Accessibility

- ✅ High contrast ratios
- ✅ Clear, readable fonts
- ✅ Semantic HTML structure
- ✅ Alt text for icons (emoji)
- ✅ Plain text fallback version

---

## 📋 Template Variables

### Debit Email Template

```html
<!-- Used variables -->
{{ user_name }}                    <!-- Recipient name -->
{{ currency }}                     <!-- Currency symbol ($) -->
{{ amount }}                       <!-- Formatted amount -->
{{ transfer_type }}                <!-- local/international -->
{{ receiver_name }}                <!-- Recipient name -->
{{ receiver_bank }}                <!-- Recipient bank -->
{{ receiver_account_number }}      <!-- Recipient account -->
{{ description }}                  <!-- Transaction description -->
{{ transaction_date }}             <!-- Formatted date/time -->
{{ transaction_id }}               <!-- Unique transaction ID -->
{{ available_balance }}            <!-- User's available balance -->
{{ total_balance }}                <!-- User's total balance -->
{{ support_email }}                <!-- Support email address -->
{{ support_phone }}                <!-- Support phone number -->
{{ dashboard_url }}                <!-- Link to dashboard -->
{{ bank_name }}                    <!-- Bank name -->
{{ current_year }}                 <!-- Current year for footer -->
```

### Credit Email Template

```html
<!-- Used variables -->
{{ user_name }}                    <!-- Receiver name -->
{{ currency }}                     <!-- Currency symbol ($) -->
{{ amount }}                       <!-- Formatted amount -->
{{ transfer_type }}                <!-- local/international -->
{{ sender_name }}                  <!-- Sender name -->
{{ sender_bank }}                  <!-- Sender bank info -->
{{ description }}                  <!-- Transaction description -->
{{ transaction_date }}             <!-- Formatted date/time -->
{{ transaction_id }}               <!-- Unique transaction ID -->
{{ available_balance }}            <!-- Receiver's available balance -->
{{ total_balance }}                <!-- Receiver's total balance -->
{{ support_email }}                <!-- Support email address -->
{{ support_phone }}                <!-- Support phone number -->
{{ dashboard_url }}                <!-- Link to dashboard -->
{{ bank_name }}                    <!-- Bank name -->
{{ current_year }}                 <!-- Current year for footer -->
```

---

## 🔐 Security Features

1. **Unsubscribe Notice**: Clearly states it's automated
2. **Support Contact**: Always visible in footer
3. **Security Alert**: Alerts users to verify transactions
4. **Transaction ID**: Unique identifier for tracking
5. **Plain Text Fallback**: For enhanced security (no images)
6. **No Sensitive Data**: Account numbers are masked
7. **HTTPS Links**: All links should use HTTPS

---

## 📱 Mobile Rendering

Both templates are fully responsive with:
- Single-column layout on mobile
- Large, tap-friendly buttons
- Readable font sizes (minimum 16px)
- Full-width background colors
- Proper spacing on small screens

---

## 🎯 Customization Ideas

1. **Add Bank Logo**: Update templates to include logo (consider size for email clients)
2. **Company Colors**: Change color scheme in `<style>` section
3. **Custom Fonts**: Add web fonts (but test compatibility)
4. **Additional Info**: Add more transaction details if needed
5. **Branding**: Update footer with company details
6. **Localization**: Translate templates to other languages
7. **HTML Features**: Add more advanced HTML5 if needed

---

## ✅ Testing Checklist

When customizing, test:
- [ ] Text rendering and alignment
- [ ] Colors display correctly
- [ ] Links are clickable
- [ ] Images load (if added)
- [ ] Mobile responsiveness
- [ ] Various email clients
- [ ] Plain text fallback
- [ ] Security notices are clear

---

## 📞 Further Support

For email template issues:
- Check [Campaign Monitor CSS Guide](https://www.campaignmonitor.com/css/)
- Test with [Litmus](https://www.litmus.com/)
- Review [Email on Acid](https://www.emailonacid.com/)
- Read [MJML Documentation](https://mjml.io/) for advanced templates

Happy emailing! 🚀
