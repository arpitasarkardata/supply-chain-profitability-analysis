import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain Profitability | APL Logistics",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fb; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 5px solid #1a6faf;
        margin-bottom: 0.5rem;
    }
    .kpi-label { font-size: 0.78rem; color: #888; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
    .kpi-value { font-size: 1.7rem; font-weight: 800; color: #1a1a2e; margin: 0; }
    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #1a6faf;
        border-bottom: 2px solid #e0ecf8; padding-bottom: 6px; margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='color:#1a1a2e; margin-bottom:0'>🚢 APL Logistics — Supply Chain Profitability Dashboard</h1>
<p style='color:#888; margin-top:4px'>Customer, Product & Profitability Performance Analysis | Unified Mentor Project</p>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Data Loading from Google Drive ───────────────────────────────────────────
@st.cache_data
def load_data():
    file_id = "1RyHvfQcwuT-mIA_UVRJtNnPIpN07oKZ-"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    df = pd.read_csv(url, encoding="latin1", low_memory=False)
    df.columns = df.columns.str.strip()
    num_cols = [
        "Benefit per order", "Sales per customer", "Order Item Discount",
        "Order Item Discount Rate", "Order Item Product Price",
        "Order Item Profit Ratio", "Order Item Quantity", "Sales",
        "Order Item Total", "Order Profit Per Order"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df.dropna(subset=["Sales", "Order Profit Per Order"], how="all", inplace=True)
    df["Profit Margin %"] = (df["Order Profit Per Order"] / df["Sales"].replace(0, np.nan)) * 100
    df["Customer Name"]   = df["Customer Fname"].astype(str) + " " + df["Customer Lname"].astype(str)
    return df

with st.spinner("⏳ Loading data from Google Drive... please wait"):
    try:
        df_raw = load_data()
        st.success(f"✅ Data loaded: {len(df_raw):,} orders")
    except Exception as e:
        st.error(f"❌ Could not load data: {e}")
        st.stop()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

all_markets    = sorted(df_raw["Market"].dropna().unique().tolist())
all_segments   = sorted(df_raw["Customer Segment"].dropna().unique().tolist())
all_categories = sorted(df_raw["Category Name"].dropna().unique().tolist())
all_statuses   = sorted(df_raw["Order Status"].dropna().unique().tolist())

sel_markets    = st.sidebar.multiselect("Market", all_markets, default=all_markets)
sel_segments   = st.sidebar.multiselect("Customer Segment", all_segments, default=all_segments)
sel_categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)
sel_statuses   = st.sidebar.multiselect("Order Status", all_statuses, default=all_statuses)
disc_range     = st.sidebar.slider("Discount Rate Range", 0.0, 1.0, (0.0, 1.0), step=0.01)

df = df_raw[
    df_raw["Market"].isin(sel_markets) &
    df_raw["Customer Segment"].isin(sel_segments) &
    df_raw["Category Name"].isin(sel_categories) &
    df_raw["Order Status"].isin(sel_statuses) &
    df_raw["Order Item Discount Rate"].between(disc_range[0], disc_range[1])
].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(df):,}** orders selected")
st.sidebar.markdown("---")
st.sidebar.markdown("**Built by:** Arpita Sarkar")
st.sidebar.markdown("**Project:** APL Logistics — Unified Mentor")
st.sidebar.markdown("[GitHub](https://github.com/arpitasarkardata/supply-chain-profitability-analysis) | [LinkedIn](https://www.linkedin.com/in/arpita-sarkar-00921a225/)")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Revenue & Profit Overview",
    "👥 Customer Value",
    "📦 Product & Category",
    "🏷️ Discount Impact",
    "🌍 Market & Region"
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — Revenue & Profit Overview
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Revenue & Profit Overview</div>', unsafe_allow_html=True)

    total_revenue = df["Sales"].sum()
    total_profit  = df["Order Profit Per Order"].sum()
    avg_margin    = (total_profit / total_revenue * 100) if total_revenue else 0
    total_orders  = len(df)
    avg_order_val = total_revenue / total_orders if total_orders else 0
    loss_pct      = (df["Order Profit Per Order"] < 0).mean() * 100

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    for col, label, value, icon in [
        (c1, "Total Revenue",      f"${total_revenue:,.0f}", "💰"),
        (c2, "Total Profit",       f"${total_profit:,.0f}",  "📈"),
        (c3, "Profit Margin",      f"{avg_margin:.1f}%",      "🎯"),
        (c4, "Total Orders",       f"{total_orders:,}",       "📦"),
        (c5, "Avg Order Value",    f"${avg_order_val:,.1f}",  "🛒"),
        (c6, "Loss-Making Orders", f"{loss_pct:.1f}%",        "⚠️"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value">{value}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        seg_grp = df.groupby("Customer Segment").agg(
            Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
        ).reset_index()
        fig = go.Figure()
        fig.add_bar(x=seg_grp["Customer Segment"], y=seg_grp["Revenue"], name="Revenue", marker_color="#1a6faf")
        fig.add_bar(x=seg_grp["Customer Segment"], y=seg_grp["Profit"],  name="Profit",  marker_color="#22c55e")
        fig.update_layout(title="Revenue vs Profit by Customer Segment",
                          barmode="group", height=350, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        ship_grp = df.groupby("Shipping Mode").agg(
            Revenue=("Sales", "sum"), Profit=("Order Profit Per Order", "sum")
        ).reset_index()
        ship_grp["Margin %"] = ship_grp["Profit"] / ship_grp["Revenue"] * 100
        fig2 = px.bar(ship_grp, x="Shipping Mode", y="Margin %", color="Margin %",
                      color_continuous_scale="RdYlGn", title="Profit Margin % by Shipping Mode",
                      text=ship_grp["Margin %"].apply(lambda x: f"{x:.1f}%"))
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=350, plot_bgcolor="white", coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        del_grp = df.groupby("Delivery Status")["Order Profit Per Order"].sum().reset_index()
        fig3 = px.pie(del_grp, names="Delivery Status", values="Order Profit Per Order",
                      title="Profit by Delivery Status",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        fig4 = px.histogram(df, x="Order Profit Per Order", nbins=80,
                            title="Profit Per Order Distribution",
                            color_discrete_sequence=["#1a6faf"])
        fig4.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig4.update_layout(height=350, plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — Customer Value
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Customer Value Dashboard</div>', unsafe_allow_html=True)

    cust_grp = df.groupby(["Customer Id", "Customer Name", "Customer Segment"]).agg(
        Total_Revenue=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
    ).reset_index()
    cust_grp["Margin %"] = (cust_grp["Total_Profit"] / cust_grp["Total_Revenue"].replace(0, np.nan) * 100).round(1)

    p33 = cust_grp["Total_Profit"].quantile(0.33)
    p66 = cust_grp["Total_Profit"].quantile(0.66)
    cust_grp["Tier"] = cust_grp["Total_Profit"].apply(
        lambda p: "🟢 High Value" if p >= p66 else ("🟡 Mid Value" if p >= p33 else "🔴 Low / Loss")
    )

    top_n = st.slider("Show Top / Bottom N customers", 5, 30, 15)
    col1, col2 = st.columns(2)

    with col1:
        top_c = cust_grp.nlargest(top_n, "Total_Profit")
        fig = px.bar(top_c, x="Total_Profit", y="Customer Name", orientation="h",
                     color="Total_Profit", color_continuous_scale="Blues",
                     title=f"Top {top_n} Customers by Profit")
        fig.update_layout(height=450, yaxis=dict(autorange="reversed"),
                          plot_bgcolor="white", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        bot_c = cust_grp.nsmallest(top_n, "Total_Profit")
        fig2 = px.bar(bot_c, x="Total_Profit", y="Customer Name", orientation="h",
                      color="Total_Profit", color_continuous_scale="Reds_r",
                      title=f"Bottom {top_n} Customers (Loss-Making)")
        fig2.update_layout(height=450, yaxis=dict(autorange="reversed"),
                           plot_bgcolor="white", coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        tier_cnt = cust_grp["Tier"].value_counts().reset_index()
        tier_cnt.columns = ["Tier", "Count"]
        fig3 = px.pie(tier_cnt, names="Tier", values="Count",
                      title="Customer Value Tier Distribution",
                      color_discrete_map={"🟢 High Value": "#22c55e",
                                          "🟡 Mid Value": "#eab308",
                                          "🔴 Low / Loss": "#ef4444"})
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.scatter(cust_grp, x="Total_Revenue", y="Total_Profit",
                          color="Customer Segment", size="Orders",
                          hover_name="Customer Name",
                          title="Revenue vs Profit per Customer")
        fig4.add_hline(y=0, line_dash="dash", line_color="red")
        fig4.update_layout(height=350, plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Customer Detail Table")
    st.dataframe(
        cust_grp.sort_values("Total_Profit", ascending=False).reset_index(drop=True)
                .rename(columns={"Total_Revenue": "Revenue ($)",
                                  "Total_Profit": "Profit ($)", "Orders": "# Orders"}),
        use_container_width=True, height=320
    )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — Product & Category
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Product & Category Performance</div>', unsafe_allow_html=True)

    cat_grp = df.groupby("Category Name").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
        Avg_Discount=("Order Item Discount Rate", "mean")
    ).reset_index()
    cat_grp["Margin %"] = (cat_grp["Profit"] / cat_grp["Revenue"].replace(0, np.nan) * 100).round(1)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(cat_grp.sort_values("Profit", ascending=True),
                     x="Profit", y="Category Name", orientation="h",
                     color="Margin %", color_continuous_scale="RdYlGn",
                     title="Profit by Category")
        fig.add_vline(x=0, line_dash="dash", line_color="red")
        fig.update_layout(height=500, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.scatter(cat_grp, x="Revenue", y="Profit",
                          size="Orders", color="Margin %",
                          color_continuous_scale="RdYlGn",
                          hover_name="Category Name", text="Category Name",
                          title="Revenue vs Profit Bubble (by Category)")
        fig2.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig2.update_traces(textposition="top center", textfont_size=9)
        fig2.update_layout(height=500, plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    prod_n = st.slider("Number of products to show", 10, 30, 15, key="prod_slider")
    prod_grp = df.groupby("Product Name").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
    ).reset_index()
    prod_grp["Margin %"] = (prod_grp["Profit"] / prod_grp["Revenue"].replace(0, np.nan) * 100).round(1)

    col3, col4 = st.columns(2)
    with col3:
        top_prod = prod_grp.nlargest(prod_n, "Profit")
        fig3 = px.bar(top_prod, x="Profit", y="Product Name", orientation="h",
                      color="Margin %", color_continuous_scale="Blues",
                      title=f"Top {prod_n} Products by Profit")
        fig3.update_layout(height=500, yaxis=dict(autorange="reversed"), plot_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        risky = prod_grp[
            (prod_grp["Revenue"] > prod_grp["Revenue"].quantile(0.5)) &
            (prod_grp["Margin %"] < 10)
        ].nlargest(prod_n, "Revenue")
        if not risky.empty:
            fig4 = px.bar(risky, x="Revenue", y="Product Name", orientation="h",
                          color="Margin %", color_continuous_scale="OrRd",
                          title="⚠️ High Revenue, Low Margin Products")
            fig4.update_layout(height=500, yaxis=dict(autorange="reversed"), plot_bgcolor="white")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No high-revenue, low-margin products found with current filters.")

    st.markdown("#### Category × Customer Segment Profit Heatmap")
    heat_data = df.pivot_table(index="Category Name", columns="Customer Segment",
                               values="Order Profit Per Order", aggfunc="sum")
    fig5 = px.imshow(heat_data, color_continuous_scale="RdYlGn", aspect="auto",
                     title="Profit Heatmap: Category × Segment",
                     labels=dict(color="Profit ($)"))
    fig5.update_layout(height=500)
    st.plotly_chart(fig5, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — Discount Impact
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Discount Impact Analyzer</div>', unsafe_allow_html=True)

    avg_disc   = df["Order Item Discount Rate"].mean() * 100
    total_disc = df["Order Item Discount"].sum()
    avg_pr     = df["Order Item Profit Ratio"].mean() * 100

    c1, c2, c3 = st.columns(3)
    for col, label, val in [
        (c1, "Avg Discount Rate",    f"{avg_disc:.1f}%"),
        (c2, "Total Discount Given", f"${total_disc:,.0f}"),
        (c3, "Avg Profit Ratio",     f"{avg_pr:.1f}%"),
    ]:
        with col:
            st.markdown(f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        sample = df.sample(min(5000, len(df)), random_state=42)
        fig = px.scatter(sample, x="Order Item Discount Rate", y="Order Item Profit Ratio",
                         color="Customer Segment", opacity=0.5, 
                         title="Discount Rate vs Profit Ratio")
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig.update_layout(height=400, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df["Discount Bracket"] = pd.cut(
            df["Order Item Discount Rate"],
            bins=[-0.01, 0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 1.0],
            labels=["0%", "1-5%", "5-10%", "10-15%", "15-20%", "20-30%", "30%+"]
        )
        disc_impact = df.groupby("Discount Bracket", observed=True).agg(
            Avg_Margin=("Profit Margin %", "mean"),
            Orders=("Sales", "count"),
            Total_Profit=("Order Profit Per Order", "sum")
        ).reset_index()
        fig2 = px.bar(disc_impact, x="Discount Bracket", y="Avg_Margin",
                      color="Avg_Margin", color_continuous_scale="RdYlGn",
                      title="Avg Profit Margin % by Discount Bracket",
                      text=disc_impact["Avg_Margin"].apply(lambda x: f"{x:.1f}%"))
        fig2.add_hline(y=0, line_dash="dash", line_color="red")
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=400, plot_bgcolor="white", coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔬 What-If Discount Simulator")
    st.caption("Estimate profit impact of changing discount rate across all filtered orders.")
    sim_col1, sim_col2 = st.columns([1, 2])
    with sim_col1:
        new_disc = st.slider("Simulated Discount Rate", 0.0, 0.5,
                             float(df["Order Item Discount Rate"].mean()), 0.01)
    with sim_col2:
        current_profit   = df["Order Profit Per Order"].sum()
        current_revenue  = df["Sales"].sum()
        disc_change      = new_disc - df["Order Item Discount Rate"].mean()
        simulated_profit = current_profit - (disc_change * df["Order Item Product Price"] * df["Order Item Quantity"]).sum()
        delta            = simulated_profit - current_profit
        ca, cb, cc = st.columns(3)
        ca.metric("Current Profit",   f"${current_profit:,.0f}")
        cb.metric("Simulated Profit", f"${simulated_profit:,.0f}", f"${delta:+,.0f}")
        cc.metric("Simulated Margin", f"{simulated_profit/current_revenue*100:.1f}%" if current_revenue else "N/A")

    cat_disc = df.groupby("Category Name").agg(
        Avg_Discount=("Order Item Discount Rate", "mean"),
        Avg_Margin=("Profit Margin %", "mean")
    ).reset_index()
    fig3 = px.scatter(cat_disc, x="Avg_Discount", y="Avg_Margin", text="Category Name",
                      title="Category: Avg Discount Rate vs Avg Profit Margin",
                      color="Avg_Margin", color_continuous_scale="RdYlGn")
    fig3.update_traces(textposition="top center", textfont_size=9)
    fig3.add_hline(y=0, line_dash="dash", line_color="red")
    fig3.update_layout(height=420, plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — Market & Region
# ═════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Market & Regional Profit Analysis</div>', unsafe_allow_html=True)

    market_grp = df.groupby("Market").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
    ).reset_index()
    market_grp["Margin %"] = (market_grp["Profit"] / market_grp["Revenue"].replace(0, np.nan) * 100).round(1)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(market_grp.sort_values("Profit"),
                     x="Profit", y="Market", orientation="h",
                     color="Margin %", color_continuous_scale="RdYlGn",
                     title="Profit by Market", text="Margin %")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(height=380, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=market_grp["Market"], y=market_grp["Revenue"],
                              name="Revenue", marker_color="#1a6faf"))
        fig2.add_trace(go.Bar(x=market_grp["Market"], y=market_grp["Profit"],
                              name="Profit", marker_color="#22c55e"))
        fig2.update_layout(barmode="group", title="Revenue vs Profit by Market",
                           height=380, plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    reg_grp = df.groupby("Order Region").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
    ).reset_index()
    reg_grp["Margin %"] = (reg_grp["Profit"] / reg_grp["Revenue"].replace(0, np.nan) * 100).round(1)

    fig3 = px.treemap(reg_grp, path=["Order Region"], values="Revenue",
                      color="Margin %", color_continuous_scale="RdYlGn",
                      title="Revenue Treemap by Region (colour = Margin %)",
                      hover_data={"Profit": True, "Orders": True})
    fig3.update_layout(height=420)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Country-Level Profit Map")
    country_grp = df.groupby("Order Country").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Sales", "count"),
    ).reset_index()
    country_grp["Margin %"] = (country_grp["Profit"] / country_grp["Revenue"].replace(0, np.nan) * 100).round(1)
    fig4 = px.choropleth(country_grp, locations="Order Country", locationmode="country names",
                         color="Profit", hover_data=["Revenue", "Margin %", "Orders"],
                         color_continuous_scale="RdYlGn", title="Total Profit by Country")
    fig4.update_layout(height=500, geo=dict(showframe=False, showcoastlines=True))
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("#### Region × Category Profit Heatmap")
    rc_heat = df.pivot_table(index="Order Region", columns="Category Name",
                              values="Order Profit Per Order", aggfunc="sum")
    fig5 = px.imshow(rc_heat, color_continuous_scale="RdYlGn", aspect="auto",
                     title="Profit Heatmap: Region × Category",
                     labels=dict(color="Profit ($)"))
    fig5.update_layout(height=450)
    st.plotly_chart(fig5, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>🚢 APL Logistics Supply Chain Profitability Dashboard &nbsp;|&nbsp; "
    "Built by <a href='https://www.linkedin.com/in/arpita-sarkar-00921a225/' target='_blank'>Arpita Sarkar</a> "
    "&nbsp;|&nbsp; Unified Mentor Project &nbsp;|&nbsp; "
    "<a href='https://github.com/arpitasarkardata/supply-chain-profitability-analysis' target='_blank'>GitHub</a>"
    "</small></center>",
    unsafe_allow_html=True
)
