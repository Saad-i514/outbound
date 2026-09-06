# WorkHive HQ — Email Campaign Sender

A specialized, high-converting cold email sender built with Streamlit, HTML email rendering, and the Resend API.

## Features

- **Real-Time HTML Preview**: Renders the complete, responsive WorkHive HQ email template inside Streamlit.
- **Dynamic Merge Tags**: Customizes `{{first_name}}`, `{{company}}`, `{{unsubscribe_url}}` instantly.
- **A/B Testing Subject Presets**: Quick access to top-performing subject lines or custom options.
- **Resend Integration**: Seamless delivery via Resend API with real-time error diagnostics and ID tracking.
- **Single & Batch Dispatch**: Send individual outreach emails or dispatch campaigns from CSV.
- **Delivery Logs**: Track outbound email statuses, timestamps, and message IDs.

---

## Quick Start

### 1. Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Run the Streamlit Application
```powershell
streamlit run app.py
```
*(Or run using the venv python directly: `.\venv\Scripts\streamlit.exe run app.py`)*

### 3. Open in Browser
The app will launch automatically at `http://localhost:8501`.
