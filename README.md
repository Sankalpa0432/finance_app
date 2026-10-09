# 💰 FinLearn: Interactive Personal Finance & Indian Tax Portfolio Web App

A production-ready, interactive financial education, calculator suite, and tax optimization web application built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. 

This application bridges personal financial literacy (budgeting, emergency reserves, debt elimination, compound growth, SIP & EMI calculators) with real-world tax planning under the **Indian Income Tax Act (AY 2026–27)**, **Capital Gains tax framework**, and **HRA exemption rules**.

---

## 🌟 Key Features & Modules

### 1. 💵 Cash Flow & Emergency Reserve Simulator
* **50/30/20 Budgeting Benchmark**: Automatically categorizes monthly income into **50% Needs**, **30% Wants**, and **20% Savings/Debt Repayment**.
* **Emergency Fund Calculator**: Computes a target liquid reserve covering **3 to 6 months of essential living expenses** to absorb financial shocks without accumulating high-interest debt.
* **Savings Gap Analysis**: Projects the exact timeline (in months) required to achieve a fully funded emergency reserve based on current monthly savings.

### 2. ⚡ Debt Elimination Engine (Snowball vs. Avalanche)
* **Debt Avalanche Method**: Prioritizes liabilities by highest interest rate first to mathematically minimize total interest paid over time.
* **Debt Snowball Method**: Prioritizes liabilities by smallest balance first to generate quick psychological wins and momentum.
* **Side-by-Side Simulation**: Runs month-by-month rollover payoff trajectories with interactive line charts comparing overall timeline and total interest savings.

### 3. 📈 Asset Allocation & Compound Growth Visualizer
* **Multi-Decade Growth Projections**: Simulates initial deposits and recurring monthly SIP contributions over 5 to 50 year horizons using compound interest mechanics.
* **Risk & Age-Adjusted Allocation**: Spreads portfolio weight across **Equities** (growth), **Bonds/Fixed Income** (stability), and **Cash** (safety).
* **Interactive Area Chart**: Visualizes principal invested vs. cumulative compound interest gains over time.

### 4. 🇮🇳 Indian Tax Optimizer (AY 2026–27)
* **Income Tax Regime Switcher**: Compares the default **Section 115BAC New Tax Regime** (AY 2026–27 slabs: 0–4L Nil, 4–8L 5%, 8–12L 10%, 12–16L 15%, 16–20L 20%, 20–24L 25%, >24L 30% with ₹75,000 standard deduction and Section 87A rebate) against the **Old Tax Regime** with Chapter VI-A deductions (Section 80C, 80D, HRA).
* **Capital Gains Tax Estimator**: Computes **Short-Term Capital Gains (STCG at 20%)** and **Long-Term Capital Gains (LTCG at 12.5% above ₹1.25 lakh)** for equity mutual funds and stocks, alongside slab-rate taxation for post-April 2023 debt mutual funds.

### 5. 🧮 Interactive Financial Calculators Suite
* **Step-Up SIP Calculator**: Projects wealth accumulation when monthly investment contributions increase annually by a fixed percentage (e.g. 5%–20% step-up with annual salary raises).
* **Loan EMI & Affordability Engine**: Calculates exact Equated Monthly Installments (EMI), principal vs. interest breakdown pie chart, and checks loan affordability against a 35%–50% Debt-to-Income / FOIR ratio threshold.
* **HRA Tax Exemption Calculator**: Computes exact Section 10(13A) tax-exempt House Rent Allowance based on the 3 statutory Income Tax limits (Actual HRA, Rent - 10% Basic, 50%/40% Basic Salary).

---

## 🛠️ Tech Stack & Architecture

* **Frontend / UI**: [Streamlit](https://streamlit.io/) (Python Web Framework)
* **Data Processing & Math Engine**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Data Visualization**: [Plotly Express & Graph Objects](https://plotly.com/python/)
* **Language**: Python 3.10+

---

## 🚀 Quickstart & Local Setup

### Prerequisites
Ensure you have Python 3.10 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/finlearn-portfolio-app.git
cd finlearn-portfolio-app
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas numpy plotly
```

### 4. Run the Application
```bash
streamlit run finance_portfolio_app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🌐 Deploying to Streamlit Community Cloud (Free)

You can deploy this application live to share on your resume and portfolio in less than two minutes:

1. Push your code to a public **GitHub** repository (ensure `finance_portfolio_app.py` and a `requirements.txt` file are present).
2. Create a free account at [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New App"**, select your GitHub repository, set the main file path to `finance_portfolio_app.py`, and click **"Deploy"**.
4. Your application will be live at a custom URL (e.g., `https://finlearn-app.streamlit.app`)!

---

## 📚 References & Grounding

The mathematical models and legal frameworks implemented in this application are grounded in official financial and tax publications:
* **Budgeting & Reserves**: Consumer Financial Protection Bureau (CFPB) & UNFCU 50/30/20 standard [2, 5].
* **Debt Payoff Mechanics**: Fidelity Investments & Wells Fargo debt management guides [6, 18].
* **Investing & Asset Allocation**: SEC Investor.gov & iShares by BlackRock [3, 8, 9].
* **Indian Taxation & Laws**: Income Tax Department of India (AY 2026–27), CBDT guidelines, and Ministry of Finance publications [1, 7, 10, 14, 15, 17, 19].

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
