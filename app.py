import os
import re
import html
import time
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import resend
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="WorkHive HQ • Outreach Campaign Dispatcher",
    page_icon="🍯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom WorkHive HQ Brand Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Georgia:ital,wght@0,400;0,700;1,400;1,700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* App Canvas */
    .stApp {
        background-color: #FAF6F0 !important;
        color: #1C1409 !important;
    }
    
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.015em;
        color: #1C1409;
    }
    
    h1, h2, h3, .serif-font {
        font-family: Georgia, 'Times New Roman', serif !important;
        color: #1C1409 !important;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: rgba(250, 246, 240, 0.9); backdrop-filter: blur(8px);}

    /* Top Brand Hero Header */
    .brand-hero {
        background: radial-gradient(circle at 10% 20%, rgba(243, 235, 221, 0.95) 0%, rgba(255, 255, 255, 0.98) 90%);
        border: 1px solid #EADCC9;
        border-radius: 20px;
        padding: 26px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 35px -10px rgba(73, 36, 16, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        overflow: hidden;
    }
    
    .brand-hero::before {
        content: "";
        position: absolute;
        top: -60px;
        left: -60px;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(212, 154, 61, 0.15) 0%, rgba(250, 246, 240, 0) 70%);
        pointer-events: none;
    }
    
    .brand-tag {
        display: inline-block;
        border: 1px solid #D4BFA6;
        background: #FAF5ED;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #492410;
        margin-bottom: 10px;
    }
    
    .brand-title {
        font-family: Georgia, serif !important;
        font-size: 28px !important;
        font-weight: 700;
        color: #1C1409 !important;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    
    .brand-title em {
        color: #936738;
        font-style: italic;
        font-family: Georgia, serif !important;
    }
    
    .brand-sub {
        font-size: 14px;
        color: #6B5B49;
        margin: 0;
        max-width: 650px;
        line-height: 1.5;
    }
    
    .brand-status-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #FEFAF7;
        border: 1px solid #C4A47A;
        padding: 8px 16px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        color: #492410;
        box-shadow: 0 2px 8px rgba(73, 36, 16, 0.05);
    }
    
    .status-honeycomb {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #D49A3D;
        box-shadow: 0 0 10px #D49A3D;
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.25); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }

    /* Metric Cards Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    
    .metric-card {
        background: #FEFAF7;
        border: 1px solid #E5D5C0;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px -4px rgba(73, 36, 16, 0.04);
        transition: transform 0.2s, border-color 0.2s;
    }
    
    .metric-card:hover {
        border-color: #C4A47A;
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 11.5px;
        font-weight: 700;
        color: #7A6956;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-family: Georgia, serif !important;
        font-size: 24px;
        font-weight: 700;
        color: #492410;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #936738;
        font-weight: 500;
        margin-top: 2px;
    }

    /* Form & Section Containers */
    .section-header {
        font-family: Georgia, serif !important;
        font-size: 18px;
        font-weight: 700;
        color: #492410 !important;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .banner-badge {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #F4ECE1;
        border: 1px solid #C4A47A;
        border-left: 4px solid #492410;
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 18px;
        font-size: 13.5px;
        color: #492410;
    }

    /* Compose & Preview Box */
    .mail-client-header {
        background: #492410;
        color: #FEFAF7;
        border-radius: 14px 14px 0 0;
        padding: 14px 20px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        font-size: 13px;
    }
    
    .mail-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .mail-label {
        color: #D4BFA6;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 0.05em;
        min-width: 60px;
    }
    
    .mail-val {
        color: #FEFAF7;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 8px;
        border-radius: 6px;
    }

    /* Brand Primary Action Button */
    .send-action>button {
        background: #492410 !important;
        color: #FEFAF7 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 14px 30px !important;
        border-radius: 9999px !important;
        border: 1px solid #2D1407 !important;
        box-shadow: 0 4px 18px rgba(73, 36, 16, 0.25) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .send-action>button:hover {
        background: #3A1A0B !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(73, 36, 16, 0.35) !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 2px solid #EADCC9;
        padding-bottom: 4px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 9999px;
        padding: 8px 20px;
        font-size: 13.5px;
        font-weight: 600;
        color: #6B5B49;
        background-color: transparent;
        border: 1px solid transparent;
        transition: all 0.15s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: #FEFAF7 !important;
        background: #492410 !important;
        border: 1px solid #492410 !important;
        box-shadow: 0 2px 8px rgba(73, 36, 16, 0.15) !important;
    }
    
    /* Inputs Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #D8C7B0 !important;
        color: #1C1409 !important;
        font-size: 14px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #492410 !important;
        box-shadow: 0 0 0 2px rgba(73, 36, 16, 0.15) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F3EBDD !important;
        border-right: 1px solid #E2D2BC !important;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #492410 !important;
    }
</style>
""", unsafe_allow_html=True)

# Templates Path
TEMPLATES_DIR = Path(__file__).parent / "templates"
CLEAN_TEMPLATE_PATH = TEMPLATES_DIR / "clean_1to1_template.html"
RICH_TEMPLATE_PATH = TEMPLATES_DIR / "email_template.html"

DEFAULT_PLAIN_TEMPLATE = """Hi {{first_name}},

I'll keep this short. Running {{company}} remotely means your team is spread across a dozen apps — chat in one, tasks in another, HR and payroll somewhere else — and the one thing that used to make work feel like work, the office, is gone.

Ten subscriptions. Ten logins. Ten bills. And a team that still feels scattered and out of sync.

We built WorkHive HQ to fix both.

It's a walkable 3D office your team lives in — walk up to a colleague and just talk, no link, no invite — plus your entire back office, built in. One login, one system, one bill.

✓ 3D office with proximity voice, meeting rooms & focus booths
✓ Full HR — recruitment, onboarding, leave & records
✓ Finance, invoicing, expenses & a real payroll engine
✓ Tasks, tickets with SLAs, OKRs, rota & recognition
✓ Zero-knowledge encrypted docs & role-based access

Spatial tools give you a room but nothing to run the business. HR platforms run the business but have no office. WorkHive HQ is the only one that's both — at one flat price with unlimited seats. Grow the team without growing the invoice.

See it live in 2 minutes: https://www.workhivehq.com/

Or just reply to this email and I'll send you a quick walkthrough — no pressure, no sales call.

Warmly,
Tooba Akram
Co-Founder, WorkHive HQ
workhivehq.com"""

def load_template(template_type="clean"):
    path = CLEAN_TEMPLATE_PATH if template_type == "clean" else RICH_TEMPLATE_PATH
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "<p>Hi {{first_name}},</p>"

def render_email_template(template_str, merge_data, signature_data=None):
    rendered = template_str
    for key, val in merge_data.items():
        placeholder = f"{{{{{key}}}}}"
        rendered = rendered.replace(placeholder, str(val if val is not None else ""))
        
    if signature_data:
        if "founder_name" in signature_data and signature_data["founder_name"]:
            name = signature_data["founder_name"]
            rendered = re.sub(r'<strong>(Muhammad Saad bin Mazhar|Tooba Akram)</strong>', f'<strong>{html.escape(name)}</strong>', rendered)
            rendered = re.sub(r'<p style="[^"]*font-weight: 700;[^"]*">(Muhammad Saad bin Mazhar|Tooba Akram)</p>', f'<p style="margin: 0 0 2px 0; font-weight: 700; color: #111111; font-size: 15px;">{html.escape(name)}</p>', rendered)
        
        if "founder_title" in signature_data and signature_data["founder_title"]:
            title = signature_data["founder_title"]
            rendered = re.sub(r'<span style="color:#492410;">(Founder|Co-Founder), WorkHive HQ</span>', f'<span style="color:#492410;">{html.escape(title)}</span>', rendered)
            rendered = re.sub(r'<p style="[^"]*color: #555555;[^"]*">(Founder|Co-Founder), WorkHive HQ</p>', f'<p style="margin: 0 0 4px 0; color: #555555; font-size: 14px;">{html.escape(title)}</p>', rendered)
            
    return rendered

if "send_history" not in st.session_state:
    st.session_state.send_history = []

if "editable_plain_text" not in st.session_state or "unsubscribe" in st.session_state.editable_plain_text.lower():
    st.session_state.editable_plain_text = DEFAULT_PLAIN_TEMPLATE

# ----------------- TOP WORKHIVE HQ HERO HEADER -----------------
st.markdown("""
<div class="brand-hero">
    <div>
        <div class="brand-tag">THE VIRTUAL OFFICE OPERATING SYSTEM</div>
        <h1 class="brand-title">Your company, <em>as a place.</em></h1>
        <p class="brand-sub">A walkable 3D office where your team actually works — with HR, finance, tasks, and cold outreach in one unified system.</p>
    </div>
    <div class="brand-status-pill">
        <div class="status-honeycomb"></div>
        <span>Resend API Active • <strong>workhivehq.online</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- METRICS DASHBOARD RIBBON -----------------
total_sent = len([x for x in st.session_state.send_history if x.get("status") == "Delivered"])
failed_sent = len([x for x in st.session_state.send_history if "Failed" in x.get("status", "")])
success_rate = "100%" if (total_sent + failed_sent == 0) else f"{(total_sent / (total_sent + failed_sent) * 100):.1f}%"

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Total Outbound Dispatched</div>
        <div class="metric-value">{total_sent}</div>
        <div class="metric-sub">Session Messages</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Delivery Success Rate</div>
        <div class="metric-value">{success_rate}</div>
        <div class="metric-sub">Resend SLA High</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Verified Outbound Domain</div>
        <div class="metric-value" style="font-size: 17px; line-height: 28px;">workhivehq.online</div>
        <div class="metric-sub">DKIM & SPF Verified</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Deliverability Engine</div>
        <div class="metric-value" style="font-size: 17px; line-height: 28px;">Primary Inbox Optimized</div>
        <div class="metric-sub">Anti-Promotions Active</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: CONFIGURATION -----------------
with st.sidebar:
    st.markdown("### ⚙️ Dispatch Settings")
    
    default_key = os.getenv("RESEND_API_KEY", "re_XXngPNv1_JaAiWRJFmy8UvhCQPuywSewN")
    api_key = st.text_input("Resend API Key", value=default_key, type="password", help="Authenticated Resend secret key")
    
    st.markdown("---")
    st.markdown("### 📤 Sender Identity")
    sender_mode = st.radio(
        "Sender Source:",
        ["WorkHive Online (tooba@workhivehq.online)", "Resend Sandbox (Testing)", "Custom Address"],
        index=0
    )
    
    if sender_mode == "WorkHive Online (tooba@workhivehq.online)":
        sender_address = "WorkHive HQ <tooba@workhivehq.online>"
    elif sender_mode == "Resend Sandbox (Testing)":
        sender_address = "WorkHive HQ <onboarding@resend.dev>"
    else:
        sender_address = st.text_input("Custom Sender Email", value="WorkHive HQ <tooba@workhivehq.online>")
        
    reply_to = st.text_input("Reply-To Address", value=os.getenv("DEFAULT_REPLY_TO", "tooba@workhivehq.online"))
    
    st.markdown("---")
    st.markdown("### 🎯 Dispatch Protocol")
    format_mode = st.radio(
        "Payload Type:",
        [
            "Pure Plain-Text (Maximum Deliverability / No HTML)",
            "Inbox-Optimized Clean HTML (Clean 1-to-1)",
            "Marketing Card (Rich HTML Design)"
        ],
        index=0
    )

# ----------------- MAIN NAVIGATION TABS -----------------
tab_single, tab_batch, tab_history, tab_guide = st.tabs([
    "🚀 Single Dispatch",
    "📑 Batch Campaign Dispatch",
    "📜 Outbound Delivery Logs",
    "💡 Deliverability Strategy"
])

base_html_template = load_template("clean" if "Clean" in format_mode else "rich")

# ----------------- TAB 1: SINGLE DISPATCH -----------------
with tab_single:
    if "Plain-Text" in format_mode:
        st.markdown("""
        <div class="banner-badge">
            <span>🛡️</span>
            <div><strong>Pure Plain-Text Protocol Active:</strong> Sending raw human format with zero tracking/promotional wrappers to prioritize landing in <strong>Primary Inbox</strong>.</div>
        </div>
        """, unsafe_allow_html=True)
    elif "Clean" in format_mode:
        st.markdown("""
        <div class="banner-badge">
            <span>✨</span>
            <div><strong>Inbox-Optimized HTML Active:</strong> Clean 1-to-1 typography styled without promotional tables.</div>
        </div>
        """, unsafe_allow_html=True)
        
    col_inputs, col_editor = st.columns([1.05, 1.35], gap="large")
    
    with col_inputs:
        st.markdown("""<div class="section-header">1. Recipient Information</div>""", unsafe_allow_html=True)
        rec_email = st.text_input("Recipient Email Address *", placeholder="saad@opatrip.com", key="single_rec_email")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            first_name = st.text_input("First Name ({{first_name}})", value="Saad")
        with col_m2:
            company_name = st.text_input("Company ({{company}})", value="Alfursan")
            
        st.markdown("""<div class="section-header" style="margin-top: 20px;">2. Subject Line</div>""", unsafe_allow_html=True)
        subject_options = [
            "We replaced 10 tools with one virtual office",
            f"{company_name}'s whole company, in one place",
            "The office your remote team lost — rebuilt",
            "Custom Subject..."
        ]
        chosen_subject_type = st.selectbox("Subject Line Preset", subject_options, index=0)
        
        if chosen_subject_type == "Custom Subject...":
            subject_line = st.text_input("Enter Custom Subject Line", value="We replaced 10 tools with one virtual office")
        else:
            subject_line = chosen_subject_type
            
        merge_dict = {
            "first_name": first_name,
            "company": company_name
        }
        
        st.markdown("<div style='margin-top: 26px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="send-action">', unsafe_allow_html=True)
        send_clicked = st.button("Start your outreach →", key="send_single_btn", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_editor:
        st.markdown("""<div class="section-header">3. Compose & Live Message Editor</div>""", unsafe_allow_html=True)
        
        # Meta chips
        st.markdown(f"""
        <div class="mail-client-header">
            <div class="mail-row">
                <span class="mail-label">FROM</span>
                <span class="mail-val">{html.escape(sender_address)}</span>
            </div>
            <div class="mail-row">
                <span class="mail-label">TO</span>
                <span class="mail-val">{html.escape(rec_email or 'saad@opatrip.com')}</span>
            </div>
            <div class="mail-row">
                <span class="mail-label">SUBJECT</span>
                <span class="mail-val">{html.escape(subject_line)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_ed_bar1, col_ed_bar2 = st.columns([3, 1])
        with col_ed_bar1:
            st.caption("✏️ You can edit the text directly below before dispatching:")
        with col_ed_bar2:
            if st.button("🔄 Reset Text", help="Restore default template text"):
                st.session_state.editable_plain_text = DEFAULT_PLAIN_TEMPLATE
                st.rerun()

        if "Plain-Text" in format_mode:
            edited_plain_body = st.text_area(
                "Email Body",
                value=st.session_state.editable_plain_text,
                height=480,
                label_visibility="collapsed",
                help="Edit your cold outreach text here. Dynamic tags like {{first_name}} and {{company}} will be replaced."
            )
            st.session_state.editable_plain_text = edited_plain_body
            
            # Apply dynamic merge replacement
            final_plain_content = edited_plain_body
            for k, v in merge_dict.items():
                final_plain_content = final_plain_content.replace(f"{{{{{k}}}}}", str(v))
                
            with st.expander("👁️ Final Rendered Output (What Recipient Sees)", expanded=False):
                st.text(final_plain_content)
        else:
            preview_tab1, preview_tab2 = st.tabs(["📱 Rendered Email Preview", "💻 HTML Code"])
            rendered_html = render_email_template(base_html_template, merge_dict)
            with preview_tab1:
                components.html(rendered_html, height=650, scrolling=True)
            with preview_tab2:
                edited_html_content = st.text_area("Raw HTML", value=rendered_html, height=450)
                rendered_html = edited_html_content

        if send_clicked:
            if not api_key:
                st.error("❌ Resend API Key is missing. Please configure it in the sidebar.")
            elif not rec_email or "@" not in rec_email:
                st.error("❌ Please provide a valid recipient email address.")
            elif not subject_line:
                st.error("❌ Subject line cannot be empty.")
            else:
                resend.api_key = api_key.strip()
                
                params = {
                    "from": sender_address.strip(),
                    "to": [rec_email.strip()],
                    "subject": subject_line.strip()
                }
                
                if "Plain-Text" in format_mode:
                    params["text"] = final_plain_content
                else:
                    params["html"] = rendered_html
                    params["text"] = final_plain_content if 'final_plain_content' in locals() else ""
                    
                if reply_to.strip():
                    params["reply_to"] = reply_to.strip()
                
                with st.spinner("Connecting to Resend infrastructure & dispatching..."):
                    try:
                        response = resend.Emails.send(params)
                        email_id = response.get("id") if isinstance(response, dict) else getattr(response, "id", str(response))
                        
                        st.success(f"✅ Dispatched successfully to **{rec_email}** (Resend ID: `{email_id}`)")
                        st.balloons()
                        
                        st.session_state.send_history.append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "to": rec_email,
                            "subject": subject_line,
                            "sender": sender_address,
                            "format": format_mode,
                            "status": "Delivered",
                            "resend_id": email_id
                        })
                    except Exception as e:
                        err_msg = str(e)
                        st.error(f"❌ Delivery error: {err_msg}")
                        st.session_state.send_history.append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "to": rec_email,
                            "subject": subject_line,
                            "sender": sender_address,
                            "format": format_mode,
                            "status": f"Failed: {err_msg}",
                            "resend_id": "-"
                        })

# ----------------- TAB 2: BATCH CAMPAIGN DISPATCH -----------------
with tab_batch:
    st.markdown("""<div class="section-header">Batch Leads Upload & Queue</div>""", unsafe_allow_html=True)
    st.markdown("Upload a CSV list of leads with columns: `email`, `first_name`, `company`.")
    
    sample_csv = """email,first_name,company
saad@alfursan.com,Saad,Alfursan
alex@nexusflow.io,Alex,NexusFlow
david@cloudscale.net,David,CloudScale"""

    batch_file = st.file_uploader("Upload CSV Lead File", type=["csv"])
    
    if batch_file is not None:
        try:
            df_leads = pd.read_csv(batch_file)
        except Exception as err:
            st.error(f"Error reading CSV: {err}")
            df_leads = None
    else:
        st.caption("Or test with pre-loaded mock leads:")
        use_sample = st.checkbox("Load Sample Leads Dataset", value=True)
        if use_sample:
            import io
            df_leads = pd.read_csv(io.StringIO(sample_csv))
        else:
            df_leads = None

    if df_leads is not None:
        st.dataframe(df_leads, use_container_width=True)
        
        col_b1, col_b2 = st.columns([2, 1])
        with col_b1:
            batch_subject_tpl = st.text_input(
                "Batch Subject Template (Supports `{{company}}`)",
                value="We replaced 10 tools with one virtual office"
            )
        with col_b2:
            batch_delay = st.slider("Throttle Delay (sec between sends)", 0.2, 5.0, 1.0, 0.1, help="Prevents rate limits and warming triggers")
        
        st.markdown('<div class="send-action">', unsafe_allow_html=True)
        if st.button("Start batch campaign →", key="send_batch_btn"):
            if not api_key:
                st.error("❌ Resend API Key is missing.")
            else:
                resend.api_key = api_key.strip()
                progress_bar = st.progress(0)
                status_text = st.empty()
                total = len(df_leads)
                success_count = 0
                
                for idx, row in df_leads.iterrows():
                    lead_email = str(row.get("email", "")).strip()
                    lead_fn = str(row.get("first_name", ""))
                    lead_comp = str(row.get("company", ""))
                    
                    if not lead_email or "@" not in lead_email:
                        continue
                        
                    lead_merge = {
                        "first_name": lead_fn,
                        "company": lead_comp
                    }
                    
                    lead_subject = batch_subject_tpl.replace("{{company}}", lead_comp)
                    
                    # Apply plain text replacement
                    lead_plain = st.session_state.editable_plain_text
                    for k, v in lead_merge.items():
                        lead_plain = lead_plain.replace(f"{{{{{k}}}}}", str(v))
                        
                    lead_html = render_email_template(base_html_template, lead_merge)
                    
                    params = {
                        "from": sender_address.strip(),
                        "to": [lead_email],
                        "subject": lead_subject
                    }
                    
                    if "Plain-Text" in format_mode:
                        params["text"] = lead_plain
                    else:
                        params["html"] = lead_html
                        params["text"] = lead_plain
                        
                    if reply_to.strip():
                        params["reply_to"] = reply_to.strip()
                        
                    status_text.text(f"⚡ Dispatching ({idx + 1}/{total}) to {lead_email}...")
                    try:
                        res = resend.Emails.send(params)
                        res_id = res.get("id") if isinstance(res, dict) else getattr(res, "id", str(res))
                        success_count += 1
                        st.session_state.send_history.append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "to": lead_email,
                            "subject": lead_subject,
                            "sender": sender_address,
                            "format": format_mode,
                            "status": "Delivered",
                            "resend_id": res_id
                        })
                    except Exception as ex:
                        st.session_state.send_history.append({
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "to": lead_email,
                            "subject": lead_subject,
                            "sender": sender_address,
                            "format": format_mode,
                            "status": f"Failed: {str(ex)}",
                            "resend_id": "-"
                        })
                    
                    progress_bar.progress((idx + 1) / total)
                    time.sleep(batch_delay)
                    
                status_text.success(f"✅ Batch queue complete! Successfully delivered {success_count}/{total} emails.")
        st.markdown('</div>', unsafe_allow_html=True)



# ----------------- TAB 3: DELIVERY LOGS -----------------
with tab_history:
    st.markdown("""<div class="section-header">Outbound Dispatch Audit Logs</div>""", unsafe_allow_html=True)
    if st.session_state.send_history:
        df_hist = pd.DataFrame(st.session_state.send_history)
        st.dataframe(df_hist, use_container_width=True)
        col_log1, col_log2 = st.columns([1, 4])
        with col_log1:
            if st.button("🗑️ Clear Audit Logs"):
                st.session_state.send_history = []
                st.rerun()
    else:
        st.info("No outbound emails recorded in this session yet.")

# ----------------- TAB 4: DELIVERABILITY GUIDE -----------------
with tab_guide:
    st.markdown("""<div class="section-header">Primary Inbox Deliverability Strategy</div>""", unsafe_allow_html=True)
    st.markdown("""
    ### Key Principles for B2B Cold Outreach:
    1. **Pure Plain-Text (Recommended for Sales Outreach)**:
       * By bypassing marketing CSS/tables and `List-Unsubscribe` triggers, plain-text emails receive up to **3.2x higher reply rates**.
    2. **Domain Authentication Checklist**:
       * ✅ SPF configured (`v=spf1 include:resend.com ~all`)
       * ✅ DKIM signed & verified
       * ✅ DMARC policy active (`v=DMARC1; p=none;`)
    3. **Warm-up Best Practice**:
       * When sending to a new contact, keep the first follow-up short and conversational to encourage an initial reply.
    """)
