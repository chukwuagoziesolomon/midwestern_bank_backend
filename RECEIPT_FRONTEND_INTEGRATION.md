**Receipt Frontend Integration Guide**

This document explains how to integrate the transfer receipt endpoints into your frontend. It covers endpoints, example requests, and a React modal implementation that lets users download or share receipts as HTML, PDF, or PNG.

**Overview**
- Backend endpoints provide three receipt formats for a completed transfer: HTML, PDF, and PNG.
- After a successful transfer POST, the API returns `receipt_urls` containing links to each format for the created transfer. Use those URLs in your modal.

**Backend Endpoints**
- POST `/api/transfers/` — create a transfer (existing endpoint). Request must include `user_id` (temporary auth method used in this project). Response includes `receipt_urls` on success.
  - Example success response excerpt:
    ```json
    {
      "message": "Transfer created successfully",
      "transfer": { /* transfer object */ },
      "receipt_urls": {
        "html": "https://HOST/api/transfers/123/receipt/?user_id=2",
        "pdf": "https://HOST/api/transfers/123/receipt/pdf/?user_id=2",
        "image": "https://HOST/api/transfers/123/receipt/image/?user_id=2"
      }
    }
    ```

- GET `/api/transfers/<id>/receipt/?user_id=<id>` — returns HTML receipt as downloadable `.html` file.
- GET `/api/transfers/<id>/receipt/pdf/?user_id=<id>` — returns PDF receipt (generated with `xhtml2pdf`).
- GET `/api/transfers/<id>/receipt/image/?user_id=<id>` — returns PNG receipt (generated with `imgkit` + external `wkhtmltoimage`).

**Install / Runtime Requirements**
- Python deps: run `pip install -r config/requirements.txt` to install `xhtml2pdf` and `imgkit`.
- `imgkit` requires the `wkhtmltoimage` binary (part of `wkhtmltopdf`). On Windows download the installer from the wkhtmltopdf site and ensure `wkhtmltoimage.exe` is on `PATH`.

Windows notes (wkhtmltoimage)
- Download from: https://wkhtmltopdf.org/downloads.html
- Add the folder containing `wkhtmltoimage.exe` to your PATH and restart your server/dev terminal.

**CORS & Auth notes**
- The backend currently uses `user_id` query/body param to associate requests. For production, replace this with proper authentication (JWT or session auth) and use `request.user` to avoid exposing user IDs.
- Ensure CORS allows your frontend origin if the frontend is served from a different host.

**Frontend: Modal flow (React)**
1. After successful POST `/api/transfers/`, read `receipt_urls` from the response and store them in state.
2. Show a modal that offers: Download PDF, Download Image, Open HTML, Share PDF/Image.

Example React modal component (minimal):
```jsx
import React from 'react';

function downloadUrl(url) {
  window.open(url, '_blank');
}

async function shareFile(url, filename, mime) {
  try {
    const r = await fetch(url, { credentials: 'include' });
    const blob = await r.blob();
    const file = new File([blob], filename, { type: mime });
    if (navigator.canShare && navigator.canShare({ files: [file] })) {
      await navigator.share({ files: [file], title: 'Transfer Receipt' });
      return;
    }
    // fallback: trigger download
    const link = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = link;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(link);
  } catch (err) {
    console.error('Share/download failed', err);
  }
}

export default function ReceiptModal({ open, onClose, receiptUrls }) {
  if (!open) return null;
  return (
    <div className="modal">
      <h3>Transfer Successful</h3>
      <p>Your transfer completed. Choose an option:</p>
      <div className="actions">
        <button onClick={() => downloadUrl(receiptUrls.pdf)}>Download PDF</button>
        <button onClick={() => downloadUrl(receiptUrls.image)}>Download Image</button>
        <button onClick={() => downloadUrl(receiptUrls.html)}>Open HTML</button>
        <button onClick={() => shareFile(receiptUrls.pdf, 'receipt.pdf', 'application/pdf')}>Share PDF</button>
        <button onClick={() => shareFile(receiptUrls.image, 'receipt.png', 'image/png')}>Share Image</button>
      </div>
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

Hints for integration
- Use `fetch` with `credentials: 'include'` or include auth headers if your API uses tokens.
- When calling `receipt_urls.pdf` or `receipt_urls.image`, opening the URL triggers a download in most browsers because the backend sets `Content-Disposition: attachment`.
- For mobile web sharing, prefer `shareFile()` which tries the Web Share API and falls back to download.

Example cURL (download PDF):
```bash
curl -o receipt.pdf "http://localhost:8000/api/transfers/123/receipt/pdf/?user_id=2"
```

**Testing & Troubleshooting**
- If PDF endpoint returns 500: check `xhtml2pdf` installed and server logs. If PDF creation fails for specific HTML, inspect rendered HTML by opening the HTML receipt first.
- If image endpoint returns 500: ensure `wkhtmltoimage.exe` is installed and on PATH (Windows). Check `imgkit` exceptions in server logs.
- CORS errors: add your frontend origin to `CORS_ALLOWED_ORIGINS` or use `CORS_ALLOW_ALL_ORIGINS=True` in a safe dev environment.

**Recommended improvements**
- Replace `user_id` param with proper auth (JWT/session). Remove user_id from query strings.
- Add server-side caching for generated PDFs/images if many downloads occur for the same transfer.
- Attach the PDF to the transfer confirmation email (server-side) if required.

File references
- Backend views: `bankapp/views.py`
- Routes: `bankapp/urls.py`
- Template: `bankapp/templates/receipts/transfer_receipt.html`
- Requirements: `config/requirements.txt`

Next steps I can do for you
- Create a ready-to-drop React modal component file in the repo.
- Add a small unit test for the PDF/image endpoints.
- Implement token-based auth and switch the endpoints to use `request.user`.

---
Document created by the dev assistant. Update this file as you change endpoints.
