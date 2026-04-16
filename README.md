[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Pandas](https://img.shields.io/badge/Pandas-2.1.3-yellow.svg)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24.1-orange.svg)](https://plotly.com/)
[![Code style](https://img.shields.io/badge/Code%20Style-PEP%208-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

# 📊 Valuation Suite - Complete Company Valuation Toolkit

A professional, interactive valuation dashboard built with Python and Streamlit. Perform Enterprise Value (EV), Comparable Company Analysis (Comps), and Discounted Cash Flow (DCF) valuations for any public company.

## 🚀 Live Demo

[https://company-valuation-suite-yqnknmx67cectkmnqmfouf.streamlit.app/]

## 📋 Features

### 1️⃣ Beginner: Enterprise Value & Multiples
- Calculate Enterprise Value (EV) using: `EV = Market Cap + Debt - Cash`
- Compute valuation multiples: EV/Revenue, EV/EBITDA (LTM & FY1)
- 52-week EV range analysis (High/Low/Average)
- Auto-fetch live stock data from Yahoo Finance
- Upload custom CSV for historical data

### 2️⃣ Intermediate: Comparable Company Analysis (Comps)
- Value any company using peer multiples
- Add peers via CSV upload or manual entry
- Calculate EV/Revenue and EV/EBITDA for each peer
- Generate statistics: High, Mean, Median, Low
- Apply peer multiples to target company
- Sample data pre-loaded for immediate testing

### 3️⃣ Advanced: Discounted Cash Flow (DCF) Model
- Full DCF valuation with 5-year projections
- WACC calculation (Cost of Equity + Cost of Debt)
- Free Cash Flow projections
- Terminal Value using perpetuity growth
- Sensitivity analysis table (WACC vs Growth Rate)
- Export results to Excel or CSV
- Scenario management framework

### 4️⃣ Football Field
- Combine all three valuation methods
- Visualize valuation ranges
- Automatic interpretation and verdict
- Save and load results across dashboards

### 5️⃣ User Guide
- Step-by-step data sourcing instructions
- Industry benchmark multiples
- Interpretation framework
- Common mistakes to avoid

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core language |
| Streamlit | Web framework & UI |
| Pandas | Data manipulation |
| NumPy | Numerical calculations |
| Plotly | Interactive charts |
| yfinance | Live stock data |
| OpenPyXL | Excel export |

## 🚀 Installation & Running Locally

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step 1: Clone or download the repository
```bash
git clone https://github.com/yourusername/valuation-suite.git
cd valuation-suite

bash
pip install -r requirements.txt

bash
streamlit run master_launcher.py
