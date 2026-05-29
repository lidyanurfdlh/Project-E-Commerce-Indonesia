
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Customer ID Analytics Dashboard", page_icon="👤", layout="wide")

st.markdown("""
<style>
.block-container {padding-top:1.4rem; max-width:1450px;}
.hero {background:linear-gradient(135deg,#0f172a,#1e293b,#0e7490); padding:28px; border-radius:24px; color:white; margin-bottom:18px;}
.hero h1 {margin:0 0 8px 0; font-size:34px;}
.hero p {color:#dbeafe; font-size:15px; line-height:1.6;}
.badge {display:inline-block; background:rgba(14,165,233,.22); border:1px solid rgba(186,230,253,.35); padding:7px 11px; border-radius:999px; margin:8px 6px 0 0; font-weight:700; font-size:12px;}
.info {background:#f8fafc; border-left:5px solid #0891b2; border-radius:12px; padding:13px 15px; color:#334155; line-height:1.6; margin:8px 0 14px 0;}
.warn {background:#fff7ed; border-left:5px solid #f97316; border-radius:12px; padding:13px 15px; color:#7c2d12; line-height:1.6; margin:8px 0 14px 0;}
.metricbox {background:white; border:1px solid #e2e8f0; border-radius:18px; padding:16px; box-shadow:0 8px 20px rgba(15,23,42,.06);}
.metriclabel {font-size:12px; color:#64748b; font-weight:800; text-transform:uppercase; letter-spacing:.5px;}
.metricvalue {font-size:26px; color:#0f172a; font-weight:850; margin-top:5px;}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "outputs"
DATE_COL = "order_date"
REVENUE_COL = "subtotal"
CATEGORY_COL = "kategori"

@st.cache_data
def load_csv(filename):
    path = OUT_DIR / filename
    if not path.exists():
        st.error(f"File {filename} tidak ditemukan. Pastikan folder outputs sudah berisi hasil dari notebook Colab.")
        st.stop()
    return pd.read_csv(path)

@st.cache_data
def load_json(filename):
    path = OUT_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def rupiah(value):
    try:
        return "Rp" + f"{float(value):,.0f}".replace(",", ".")
    except Exception:
        return "Rp0"

def fmt_num(value):
    try:
        return f"{int(float(value)):,}".replace(",", ".")
    except Exception:
        return str(value)

def metric_box(label, value):
    st.markdown(f"""
    <div class="metricbox">
      <div class="metriclabel">{label}</div>
      <div class="metricvalue">{value}</div>
    </div>
    """, unsafe_allow_html=True)

summary = load_json("project_summary.json")
rfm = load_csv("customer_rfm.csv")
segment_summary = load_csv("segment_summary.csv")
monthly = load_csv("customer_monthly_summary.csv")
customer_product = load_csv("customer_product_summary.csv")
rules = load_csv("market_basket_rules.csv")
next_best_action = load_csv("next_best_action.csv")
top_products = load_csv("top_products.csv")
line_items = load_csv("transaction_line_items.csv")

if DATE_COL in line_items.columns:
    line_items[DATE_COL] = pd.to_datetime(line_items[DATE_COL], errors="coerce")
for col in ["first_order_date", "last_order_date"]:
    if col in rfm.columns:
        rfm[col] = pd.to_datetime(rfm[col], errors="coerce")

st.markdown("""
<div class="hero">
<h1>👤 Customer ID Analytics Dashboard — Recommendation Logic</h1>
<p>Dashboard customer-centric berbasis <b>Customer RFM</b>, <b>Association Rule</b>, dan <b>Nudge / Next Best Action</b>. Tujuannya adalah melakukan segmentasi pelanggan berdasarkan perilaku transaksi, rekomendasi kategori/bundling, serta strategi pesan promosi yang dapat ditindaklanjuti. Logika rekomendasi produk utama mengikuti kategori favorit pelanggan, sedangkan cross-sell dari Association Rule ditampilkan terpisah.</p>
<span class="badge">Customer ID</span><span class="badge">RFM</span><span class="badge">Association Rule</span><span class="badge">Nudge Theory</span><span class="badge">Next Best Action</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Filter Dashboard")
    segment_options = sorted(rfm["segment"].dropna().unique().tolist())
    selected_segments = st.multiselect("Segment customer", segment_options, default=segment_options)
    min_freq = int(rfm["frequency"].min()) if len(rfm) else 0
    max_freq = int(rfm["frequency"].max()) if len(rfm) else 1
    selected_freq = st.slider("Frekuensi transaksi/order", min_freq, max_freq, (min_freq, max_freq))
    customer_search = st.text_input("Cari customer_id", "")
    st.divider()
    st.write("**Inti Metode**")
    st.caption("RFM membentuk segmentasi pelanggan. Association Rule Mining mencari pola kategori yaitu recommended_product mengikuti favorite_category terlebih dahulu dan cross_sell_product_from_rule dipisahkan agar rekomendasi tidak terlihat random. Nudge menyusun pesan dan next best action")

filtered = rfm[rfm["segment"].isin(selected_segments)].copy()
filtered = filtered[(filtered["frequency"] >= selected_freq[0]) & (filtered["frequency"] <= selected_freq[1])]
if customer_search.strip():
    try:
        filtered = filtered[filtered["customer_id"] == int(customer_search.strip())]
    except ValueError:
        st.warning("customer_id harus berupa angka.")

k1, k2, k3, k4, k5 = st.columns(5)
with k1: metric_box("Customer", fmt_num(filtered['customer_id'].nunique()))
with k2: metric_box("Revenue", rupiah(filtered["monetary"].sum()))
with k3: metric_box("Avg Frequency", f"{filtered['frequency'].mean() if len(filtered) else 0:.2f}")
with k4: metric_box("Repeat Rate", f"{(filtered['frequency'].gt(1).mean()*100 if len(filtered) else 0):.1f}%")
with k5: metric_box("Avg Order Value", rupiah(filtered["avg_order_value"].mean() if len(filtered) else 0))

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview RFM", "Market Basket Rules", "Next Best Action", "Customer 360", "Data & Panduan"])

with tab1:
    st.subheader("1. Segmentasi Customer Berbasis RFM")
    left, right = st.columns(2)
    with left:
        seg_count = filtered.groupby("segment", as_index=False).agg(customers=("customer_id", "nunique"), revenue=("monetary", "sum"))
        if not seg_count.empty:
            fig = px.bar(seg_count.sort_values("customers", ascending=True), x="customers", y="segment", orientation="h", title="Jumlah Customer per Segment")
            st.plotly_chart(fig, use_container_width=True)
    with right:
        if not filtered.empty:
            fig = px.scatter(filtered, x="recency_days", y="monetary", size="frequency", color="segment", hover_data=["customer_id", "rfm_score"], title="Recency vs Monetary per Customer")
            st.plotly_chart(fig, use_container_width=True)
    st.dataframe(segment_summary, use_container_width=True)

    st.subheader("Tren Bulanan per Segment")
    if not monthly.empty:
        fig = px.line(monthly, x="month", y="revenue", color="segment", markers=True, title="Revenue Bulanan")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("2. Market Basket Rules untuk Cross-Selling")
    st.markdown('<div class="info"><b>Catatan:</b> Association Rule tetap dipakai untuk cross-selling. Namun, hasil rule tidak lagi langsung dipaksakan menjadi recommended_product utama jika berbeda jauh dari kategori favorit pelanggan.</div>', unsafe_allow_html=True)
    if rules.empty:
        st.info("Belum ada rules yang memenuhi minimum support/confidence/lift.")
    else:
        levels = sorted(rules["rule_level"].dropna().unique().tolist()) if "rule_level" in rules.columns else []
        selected_level = st.selectbox("Level rule", levels) if levels else None
        rules_show = rules[rules["rule_level"] == selected_level] if selected_level else rules
        st.dataframe(rules_show.head(50), use_container_width=True)
        if {"support","confidence","lift"}.issubset(rules_show.columns) and not rules_show.empty:
            fig = px.scatter(rules_show, x="support", y="confidence", size="lift", color="lift", hover_data=["antecedent","consequent"], title="Support vs Confidence")
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("3. Next Best Action per Customer")
    st.markdown('<div class="warn"><b>Catatan:</b> recommended_product sekarang diprioritaskan dari favorite_category pelanggan. Jika customer favoritnya Alat Tulis, rekomendasi utama juga Alat Tulis. Produk lintas kategori dari Association Rule ditampilkan di kolom cross_sell_product_from_rule.</div>', unsafe_allow_html=True)
    segments_nba = sorted(next_best_action["segment"].dropna().unique().tolist())
    selected_nba_segment = st.selectbox("Segment rekomendasi", ["Semua"] + segments_nba)
    nba_show = next_best_action.copy() if selected_nba_segment == "Semua" else next_best_action[next_best_action["segment"] == selected_nba_segment]
    display_cols = [c for c in ["customer_id","segment","favorite_category","favorite_product","recommended_product","recommended_category","recommendation_basis","recommendation_reason","cross_sell_product_from_rule","cross_sell_category_from_rule","nudge_type","action_recommendation"] if c in nba_show.columns]
    st.dataframe(nba_show[display_cols].head(100), use_container_width=True, height=520)

    st.subheader("Distribusi Basis Rekomendasi")
    if "recommendation_basis" in nba_show.columns:
        basis = nba_show["recommendation_basis"].value_counts().reset_index()
        basis.columns = ["recommendation_basis", "customers"]
        fig = px.bar(basis, x="customers", y="recommendation_basis", orientation="h", title="Jumlah Customer per Basis Rekomendasi")
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("4. Customer 360°")
    customer_ids = filtered["customer_id"].dropna().astype(int).sort_values().tolist()
    if customer_ids:
        selected_customer = st.selectbox("Pilih customer_id", customer_ids[:5000])
        profile = rfm[rfm["customer_id"] == selected_customer].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Segment", profile["segment"])
        c2.metric("RFM", profile["rfm_score"])
        c3.metric("Frequency", int(profile["frequency"]))
        c4.metric("Monetary", rupiah(profile["monetary"]))

        cust_nba = next_best_action[next_best_action["customer_id"] == selected_customer]
        if not cust_nba.empty:
            st.success(cust_nba.iloc[0]["message_template"])
            st.write("**Aksi yang disarankan:**", cust_nba.iloc[0]["action_recommendation"])
            st.write("**Produk cross-sell dari rule:**", cust_nba.iloc[0].get("cross_sell_product_from_rule", "-"))
            st.write("**Alasan cross-sell:**", cust_nba.iloc[0].get("cross_sell_reason", "-"))

        st.write("**Riwayat transaksi/order**")
        cust_line = line_items[line_items["customer_id"] == selected_customer].sort_values(DATE_COL, ascending=False)
        st.dataframe(cust_line.head(100), use_container_width=True)

        st.write("**Ringkasan produk customer**")
        cust_prod = customer_product[customer_product["customer_id"] == selected_customer]
        st.dataframe(cust_prod, use_container_width=True)
    else:
        st.info("Tidak ada customer sesuai filter.")

with tab5:
    st.subheader("5. Data dan Panduan Baca")
    st.markdown("""
    **Cara membaca:**
    - `favorite_category` adalah kategori dominan pelanggan berdasarkan nilai transaksi.
    - `recommended_product` adalah rekomendasi utama yang mengikuti kategori favorit terlebih dahulu.
    - `recommended_category` menunjukkan kategori dari produk rekomendasi utama.
    - `recommendation_basis` menjelaskan asal logika rekomendasi.
    - `cross_sell_product_from_rule` adalah rekomendasi tambahan dari Association Rule.
    - Dengan pemisahan ini, rekomendasi utama tidak terlihat random, tetapi insight cross-selling tetap tersedia.
    """)
    data_choice = st.selectbox("Pilih data", ["customer_rfm", "segment_summary", "market_basket_rules", "next_best_action", "transaction_line_items", "customer_product_summary", "top_products"])
    mapping = {
        "customer_rfm": rfm,
        "segment_summary": segment_summary,
        "market_basket_rules": rules,
        "next_best_action": next_best_action,
        "transaction_line_items": line_items,
        "customer_product_summary": customer_product,
        "top_products": top_products,
    }
    st.dataframe(mapping[data_choice], use_container_width=True, height=540)
