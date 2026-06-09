# 🚢 Supply Chain Profitability Analysis — APL Logistics

> **Customer, Product & Profitability Performance Analysis in Supply Chain Operations**
> Unified Mentor Data Analytics Project

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://arpitasarkardata-supply-chain-profitability-analysis.streamlit.app)

---

## 📌 Project Overview

A global logistics provider like APL Logistics handles thousands of orders daily — but **not all customers, products, or regions are equally profitable**. High revenue does not always mean high profit. Discounts and shipping costs can silently erode margins, and certain product categories may be loss-making.

This project delivers **financial clarity and margin intelligence** by answering:
- Which customers, products, and regions truly generate value?
- Where are discounts silently eroding profit margins?
- Which markets have strong revenue but weak profit?

---

## 📊 Live Dashboard

🔗 **[Launch Streamlit Dashboard →](https://arpitasarkardata-supply-chain-profitability-analysis.streamlit.app)**

### Dashboard Modules

| Tab | What It Shows |
|---|---|
| 📊 Revenue & Profit Overview | KPIs, segment comparison, profit distribution, delivery status |
| 👥 Customer Value | Top/bottom customers, tier segmentation, Pareto-style scatter |
| 📦 Product & Category | Category profit bars, bubble chart, risk matrix, heatmap |
| 🏷️ Discount Impact | Bracket analysis, what-if simulator, trendline scatter |
| 🌍 Market & Region | Market bars, region treemap, world choropleth map, heatmap |

---

## 📁 Repository Structure

```
supply-chain-profitability-analysis/
│
├── app.py                   ← Streamlit dashboard (5-tab interactive app)
├── APL_Logistics.csv        ← Dataset (~180,000 orders)
├── requirements.txt         ← Python dependencies
└── README.md                ← This file
```

---

## 🗂️ Dataset

| Field | Description |
|---|---|
| **Source** | APL Logistics (KWE Group) — via Unified Mentor |
| **Size** | ~180,000 orders |
| **Key Columns** | Sales, Order Profit Per Order, Order Item Discount Rate, Customer Segment, Category Name, Market, Order Region, Shipping Mode, Delivery Status |

---

## 📈 Key Performance Indicators

| KPI | Description |
|---|---|
| Total Revenue | Sum of all sales |
| Total Profit | Aggregate profit across all orders |
| Profit Margin % | Profit as a percentage of sales |
| Customer Value Index | Profit contribution per customer |
| Category Margin | Average margin by product category |
| Discount Impact Ratio | Margin loss attributable to discounts |

---

## 🔍 Analytical Methodology

1. **Data Cleaning & Financial Validation** — coerce numeric fields, remove invalid rows, engineer derived columns
2. **Revenue & Profit Overview** — segment-level and shipping-mode-level comparison
3. **Product & Category Analysis** — identify high-revenue/low-margin products and loss-making categories
4. **Customer Contribution Analysis** — tier segmentation, top/bottom customers, Pareto analysis
5. **Discount Impact Diagnostics** — bracket-wise margin analysis, what-if simulator
6. **Market & Regional Analysis** — choropleth map, treemap, region × category heatmap

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Pandas / NumPy | Data manipulation |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |
| Matplotlib / Seaborn | EDA charts (Colab) |

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/arpitasarkardata/supply-chain-profitability-analysis.git
cd supply-chain-profitability-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch dashboard
streamlit run app.py
```

---

## 👩‍💻 Author

**Arpita Sarkar**
B.Tech — Electronics & Communication Engineering
Kalyani Government Engineering College (MAKAUT) | CGPA: 7.87 | 2025

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/arpita-sarkar-00921a225/)
[![GitHub](https://img.shields.io/badge/GitHub-arpitasarkardata-black?logo=github)](https://github.com/arpitasarkardata)

---

## 📄 License

This project is for educational and portfolio purposes as part of the Unified Mentor Data Analytics program.
