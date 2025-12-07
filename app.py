import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timezone

import plotly.express as px

# =========================
# CONFIG
# =========================

API_URL = "https://n8n.srv1179649.hstgr.cloud/webhook/qx-dashboard-live"  # <-- YOUR n8n URL

st.set_page_config(
    page_title="Qubic Guardian – Real-Time Risk Dashboard",
    page_icon="🛡",
    layout="wide",
)

# CSS theme
st.markdown(
    """
    <style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #050816 0%, #020617 40%, #020617 100%);
        color: #f9fafb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #050816;  /* deeper, richer background */
        padding-top: 18px;
        padding-bottom: 18px;
        padding-left: 10px;
        padding-right: 10px;
        border-right: 1px solid rgba(15, 23, 42, 0.85);
        box-shadow: 6px 0 24px rgba(0, 0, 0, 0.75);
        min-width: 250px;
        max-width: 250px;   /* compact like Infinity */
    }

    /* Sidebar logo wrapper */
    .sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 16px;
        padding: 6px 10px 2px 6px;
        border-radius: 14px;
        background: radial-gradient(circle at top left, #111827 0%, #020617 60%);
    }

    /* “Dashboard view” heading */
    section[data-testid="stSidebar"] h3 {
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 10px;
        margin-top: 6px;
    }

    /* Sidebar nav like Infinity */
    .sidebar-nav [data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .sidebar-nav [data-testid="stRadio"] > div[role="radiogroup"]
        > label[data-baseweb="radio"] {
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid transparent;
        background: transparent;
        cursor: pointer;
        display: flex;
        align-items: center;
        transition: all 0.15s ease-in-out;
    }

    .sidebar-nav [data-testid="stRadio"] > div[role="radiogroup"]
        > label[data-baseweb="radio"]:hover {
        background: rgba(15, 23, 42, 0.95);
        border-color: rgba(148, 163, 184, 0.55);
    }

    /* Active (selected) nav like purple Infinity highlight */
    .sidebar-nav [data-testid="stRadio"] > div[role="radiogroup"]
        > label[data-baseweb="radio"][aria-checked="true"] {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-color: transparent;
        box-shadow: 0 0 0 1px rgba(15, 23, 42, 0.8);
        color: #f9fafb;
    }

    .sidebar-nav [data-testid="stRadio"] > div[role="radiogroup"]
        > label[data-baseweb="radio"][aria-checked="true"] p {
        color: #f9fafb !important;
        font-weight: 600;
    }

    /* Radio label text — bigger and clearer */
    .sidebar-nav [data-testid="stRadio"] p {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        margin-bottom: 0;
        letter-spacing: 0.15px;
}


    /* Subtle divider between nav and filters */
    section[data-testid="stSidebar"] hr {
        border: none;
        border-top: 1px solid rgba(31, 41, 55, 0.9);
        margin: 14px 0 10px 0;
    }


    /* Metrics */
    .big-metric {
        font-size: 32px !important;
        font-weight: 800 !important;
    }
    .metric-label {
        font-size: 12px !important;
        color: #9ca3af !important;
        text-transform: uppercase;
        letter-spacing: 0.14em;
    }
    .metric-sub {
        font-size: 12px !important;
        color: #6b7280 !important;
    }

    /* Risk badges */
    .risk-badge-high {
        background-color: #ef444433;
        color: #f97373;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
    }
    .risk-badge-medium {
        background-color: #facc1533;
        color: #fde047;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
    }
    .risk-badge-low {
        background-color: #22c55e33;
        color: #4ade80;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
    }

    /* Cards */
    .card,
    .card-soft {
        border-radius: 0;
        padding: 0;
        background: transparent;
        border: none;
        box-shadow: none;
    }
        
    /* ---- Premium Chart Card Styling (tight fit) ---- */
    div[data-testid="stPlotlyChart"] {
        border-radius: 18px;                    /* rounded corners */
        overflow: hidden;                       /* clip chart to radius */
        padding: 0;                             /* no inner padding */
        background: linear-gradient(145deg,
            #0b1120 0%,
            #111827 50%,
            #0f172a 100%
        );
        border: 1px solid rgba(148, 163, 184, 0.12);
        box-shadow:
            0 12px 28px rgba(0, 0, 0, 0.45),
            inset 0 0 20px rgba(255, 255, 255, 0.02);
        margin-bottom: 22px;
        transition: all 0.25s ease-in-out;
    }

    div[data-testid="stPlotlyChart"]:hover {
        transform: translateY(-3px);
        box-shadow:
            0 16px 32px rgba(0, 0, 0, 0.55),
            inset 0 0 25px rgba(255, 255, 255, 0.03);
    }


    /* Hover effect (premium look) */
    div[data-testid="stPlotlyChart"]:hover {
        transform: translateY(-3px);
        box-shadow: 
            0 16px 32px rgba(0, 0, 0, 0.55),
            inset 0 0 25px rgba(255, 255, 255, 0.03);
    }


    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .section-caption {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 10px;
    }

    /* Sidebar nav like figma reference */
    .sidebar-nav label > div:first-child {
        border-radius: 12px;
        padding: 6px 10px;
        border: 1px solid transparent;
        transition: all 0.15s ease-in-out;
        background: transparent;
    }
    .sidebar-nav label > div:first-child:hover {
        border-color: rgba(148, 163, 184, 0.6);
        background: rgba(15, 23, 42, 0.9);
    }
    .sidebar-nav label input:checked + div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-color: transparent;
        color: #f9fafb;
        box-shadow: 0 0 0 1px rgba(15, 23, 42, 0.6);
    }

    /* Hide default radio label text (we add our own) */
    .sidebar-nav > div > label p {
        font-weight: 500;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# DATA LOADING
# =========================


@st.cache_data(ttl=30)
def load_data():
    """Fetch data from n8n webhook and return as cleaned DataFrame."""
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict):
        if "data" in data:
            data = data["data"]
        elif "rows" in data:
            data = data["rows"]

    df = pd.DataFrame(data)
    if df.empty:
        return df

    df.columns = [c.strip() for c in df.columns]

    # Timestamp
    if "timestamp_raw" in df.columns:
        ts = pd.to_numeric(df["timestamp_raw"], errors="coerce")
        if ts.dropna().gt(10**10).any():
            df["timestamp"] = pd.to_datetime(ts, unit="ms", utc=True)
        else:
            df["timestamp"] = pd.to_datetime(ts, unit="s", utc=True)
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    else:
        df["timestamp"] = pd.NaT

    # Numeric cols
    num_cols = [
        "shares",
        "price_qubic",
        "qubic_price_usd",
        "trade_value_qub",
        "trade_value_usdt",
        "risk_score",
        "risk_score_anamoly",
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # String cols
    str_cols = [
        "asset",
        "side",
        "direction",
        "risk_level",
        "risk_level_anamoly",
        "risk_tags_anamoly",
    ]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Derived flags
    df["is_whale_value"] = df["trade_value_usdt"].fillna(0) >= 500
    df["is_whale_shares"] = df["shares"].fillna(0) >= 1_000_000
    df["is_whale"] = df["is_whale_value"] | df["is_whale_shares"]

    df["has_anomaly"] = df["risk_level_anamoly"].isin(["MEDIUM", "HIGH"])

    if df["timestamp"].notna().any():
        df["date"] = df["timestamp"].dt.date
        df["hour_bucket"] = df["timestamp"].dt.floor("H")
    else:
        df["date"] = pd.NaT
        df["hour_bucket"] = pd.NaT

    df["effective_risk"] = df["risk_level_anamoly"].where(
        df["risk_level_anamoly"].notna() & (df["risk_level_anamoly"] != ""),
        df["risk_level"],
    )

    df = df.sort_values("timestamp", ascending=False)

    return df


# =========================
# FILTERS
# =========================


def sidebar_filters(df: pd.DataFrame):
    """Render filters INSIDE an existing st.sidebar context, return filtered df."""
    st.subheader("🔍 Filter trades")

    if df.empty:
        st.info("No data yet. Wait for Qubic trades to arrive.")
        return df

    # --- Asset dropdown with 'All' ---
    assets = sorted(df["asset"].dropna().unique().tolist())
    asset_options = ["All"] + assets
    selected_asset = st.selectbox(
        "Assets (tokens)",
        options=asset_options,
        index=0,   # "All" by default
    )

    # --- Direction dropdown ---
    directions = sorted(df["direction"].dropna().unique().tolist())
    directions_display = ["All"] + [d.capitalize() for d in directions]
    direction_choice = st.selectbox("Direction", directions_display, index=0)

    # --- Risk dropdown ---
    risk_options = ["All", "High", "Medium", "Low", "Only anomalies"]
    selected_risk = st.selectbox("Risk view", risk_options, index=0)

    # --- Sliders ---
    max_val = float(df["trade_value_usdt"].max() or 0)
    min_val_filter = st.slider(
        "Minimum trade value (USDT)",
        min_value=0.0,
        max_value=round(max(max_val, 10.0), 2),
        value=0.0,
        step=0.5,
    )

    if df["timestamp"].notna().any():
        max_hours = 48
        hours_back = st.slider(
            "Lookback window (hours)",
            min_value=1,
            max_value=max_hours,
            value=24,
        )
        cutoff = pd.Timestamp.now(timezone.utc) - pd.Timedelta(hours=hours_back)
        df = df[df["timestamp"] >= cutoff]

    # ---------- APPLY FILTERS ----------

    # Asset filter
    if selected_asset != "All":
        df = df[df["asset"] == selected_asset]

    # Direction filter
    if direction_choice != "All":
        df = df[df["direction"].str.lower() == direction_choice.lower()]

    # Min value filter
    df = df[df["trade_value_usdt"].fillna(0) >= min_val_filter]

    # Risk filter
    if selected_risk == "Only anomalies":
        df = df[df["has_anomaly"]]
    elif selected_risk in ["High", "Medium", "Low"]:
        df = df[df["effective_risk"].str.upper() == selected_risk.upper()]

    return df



# =========================
# HEADER
# =========================


def render_header():
    st.markdown(
        """
        <div style="padding: 4px 0 4px 0;">
            <h2
                style="
                    margin: 0;
                    font-size: 40px;
                    font-weight: 600;
                    text-align: left;
                "
            >
                Real-Time Risk & Liquidity Dashboard
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )




# =========================
# KPI SECTION
# =========================


def render_overview_kpis(df: pd.DataFrame):

    if df.empty:
        st.markdown(
            '<div class="section-title">Network status</div>'
            '<div class="section-caption">Waiting for live trades in the selected window.</div>',
            unsafe_allow_html=True,
        )
        st.info("No trades found. Trigger some transactions and click **Refresh**.")
        return

    total_trades = len(df)
    total_volume = df["trade_value_usdt"].sum()
    unique_assets = df["asset"].nunique()

    whale_trades = df[df["is_whale"]]
    whale_share = len(whale_trades) / total_trades * 100 if total_trades else 0

    anomalies = df[df["has_anomaly"]]
    anomaly_share = len(anomalies) / total_trades * 100 if total_trades else 0

    if df["date"].notna().any():
        by_date = (
            df.groupby("date")["trade_value_usdt"].sum().sort_index(ascending=True)
        )
        today_vol = by_date.iloc[-1]
        prev_vol = by_date.iloc[-2] if len(by_date) > 1 else 0
        vol_change = ((today_vol - prev_vol) / prev_vol * 100) if prev_vol > 0 else np.nan
    else:
        vol_change = np.nan

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-label">Total Trades</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="big-metric">{total_trades:,}</div>',
            unsafe_allow_html=True,
        )
        # st.markdown(
        #     '<div class="metric-sub">Executed in selected time window</div>',
        #     unsafe_allow_html=True,
        # )

    with col2:
        st.markdown(
            '<div class="metric-label">Total Volume (USDT)</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="big-metric">${total_volume:,.2f}</div>',
            unsafe_allow_html=True,
        )
        subtitle = "No prior day for comparison"
        if not np.isnan(vol_change):
            arrow = "▲" if vol_change >= 0 else "▼"
            subtitle = f"{arrow} {vol_change:+.1f}% vs previous day"
        st.markdown(
            f'<div class="metric-sub">{subtitle}</div>',
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            '<div class="metric-label">Unique Assets</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="big-metric">{unique_assets:,}</div>',
            unsafe_allow_html=True,
        )
        # st.markdown(
        #     '<div class="metric-sub">Actively traded in this window</div>',
        #     unsafe_allow_html=True,
        # )

    with col4:
        st.markdown(
            '<div class="metric-label">Whales & Anomalies</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="big-metric">{whale_share:.1f}% · {anomaly_share:.1f}%</div>',
            unsafe_allow_html=True,
        )
        # st.markdown(
        #     '<div class="metric-sub">Share of high-impact or suspicious trades</div>',
        #     unsafe_allow_html=True,
        # )



# =========================
# RISK BADGE
# =========================


def risk_badge(level: str) -> str:
    lvl = (level or "").upper()
    if lvl == "HIGH":
        cls = "risk-badge-high"
    elif lvl == "MEDIUM":
        cls = "risk-badge-medium"
    else:
        cls = "risk-badge-low"
    return f'<span class="{cls}">{lvl or "LOW"}</span>'


# =========================
# PAGES
# =========================

# ---- Page 1: Overview ----


def page_overview(df: pd.DataFrame):
    render_overview_kpis(df)
    st.markdown("")

    if df.empty:
        return

    st.markdown('<div class="card" style="margin-top:12px;">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Network trading story</div>'
        '<div class="section-caption">'
        "How liquidity and risk are evolving across the ecosystem in the selected window."
        "</div>",
        unsafe_allow_html=True,
    )

    vol_by_asset = (
        df.groupby("asset", as_index=False)["trade_value_usdt"].sum().sort_values(
            "trade_value_usdt", ascending=False
        )
    )
    ts = (
        df.groupby(pd.Grouper(key="timestamp", freq="15min"))["trade_value_usdt"]
        .sum()
        .reset_index()
    )

    col1, col2 = st.columns([2.2, 1.8])

    with col1:
        fig = px.bar(
            vol_by_asset,
            x="asset",
            y="trade_value_usdt",
            title="Volume by asset (USDT)",
            labels={"trade_value_usdt": "Volume (USDT)", "asset": "Asset"},
        )
        fig.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=10, r=10, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.96)",
            title={
                "text": "Volume by asset (USDT)",
                "x": 0.5,        # <-- CENTER TITLE
                "xanchor": "center"
            }
        )


        st.plotly_chart(fig, use_container_width=True)

    with col2:
        trade_count_by_asset = (
            df.groupby("asset", as_index=False)["timestamp_raw"].count().rename(
                columns={"timestamp_raw": "trades"}
            )
        )
        fig2 = px.bar(
            trade_count_by_asset.sort_values("trades", ascending=False),
            x="asset",
            y="trades",
            title="Number of trades per asset",
            labels={"trades": "Trades", "asset": "Asset"},
        )
        fig2.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=10, r=10, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title={
                        "text": "Number of trades per asset",
                        "x": 0.5,        
                        "xanchor": "center"
                    }
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="card-soft">', unsafe_allow_html=True)
    col_ts, col_dist = st.columns([2.2, 1.8])

    with col_ts:
        st.markdown(
            '<div class="section-title">Liquidity over time</div>'
            '<div class="section-caption">'
            "15-minute aggregated trade value in USDT. Spikes may indicate coordinated activity."
            "</div>",
            unsafe_allow_html=True,
        )
        if not ts.empty:
            fig3 = px.line(
                ts,
                x="timestamp",
                y="trade_value_usdt",
                labels={"trade_value_usdt": "Volume (USDT)", "timestamp": "Time"},
            )
            fig3.update_layout(
                template="plotly_dark",
                height=280,
                margin=dict(l=10, r=10, t=10, b=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No time-series data after filters.")

    with col_dist:
        st.markdown(
            '<div class="section-title">Trade value buckets</div>'
            '<div class="section-caption">'
            "Distribution of trade sizes – do we see mostly retail or whale-sized flows?"
            "</div>",
            unsafe_allow_html=True,
        )
        bins = [0, 10, 50, 100, 250, 500, 1000, 5_000, 10_000]
        labels = [
            "<10",
            "10–50",
            "50–100",
            "100–250",
            "250–500",
            "500–1k",
            "1k–5k",
            "5k–10k",
        ]
        df["value_bucket"] = pd.cut(
            df["trade_value_usdt"].fillna(0), bins=bins, labels=labels, right=False
        )
        bucket_counts = (
            df["value_bucket"].value_counts().rename_axis("bucket").reset_index(name="trades")
        )
        if not bucket_counts.empty:
            fig4 = px.bar(
                bucket_counts.sort_values("bucket"),
                x="bucket",
                y="trades",
                labels={"bucket": "Trade size (USDT)", "trades": "Trades"},
            )
            fig4.update_layout(
                template="plotly_dark",
                height=280,
                margin=dict(l=10, r=10, t=10, b=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Not enough data to build bucket distribution.")

    st.markdown("</div>", unsafe_allow_html=True)


# ---- Page 2: Risk & Anomalies ----


def page_risk(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Risk posture</div>'
        '<div class="section-caption">'
        "Where is risk concentrated? Which assets and trades are triggering alerts?"
        "</div>",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No trades in this window. Cannot compute risk metrics.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    risk_counts = (
        df["effective_risk"]
        .str.upper()
        .replace({"": "LOW", None: "LOW"})
        .value_counts()
        .rename_axis("risk")
        .reset_index(name="trades")
    )

    whale_anomaly = df[(df["is_whale"]) | (df["has_anomaly"])]

    col1, col2, col3 = st.columns([1.4, 1.4, 1.2])

    with col1:
        if not risk_counts.empty:
            fig = px.pie(
                risk_counts,
                names="risk",
                values="trades",
                title="Risk level distribution",
            )
            fig.update_layout(
                template="plotly_dark",
                height=320,
                margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                title={
                            "text": "Risk level distribution",
                            "x": 0.5,        
                            "xanchor": "center"
                        }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No risk labels to plot.")

    with col2:
        if not whale_anomaly.empty:
            top_risky_assets = (
                whale_anomaly.groupby("asset", as_index=False)["trade_value_usdt"]
                .sum()
                .sort_values("trade_value_usdt", ascending=False)
                .head(10)
            )
            fig2 = px.bar(
                top_risky_assets,
                x="asset",
                y="trade_value_usdt",
                title="Whale / anomaly volume by asset",
                labels={"trade_value_usdt": "Volume (USDT)", "asset": "Asset"},
            )
            fig2.update_layout(
                template="plotly_dark",
                height=320,
                margin=dict(l=10, r=10, t=40, b=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                title={
                            "text": "Whale / anomaly volume by asset",
                            "x": 0.5,        
                            "xanchor": "center"
                        }
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No whale or anomaly trades in this window.")

    with col3:
        high = df[df["effective_risk"].str.upper() == "HIGH"]
        med = df[df["effective_risk"].str.upper() == "MEDIUM"]
        low = df[df["effective_risk"].str.upper().isin(["LOW", "", None])]

        st.write("**Risk inventory**")
        st.metric("High risk trades", len(high))
        st.metric("Medium risk trades", len(med))
        st.metric("Low/no risk trades", len(low))

        st.write("")
        st.caption(
            "High-risk trades combine anomaly flags with large value or unusual behavior. "
            "Use the feed below to investigate specific txids."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="card-soft">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Live risk & anomaly feed</div>'
        '<div class="section-caption">'
        "Most recent high-impact trades. Sort by timestamp or value in the table for investigation."
        "</div>",
        unsafe_allow_html=True,
    )

    df_sorted = df.copy()
    risk_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    df_sorted["risk_rank"] = df_sorted["effective_risk"].str.upper().map(risk_order).fillna(0)
    df_sorted = df_sorted.sort_values(["risk_rank", "timestamp"], ascending=[False, False])

    top = df_sorted.head(30)

    if top.empty:
        st.info("No trades with risk labels available.")
    else:
        rows = []
        for _, row in top.iterrows():
            ts_str = (
                row["timestamp"].strftime("%Y-%m-%d %H:%M:%S UTC")
                if pd.notna(row["timestamp"])
                else "-"
            )
            rows.append(
                {
                    "Time": ts_str,
                    "Asset": row.get("asset"),
                    "Value (USDT)": round(row.get("trade_value_usdt", 0.0), 2),
                    "Shares": int(row.get("shares", 0) or 0),
                    "Direction": row.get("direction"),
                    "Side": row.get("side"),
                    "Risk": row.get("effective_risk"),
                    "Anomaly tags": row.get("risk_tags_anamoly"),
                    "TxID": row.get("txid", ""),
                }
            )
        alert_df = pd.DataFrame(rows)
        st.dataframe(alert_df, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---- Page 3: Asset Intelligence ----


def page_assets(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Asset intelligence</div>'
        '<div class="section-caption">'
        "Compare tokens by liquidity, whale activity and risk. Then deep-dive into a single asset."
        "</div>",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No data available for assets in this window.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    grouped = (
        df.groupby("asset")
        .agg(
            trades=("timestamp_raw", "count"),
            volume_usdt=("trade_value_usdt", "sum"),
            whales=("is_whale", "sum"),
            anomalies=("has_anomaly", "sum"),
        )
        .reset_index()
    )

    grouped["whale_share"] = grouped["whales"] / grouped["trades"] * 100
    grouped["anomaly_share"] = grouped["anomalies"] / grouped["trades"] * 100

    grouped = grouped.sort_values("volume_usdt", ascending=False)

    col1, col2 = st.columns([1.8, 1.8])

    with col1:
        fig = px.scatter(
            grouped,
            x="volume_usdt",
            y="whale_share",
            size="trades",
            color="anomaly_share",
            hover_data=["asset", "trades", "whales", "anomalies"],
            labels={
                "volume_usdt": "Volume (USDT)",
                "whale_share": "Whale share (%)",
                "anomaly_share": "Anomaly share (%)",
            },
            title="Liquidity vs whale intensity",
        )
        fig.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=10, r=10, t=40, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title={
                            "text": "Liquidity vs whale intensity",
                            "x": 0.5,        
                            "xanchor": "center"
                        }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Asset league table**")
        st.caption("Sorted by volume. Use this to identify priority tokens for monitoring.")
        show_cols = [
            "asset",
            "trades",
            "volume_usdt",
            "whales",
            "anomalies",
            "whale_share",
            "anomaly_share",
        ]
        tbl = grouped[show_cols].copy()
        tbl["volume_usdt"] = tbl["volume_usdt"].round(2)
        tbl["whale_share"] = tbl["whale_share"].round(1)
        tbl["anomaly_share"] = tbl["anomaly_share"].round(1)
        st.dataframe(tbl, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="card-soft">', unsafe_allow_html=True)

    assets = grouped["asset"].tolist()
    default_asset = assets[0] if assets else None
    selected_asset = st.selectbox("Focus asset", assets, index=0 if default_asset else None)

    if selected_asset:
        asset_df = df[df["asset"] == selected_asset].copy()

        st.markdown(
            f'<div class="section-title">Trading story – {selected_asset}</div>'
            '<div class="section-caption">'
            "Timeline of trades, whale entries and risk level evolution for this token."
            "</div>",
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns([2.2, 1.8])

        with col_a:
            if asset_df["timestamp"].notna().any():
                ts_asset = (
                    asset_df.groupby(pd.Grouper(key="timestamp", freq="15min"))[
                        "trade_value_usdt"
                    ]
                    .sum()
                    .reset_index()
                )
                fig_ts = px.area(
                    ts_asset,
                    x="timestamp",
                    y="trade_value_usdt",
                    labels={
                        "trade_value_usdt": "Volume (USDT)",
                        "timestamp": "Time",
                    },
                )
                fig_ts.update_layout(
                    template="plotly_dark",
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=40),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_ts, use_container_width=True)
            else:
                st.info("No timestamp information for this asset.")

        with col_b:
            asset_df["bucket"] = pd.cut(
                asset_df["trade_value_usdt"].fillna(0),
                bins=[0, 50, 100, 250, 500, 1_000, 5_000, 10_000],
                labels=["<50", "50–100", "100–250", "250–500", "500–1k", "1k–5k", "5k–10k"],
                right=False,
            )
            dist = (
                asset_df["bucket"]
                .value_counts()
                .rename_axis("Bucket")
                .reset_index(name="Trades")
            )
            if not dist.empty:
                fig_bucket = px.bar(
                    dist.sort_values("Bucket"),
                    x="Bucket",
                    y="Trades",
                    title="Trade size distribution",
                )
                fig_bucket.update_layout(
                    template="plotly_dark",
                    height=280,
                    margin=dict(l=10, r=10, t=40, b=40),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    title={
                            "text": "Trade size distribution",
                            "x": 0.5,        
                            "xanchor": "center"
                        }
                    
                )
                st.plotly_chart(fig_bucket, use_container_width=True)
            else:
                st.info("Not enough trades for distribution.")

        st.markdown("---")
        st.write("**Latest trades for this asset**")

        cols = [
            "timestamp",
            "trade_value_usdt",
            "shares",
            "side",
            "direction",
            "effective_risk",
            "risk_tags_anamoly",
        ]
        if "txid" in asset_df.columns:
            cols.append("txid")

        latest = asset_df.head(20)[[c for c in cols if c in asset_df.columns]].copy()
        if "timestamp" in latest.columns:
            latest["timestamp"] = latest["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        if "trade_value_usdt" in latest.columns:
            latest["trade_value_usdt"] = latest["trade_value_usdt"].round(4)

        st.dataframe(latest, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---- Page 4: Trade Explorer ----


def page_explorer(df: pd.DataFrame):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">Trade explorer</div>'
        '<div class="section-caption">'
        "Low-level view of every trade after filters. Use this for debugging or exporting to CSV."
        "</div>",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No trades to explore in the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    n = len(df)
    if n <= 20:
        max_rows = n
    else:
        max_rows = st.slider(
            "Rows to show",
            min_value=20,
            max_value=min(1000, n),
            value=min(200, n),
            step=20,
        )

    cols = [
        "timestamp",
        "asset",
        "shares",
        "trade_value_usdt",
        "side",
        "direction",
        "risk_level",
        "risk_level_anamoly",
        "risk_tags_anamoly",
    ]
    if "txid" in df.columns:
        cols.append("txid")

    disp = df.head(max_rows)[[c for c in cols if c in df.columns]].copy()

    if "timestamp" in disp.columns:
        disp["timestamp"] = disp["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    if "trade_value_usdt" in disp.columns:
        disp["trade_value_usdt"] = disp["trade_value_usdt"].round(4)

    st.dataframe(disp, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download filtered trades as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="qubic_guardian_filtered_trades.csv",
        mime="text/csv",
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN APP
# =========================


def main():
    render_header()

    # top_cols = st.columns([1, 4])
    # with top_cols[0]:
    #     if st.button("🔄 Refresh now"):
    #         load_data.clear()
    # with top_cols[1]:
    #     st.caption(
    #         "Data auto-refreshes roughly every **30 seconds** via caching. "
    #         "Use **Refresh now** after major activity or new hackathon tests."
    #     )

    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error fetching data from n8n: {e}")
        st.stop()

    # ---- Sidebar layout: logo -> nav -> filters ----
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
        page = st.radio(
            "",
            ["Overview", "Risk & Anomalies", "Asset Intelligence", "Trade Explorer"],
            index=0,
            label_visibility="collapsed",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        filtered_df = sidebar_filters(df)

        # Refresh button under filters
        if st.button("🔄 Refresh now", use_container_width=True, key="refresh_sidebar"):
            load_data.clear()


    st.markdown("---")

    if page == "Overview":
        page_overview(filtered_df)
    elif page == "Risk & Anomalies":
        page_risk(filtered_df)
    elif page == "Asset Intelligence":
        page_assets(filtered_df)
    else:
        page_explorer(filtered_df)


if __name__ == "__main__":
    main()
