import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Personal Finance & Economics Portfolio App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title & Header
st.title("💰 Interactive Personal Finance & Economics Hub")
st.markdown("""
Welcome to your interactive portfolio web application! This application covers core concepts in personal finance, 
investing, debt management, tax planning, and interactive financial calculators—grounded in real-world financial frameworks and Indian tax laws.
""")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
module = st.sidebar.radio(
    "Choose a Module:",
    [
        "1. Cash Flow & Emergency Fund",
        "2. Debt Snowball vs. Avalanche",
        "3. Asset Allocation & Compound Growth",
        "4. Indian Tax Optimizer & Capital Gains",
        "5. Financial Calculators Suite (SIP, EMI & HRA)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Portfolio Project Tip**: You can deploy this app for free on Streamlit Community Cloud using your GitHub repository.")

# ==========================================
# MODULE 1: CASH FLOW & EMERGENCY FUND
# ==========================================
if module == "1. Cash Flow & Emergency Fund":
    st.header("💵 Module 1: Cash Flow & Emergency Fund Simulator")
    st.write("Understand the **50/30/20 Budgeting Framework** and build financial resilience with an **Emergency Reserve**.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚙️ Input Your Monthly Income & Fixed Costs")
        monthly_income = st.number_input("Monthly Take-Home Income (₹ / $)", min_value=1000, value=60000, step=5000)
        currency = st.selectbox("Currency Symbol", ["₹", "$", "€"])

        st.markdown("### 📊 50/30/20 Budget Allocation")
        st.write("The 50/30/20 rule allocates your net income into three primary categories:")
        
        needs_target = monthly_income * 0.50
        wants_target = monthly_income * 0.30
        savings_target = monthly_income * 0.20

        st.metric(label="Essentials / Needs (50%)", value=f"{currency}{needs_target:,.2f}", help="Housing, utilities, groceries, basic transport")
        st.metric(label="Wants & Lifestyle (30%)", value=f"{currency}{wants_target:,.2f}", help="Dining out, entertainment, hobbies")
        st.metric(label="Savings & Debt Repayment (20%)", value=f"{currency}{savings_target:,.2f}", help="Emergency fund, investments, extra debt payments")

    with col2:
        st.subheader("🥧 Budget Allocation Visualizer")
        budget_df = pd.DataFrame({
            "Category": ["Needs (50%)", "Wants (30%)", "Savings & Debt (20%)"],
            "Amount": [needs_target, wants_target, savings_target]
        })
        fig = px.pie(budget_df, values="Amount", names="Category", color_discrete_sequence=["#2b5c8f", "#d95f02", "#2ca02c"], title="50/30/20 Monthly Breakdown")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🛡️ Emergency Fund Target Calculator")
    st.write("An emergency fund protects you against unplanned expenses (medical, job loss, car repair) without going into high-interest debt.")

    col_ef1, col_ef2 = st.columns(2)
    with col_ef1:
        essential_expenses = st.number_input("Essential Monthly Expenses (Needs)", min_value=500, value=int(needs_target), step=1000)
        target_months = st.slider("Target Buffer (Months of Expenses)", min_value=1, max_value=12, value=6)
        current_savings = st.number_input("Current Liquid Savings", min_value=0, value=50000, step=5000)

    target_ef = essential_expenses * target_months
    shortfall = max(0, target_ef - current_savings)

    with col_ef2:
        st.markdown(f"#### Target Reserve: **{currency}{target_ef:,.2f}**")
        if current_savings >= target_ef:
            st.success("🎉 Congratulations! Your emergency fund is fully funded.")
        else:
            st.warning(f"⚠️ You need **{currency}{shortfall:,.2f}** more to reach your {target_months}-month safety net.")
            monthly_contribution = st.number_input("Monthly Contribution towards Emergency Fund", min_value=500, value=int(savings_target), step=500)
            if monthly_contribution > 0:
                months_needed = int(np.ceil(shortfall / monthly_contribution))
                st.info(f"⏳ At {currency}{monthly_contribution:,.2f}/month, you will reach your goal in **{months_needed} months**.")


# ==========================================
# MODULE 2: DEBT SNOWBALL VS AVALANCHE
# ==========================================
elif module == "2. Debt Snowball vs. Avalanche":
    st.header("⚡ Module 2: Debt Payoff Simulator (Snowball vs. Avalanche)")
    st.write("Compare the **Debt Avalanche** (mathematically saves the most interest) vs. **Debt Snowball** (psychological quick wins).")

    st.subheader("📋 Enter Your Debts")
    
    default_debts = pd.DataFrame([
        {"Debt Name": "Credit Card A", "Balance": 50000, "Interest Rate (%)": 24.0, "Min Payment": 2500},
        {"Debt Name": "Personal Loan", "Balance": 150000, "Interest Rate (%)": 14.0, "Min Payment": 4000},
        {"Debt Name": "Auto Loan", "Balance": 300000, "Interest Rate (%)": 8.5, "Min Payment": 7000}
    ])

    edited_debts = st.data_editor(default_debts, num_rows="dynamic")
    extra_monthly_budget = st.number_input("Extra Monthly Payment Budget beyond Minimums (₹ / $)", min_value=0, value=5000, step=500)

    def simulate_payoff(df_debts, strategy="Avalanche", extra_budget=0):
        debts = df_debts.copy()
        debts["Balance"] = debts["Balance"].astype(float)
        debts["Interest Rate (%)"] = debts["Interest Rate (%)"].astype(float)
        debts["Min Payment"] = debts["Min Payment"].astype(float)

        total_interest_paid = 0
        months = 0
        history = []

        while debts["Balance"].sum() > 0 and months < 360:
            months += 1
            # Calculate monthly interest
            debts["Monthly Interest"] = debts["Balance"] * (debts["Interest Rate (%)"] / 100 / 12)
            total_interest_paid += debts["Monthly Interest"].sum()
            debts["Balance"] += debts["Monthly Interest"]

            # Pay minimums
            for idx, row in debts.iterrows():
                if row["Balance"] > 0:
                    payment = min(row["Balance"], row["Min Payment"])
                    debts.loc[idx, "Balance"] -= payment

            # Apply extra budget according to strategy
            active_debts = debts[debts["Balance"] > 0]
            if not active_debts.empty:
                if strategy == "Avalanche":
                    target_idx = active_debts.sort_values(by="Interest Rate (%)", ascending=False).index[0]
                else: # Snowball
                    target_idx = active_debts.sort_values(by="Balance", ascending=True).index[0]

                extra_payment = extra_budget
                actual_extra = min(debts.loc[target_idx, "Balance"], extra_payment)
                debts.loc[target_idx, "Balance"] -= actual_extra

            history.append({"Month": months, "Total Remaining Balance": debts["Balance"].sum()})

        return months, total_interest_paid, pd.DataFrame(history)

    if st.button("🚀 Run Debt Payoff Simulation"):
        m_av, int_av, hist_av = simulate_payoff(edited_debts, strategy="Avalanche", extra_budget=extra_monthly_budget)
        m_sn, int_sn, hist_sn = simulate_payoff(edited_debts, strategy="Snowball", extra_budget=extra_monthly_budget)

        col_a, col_b = st.columns(2)
        with col_a:
            st.success("🏔️ **Debt Avalanche Strategy**")
            st.metric("Total Months to Debt-Free", f"{m_av} Months")
            st.metric("Total Interest Paid", f"₹ / ${int_av:,.2f}")
            st.caption("Targets highest interest rate first -> Minimizes total cost.")

        with col_b:
            st.info("❄️ **Debt Snowball Strategy**")
            st.metric("Total Months to Debt-Free", f"{m_sn} Months")
            st.metric("Total Interest Paid", f"₹ / ${int_sn:,.2f}")
            st.caption("Targets lowest balance first -> Maximizes psychological motivation.")

        st.subheader("📈 Payoff Trajectory Comparison")
        hist_av["Strategy"] = "Avalanche"
        hist_sn["Strategy"] = "Snowball"
        combined_hist = pd.concat([hist_av, hist_sn])

        fig_debt = px.line(combined_hist, x="Month", y="Total Remaining Balance", color="Strategy",
                           title="Remaining Debt Balance Over Time",
                           color_discrete_map={"Avalanche": "#2ca02c", "Snowball": "#d95f02"})
        st.plotly_chart(fig_debt, use_container_width=True)

        if int_av < int_sn:
            diff = int_sn - int_av
            st.markdown(f"💡 **Key Insight**: The **Avalanche method saves you {diff:,.2f}** in total interest compared to the Snowball method!")


# ==========================================
# MODULE 3: ASSET ALLOCATION & COMPOUND GROWTH
# ==========================================
elif module == "3. Asset Allocation & Compound Growth":
    st.header("📈 Module 3: Wealth Building & Asset Allocation")
    st.write("Visualize the exponential power of **Compound Interest** and design an age-appropriate **Asset Allocation**.")

    tab1, tab2 = st.tabs(["🚀 Compound Interest Simulator", "📊 Asset Allocation Framework"])

    with tab1:
        st.subheader("Compound Interest Growth Engine")
        col_c1, col_c2 = st.columns([1, 1])

        with col_c1:
            initial_inv = st.number_input("Initial Investment (₹ / $)", min_value=0, value=100000, step=10000)
            monthly_contrib = st.number_input("Monthly Contribution (₹ / $)", min_value=0, value=10000, step=1000)
            annual_return = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
            years = st.slider("Investment Horizon (Years)", min_value=1, max_value=40, value=25)

        # Calculation
        months = years * 12
        r_monthly = (annual_return / 100) / 12
        
        balance_history = []
        curr_balance = initial_inv
        total_principal = initial_inv

        for m in range(1, months + 1):
            curr_balance = (curr_balance + monthly_contrib) * (1 + r_monthly)
            total_principal += monthly_contrib
            if m % 12 == 0:
                balance_history.append({
                    "Year": m // 12,
                    "Total Value": curr_balance,
                    "Total Contributions": total_principal,
                    "Compound Growth (Interest)": curr_balance - total_principal
                })

        df_compound = pd.DataFrame(balance_history)

        with col_c2:
            st.metric("Final Portfolio Value", f"₹ / ${curr_balance:,.2f}")
            st.metric("Total Out-of-Pocket Contributions", f"₹ / ${total_principal:,.2f}")
            st.metric("Total Compound Wealth Earned", f"₹ / ${curr_balance - total_principal:,.2f}")

        fig_compound = px.bar(df_compound, x="Year", y=["Total Contributions", "Compound Growth (Interest)"],
                               title="Growth of Wealth Over Time (Principal vs Interest)",
                               barmode="stack", color_discrete_sequence=["#1f77b4", "#2ca02c"])
        st.plotly_chart(fig_compound, use_container_width=True)

    with tab2:
        st.subheader("Asset Allocation Guidelines")
        st.write("Asset allocation spreads investments across **Stocks** (growth/volatility), **Bonds** (stability/income), and **Cash** (liquidity).")

        age = st.slider("Your Current Age", min_value=18, max_value=80, value=25)
        risk_profile = st.select_slider("Risk Tolerance", options=["Conservative", "Moderate", "Aggressive"], value="Moderate")

        # Basic asset allocation logic
        if risk_profile == "Aggressive":
            stock_pct = max(20, 110 - age)
            bond_pct = max(0, 100 - stock_pct - 10)
            cash_pct = 100 - stock_pct - bond_pct
        elif risk_profile == "Moderate":
            stock_pct = max(10, 100 - age)
            bond_pct = max(0, 100 - stock_pct - 10)
            cash_pct = 100 - stock_pct - bond_pct
        else:
            stock_pct = max(10, 80 - age)
            bond_pct = max(10, 100 - stock_pct - 10)
            cash_pct = 100 - stock_pct - bond_pct

        alloc_df = pd.DataFrame({
            "Asset Class": ["Stocks / Equity Index Funds", "Bonds / Fixed Income", "Cash & Emergency Reserve"],
            "Allocation (%)": [stock_pct, bond_pct, cash_pct]
        })

        fig_alloc = px.pie(alloc_df, values="Allocation (%)", names="Asset Class",
                           color_discrete_sequence=["#d95f02", "#1f77b4", "#7570b3"],
                           title=f"Suggested Portfolio Mix for Age {age} ({risk_profile} Profile)")
        st.plotly_chart(fig_alloc, use_container_width=True)


# ==========================================
# MODULE 4: INDIAN TAXATION & CAPITAL GAINS
# ==========================================
elif module == "4. Indian Tax Optimizer & Capital Gains":
    st.header("🏛️ Module 4: Indian Tax Regime & Capital Gains Calculator")
    st.write("Navigate the **New Tax Regime (Section 115BAC - AY 2026-27)** vs **Old Tax Regime**, and estimate **Capital Gains Tax**.")

    tab_tax1, tab_tax2 = st.tabs(["🧮 New vs. Old Tax Regime Switcher", "📊 Mutual Fund & Capital Gains Tax"])

    with tab_tax1:
        st.subheader("Income Tax Calculator (Salaried Individuals AY 2026-27)")
        gross_salary = st.number_input("Gross Annual Salary Income (₹)", min_value=0, value=1200000, step=50000)

        col_ded1, col_ded2 = st.columns(2)
        with col_ded1:
            st.markdown("#### Old Regime Exemptions & Deductions")
            sec_80c = st.number_input("Section 80C (PPF, ELSS, EPF, LIC) [Max ₹1.5L]", min_value=0, max_value=150000, value=150000, step=10000)
            sec_80d = st.number_input("Section 80D (Health Insurance)", min_value=0, max_value=100000, value=25000, step=5000)
            hra = st.number_input("House Rent Allowance (HRA) Exemption", min_value=0, value=100000, step=10000)
            std_ded_old = 50000

        with col_ded2:
            st.markdown("#### New Regime Deductions")
            std_ded_new = 75000  # Updated Standard Deduction for AY 2026-27
            st.info(f"Standard Deduction under New Regime: **₹{std_ded_new:,.0f}**")
            st.caption("Note: Section 80C, 80D, HRA are NOT available under the New Tax Regime.")

        # Compute Old Regime Tax
        taxable_old = max(0, gross_salary - std_ded_old - sec_80c - sec_80d - hra)
        def calc_old_tax(income):
            tax = 0
            if income > 1000000:
                tax += (income - 1000000) * 0.30 + 112500
            elif income > 500000:
                tax += (income - 500000) * 0.20 + 12500
            elif income > 250000:
                tax += (income - 250000) * 0.05
            # Sec 87A rebate for Old regime up to 5L taxable
            if income <= 500000:
                tax = 0
            return tax * 1.04 # 4% Health & Ed Cess

        # Compute New Regime Tax (AY 2026-27 / FY 2025-26 Slabs)
        taxable_new = max(0, gross_salary - std_ded_new)
        def calc_new_tax(income):
            # Slabs: 0-4L Nil, 4-8L 5%, 8-12L 10%, 12-16L 15%, 16-20L 20%, 20-24L 25%, >24L 30%
            tax = 0
            if income > 2400000:
                tax += (income - 2400000) * 0.30 + 300000
            elif income > 2000000:
                tax += (income - 2000000) * 0.20 + 220000
            elif income > 1600000:
                tax += (income - 1600000) * 0.15 + 160000
            elif income > 1200000:
                tax += (income - 1200000) * 0.10 + 120000
            elif income > 800000:
                tax += (income - 800000) * 0.10 + 40000
            elif income > 400000:
                tax += (income - 400000) * 0.05

            # Sec 87A Rebate for New Regime taxable income up to ₹7,00,000 threshold
            if income <= 700000:
                tax = 0

            return tax * 1.04 # 4% Cess

        tax_old = calc_old_tax(taxable_old)
        tax_new = calc_new_tax(taxable_new)

        st.markdown("---")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Old Regime Tax Liability", f"₹{tax_old:,.2f}")
            st.caption(f"Taxable Income: ₹{taxable_old:,.2f}")

        with col_res2:
            st.metric("New Regime Tax Liability (Default)", f"₹{tax_new:,.2f}")
            st.caption(f"Taxable Income: ₹{taxable_new:,.2f}")

        if tax_new < tax_old:
            st.success(f"🎉 The **New Tax Regime saves you ₹{tax_old - tax_new:,.2f}** in income tax!")
        elif tax_old < tax_new:
            st.success(f"🎉 The **Old Tax Regime saves you ₹{tax_new - tax_old:,.2f}** due to your deductions!")
        else:
            st.info("Both regimes result in the same tax liability for your income level.")

    with tab_tax2:
        st.subheader("Equity & Debt Mutual Fund Capital Gains Tax Estimator")
        st.write("Tax rules for mutual funds depend on asset class (Equity vs. Debt) and holding period.")

        asset_class = st.radio("Asset Category", ["Equity Oriented Mutual Funds / Stocks", "Debt Mutual Funds"])
        purchase_price = st.number_input("Total Purchase Cost (₹)", min_value=1000, value=200000, step=10000)
        sale_price = st.number_input("Total Sale Value (₹)", min_value=1000, value=350000, step=10000)
        holding_months = st.number_input("Holding Period (Months)", min_value=1, value=18, step=1)

        gain = max(0, sale_price - purchase_price)
        st.write(f"Total Capital Gain Realized: **₹{gain:,.2f}**")

        if asset_class == "Equity Oriented Mutual Funds / Stocks":
            if holding_months <= 12:
                st.info("classified as **Short-Term Capital Gain (STCG)** (Holding <= 12 months)")
                tax_rate = 0.20 # 20% STCG
                tax_due = gain * tax_rate
                st.metric("STCG Tax Payable (20%)", f"₹{tax_due:,.2f}")
            else:
                st.info("classified as **Long-Term Capital Gain (LTCG)** (Holding > 12 months)")
                exemption_limit = 125000 # ₹1.25 Lakh LTCG exemption
                taxable_gain = max(0, gain - exemption_limit)
                tax_rate = 0.125 # 12.5% LTCG
                tax_due = taxable_gain * tax_rate
                st.metric("LTCG Tax Payable (12.5% above ₹1.25L Exemption)", f"₹{tax_due:,.2f}")
                st.caption(f"Exempt Gain: ₹{min(gain, exemption_limit):,.2f} | Taxable Gain: ₹{taxable_gain:,.2f}")
        else:
            st.info("classified as **Debt Mutual Fund Gain**")
            st.write("Note: Gains on debt mutual funds are added to your total income and taxed as per your **Individual Income Slab Rate**.")


# ==========================================
# MODULE 5: FINANCIAL CALCULATORS SUITE
# ==========================================
elif module == "5. Financial Calculators Suite (SIP, EMI & HRA)":
    st.header("🧮 Module 5: Interactive Financial Calculators Suite")
    st.write("A collection of essential everyday financial calculators to support practical decision-making.")

    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "📈 Step-Up SIP Calculator", 
        "🏦 Loan EMI & Affordability Calculator", 
        "🏠 HRA Tax Exemption Calculator"
    ])

    # --- TAB 1: STEP-UP SIP CALCULATOR ---
    with calc_tab1:
        st.subheader("Step-Up Systematic Investment Plan (SIP) Calculator")
        st.write("As your career progresses, your income grows. A **Step-Up SIP** increases your monthly investment annually by a fixed percentage.")

        col_sip1, col_sip2 = st.columns(2)
        with col_sip1:
            initial_sip = st.number_input("Starting Monthly SIP Amount (₹ / $)", min_value=500, value=5000, step=500)
            annual_stepup = st.slider("Annual Step-Up Rate (%)", min_value=0, max_value=25, value=10, step=1, help="Percentage by which your SIP increases every year")
            sip_return = st.slider("Expected Annual Return Rate (%)", min_value=1.0, max_value=20.0, value=12.0, step=0.5)
            sip_years = st.slider("Investment Duration (Years)", min_value=1, max_value=35, value=20)

        # Calculation
        monthly_rate = (sip_return / 100) / 12
        total_months = sip_years * 12
        
        yearly_breakdown = []
        current_sip = initial_sip
        accumulated_corpus = 0
        total_invested = 0

        for year in range(1, sip_years + 1):
            year_invested = 0
            for m in range(12):
                accumulated_corpus = (accumulated_corpus + current_sip) * (1 + monthly_rate)
                total_invested += current_sip
                year_invested += current_sip
            
            yearly_breakdown.append({
                "Year": year,
                "Monthly SIP": current_sip,
                "Total Invested": total_invested,
                "Corpus Value": accumulated_corpus,
                "Wealth Gain": accumulated_corpus - total_invested
            })
            # Increase SIP for next year
            current_sip = current_sip * (1 + annual_stepup / 100)

        df_sip = pd.DataFrame(yearly_breakdown)

        with col_sip2:
            st.metric("Final Accumulated Wealth Corpus", f"₹ / ${accumulated_corpus:,.2f}")
            st.metric("Total Out-of-Pocket Invested", f"₹ / ${total_invested:,.2f}")
            st.metric("Net Wealth Multiplication Factor", f"{(accumulated_corpus / total_invested):.2f}x")

            fig_sip = px.area(
                df_sip, x="Year", y=["Total Invested", "Corpus Value"],
                title=f"Step-Up SIP Corpus Trajectory ({annual_stepup}% Annual Step-Up)",
                color_discrete_map={"Total Invested": "#1f77b4", "Corpus Value": "#2ca02c"}
            )
            st.plotly_chart(fig_sip, use_container_width=True)

    # --- TAB 2: LOAN EMI & AFFORDABILITY CALCULATOR ---
    with calc_tab2:
        st.subheader("Loan Equated Monthly Installment (EMI) & Affordability Engine")
        st.write("Calculate your monthly EMI, total interest payable, and evaluate whether a loan fits comfortably within your income.")

        col_emi1, col_emi2 = st.columns(2)
        with col_emi1:
            loan_amount = st.number_input("Loan Amount (Principal) (₹ / $)", min_value=10000, value=1000000, step=50000)
            interest_rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, max_value=30.0, value=8.5, step=0.1)
            tenure_years = st.slider("Loan Tenure (Years)", min_value=1, max_value=30, value=15)
            monthly_income_emi = st.number_input("Your Net Monthly Income (₹ / $)", min_value=10000, value=80000, step=5000)

        # EMI Calculation: E = P * r * (1+r)^n / ((1+r)^n - 1)
        r = (interest_rate / 100) / 12
        n = tenure_years * 12
        emi = (loan_amount * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)
        total_payment = emi * n
        total_interest = total_payment - loan_amount
        foir_pct = (emi / monthly_income_emi) * 100

        with col_emi2:
            st.metric("Monthly EMI Payable", f"₹ / ${emi:,.2f}")
            st.metric("Total Interest Payable", f"₹ / ${total_interest:,.2f}")
            st.metric("Total Amount Paid (Principal + Interest)", f"₹ / ${total_payment:,.2f}")

            # Affordability check (FOIR guideline: <= 40% of income)
            st.markdown(f"**Debt-to-Income / FOIR Ratio**: **{foir_pct:.1f}%**")
            if foir_pct <= 35:
                st.success("🟢 **Comfortably Affordable**: EMI is below 35% of your monthly income.")
            elif foir_pct <= 50:
                st.warning("🟡 **Moderate Stretch**: EMI is between 35% and 50% of your monthly income. Keep other expenses low.")
            else:
                st.error("🔴 **High Financial Strain**: EMI exceeds 50% of your income. Consider reducing loan size or extending tenure.")

            emi_pie_df = pd.DataFrame({
                "Component": ["Principal Loan Amount", "Total Interest Paid"],
                "Amount": [loan_amount, total_interest]
            })
            fig_emi = px.pie(emi_pie_df, values="Amount", names="Component", color_discrete_sequence=["#1f77b4", "#d95f02"], title="Principal vs Interest Breakdown")
            st.plotly_chart(fig_emi, use_container_width=True)

    # --- TAB 3: HRA TAX EXEMPTION CALCULATOR ---
    with calc_tab3:
        st.subheader("House Rent Allowance (HRA) Tax Exemption Calculator (Section 10(13A))")
        st.write("Calculate your exact tax-exempt HRA amount under Old Tax Regime rules using statutory Income Tax limits.")

        col_hra1, col_hra2 = st.columns(2)
        with col_hra1:
            basic_salary = st.number_input("Annual Basic Salary + DA (₹)", min_value=50000, value=600000, step=25000)
            hra_received = st.number_input("Annual HRA Received from Employer (₹)", min_value=0, value=240000, step=10000)
            annual_rent = st.number_input("Actual Annual Rent Paid (₹)", min_value=0, value=210000, step=10000)
            city_type = st.radio("Residing City Classification", ["Metro City (Mumbai, Delhi, Kolkata, Chennai)", "Non-Metro City"])

        # Statutory HRA Exemption Rules:
        # Exempt HRA is MINIMUM of:
        # 1. Actual HRA received
        # 2. 50% of Basic Salary (Metro) or 40% of Basic Salary (Non-Metro)
        # 3. Actual Rent Paid minus 10% of Basic Salary

        metro_pct = 0.50 if "Metro" in city_type else 0.40
        limit1 = hra_received
        limit2 = basic_salary * metro_pct
        limit3 = max(0, annual_rent - (0.10 * basic_salary))

        exempt_hra = min(limit1, limit2, limit3)
        taxable_hra = max(0, hra_received - exempt_hra)

        with col_hra2:
            st.markdown("#### 📐 Statutory Calculations under Sec 10(13A):")
            st.write(f"1. Actual HRA Received: **₹{limit1:,.2f}**")
            st.write(f"2. {int(metro_pct*100)}% of Basic Salary: **₹{limit2:,.2f}**")
            st.write(f"3. Rent Paid - 10% of Basic Salary: **₹{limit3:,.2f}**")

            st.markdown("---")
            st.metric("Tax-Exempt HRA Amount", f"₹{exempt_hra:,.2f}")
            st.metric("Taxable HRA Amount (Added to Gross Income)", f"₹{taxable_hra:,.2f}")

            if exempt_hra == hra_received:
                st.success("🎉 Your entire HRA is 100% tax-exempt!")
            else:
                st.info(f"💡 You save tax on **₹{exempt_hra:,.2f}**, and **₹{taxable_hra:,.2f}** is included in your taxable income under the Old Tax Regime.")
