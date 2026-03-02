# 🎥 DCF Valuation Tool - Video Presentation Transcript
*(Target Length: 8-12 minutes)*

---

### [0:00 - 1:00] 1. Introduction & Setup
*(Webcam view of student visible in the bottom corner of the screen recording)*

**Speaker:** 
"Hello everyone, today I'm presenting my Discounted Cash Flow (DCF) Valuation Application. The problem this app solves is that calculating a DCF from scratch in Excel is tedious, prone to manual errors, and makes testing different scenarios time-consuming. 

My Streamlit python app completely automates the data-fetching and calculation process. It takes a live stock ticker, pulls in current financial data dynamically from Yahoo Finance, and instantly calculates the intrinsic value. More importantly, it allows interactive sensitivity analysis so we can evaluate different 'what-if' scenarios."

---

### [1:00 - 3:00] 2. App Demo & Walkthrough
*(Screen recording showing the app, student types "AAPL" into the sidebar)*

**Speaker:**
"Let's look at the demo. I'm going to type 'AAPL' for Apple into the ticker box. 

Immediately, the app hits the `yfinance` API and retrieves Apple's base revenue, total cash, total debt, and shares outstanding. 
Right below, we see the DCF Outputs: Enterprise Value, Equity Value, and the Implied Share Price. Currently, based on the default assumptions we see on the left, the app predicts a specific price and compares it against Apple's live stock price to show us if it's overvalued or undervalued.

You can also see the 'Projected Cash Flows' table which shows Revenue, EBIT, and Free Cash Flow out to Year 5, along with the Discount Factor applied."

---

### [3:00 - 6:00] 3. Explaining the Key Assumptions (Hitting the Rubric)

**Speaker:**
"Now, let me explain the driving forces behind this model, specifically the 'Why' behind my inputs.

**1. How did I calculate WACC?**
For my base case, I used a WACC (Weighted Average Cost of Capital) of around 10%. Why? WACC is the minimum return investors expect. It's built from the Risk-Free Rate, Beta, and Equity Risk Premium, plus the Cost of Debt.
- *Risk-Free Rate:* I look at the 10-year US Treasury yield, which is roughly 4-4.5%.
- *Equity Risk Premium:* The extra return for investing in the stock market over bonds is historically around 5-6%. 
- *Beta:* Apple's Beta is around 1.1 to 1.2, meaning it's slightly more volatile than the market.
- *Cost of Debt:* The interest rate on their borrowing is relatively low, around 4-5%, and they have a low debt-to-equity ratio.
When you plug this into the CAPM formula (Risk-Free Rate + Beta * ERP), you arrive at roughly an 10% to 11% Cost of Equity, blending with Cost of Debt gets us to around 10%. This is highly reasonable for a mature tech giant like Apple. 

**2. Why this growth rate?**
In the sidebar, you'll see I set the 1-5 year Revenue Growth Rate to 5%. 
Why 5%? If we look at Apple's historical growth over the last 3-4 years, stripping out the COVID hardware boom, they've settled into single-digit revenue growth. Phone upgrade cycles are lengthening, and while Services are growing fast, Hardware makes up the majority of revenue. So, analyst estimates and industry outlooks suggest a sustained 4-6% growth rate is far more realistic than aggressive double-digit assumptions.

**3. How does my DCF calculation work?**
Let me walk you through the math the app does in the background:
First, I **project the cash flows** by taking today's revenue and growing it by my 5% assumption for Years 1 through 5. 
Next, I apply an operating margin and tax rate to arrive at NOPAT, which I use as a proxy for Unlevered Free Cash Flow.
Then, I **discount each year** back to present value using the WACC. You can see the Discount factor dropping in the table!
After Year 5, the company still exists, so we calculate the **Terminal Value** using the Gordon Growth Model—assuming a perpetual 2.5% growth rate—and discount that massive chunk back to today.
Finally, I **sum** the present value of the 5-year cash flows and the present value of the Terminal Value to get the *Enterprise Value*. To get the *Equity Value* for shareholders, I just add the company's Cash and subtract its Debt. Divide by shares, and that's the Implied Share Price!"

---

### [6:00 - 8:00] 4. Adjusting Assumptions Dynamically
*(Student is seen moving the sliders on the left)*

**Speaker:**
"But DCFs are just models; they're only as good as their inputs. Watch what happens when I adjust the assumptions. 
If I think Apple will launch an extremely successful new AI iPhone and bump growth to 10%, I slide it to the right. Instantly, the projected cash flows jump, and the Enterprise Value spikes. 
If the Federal Reserve raises interest rates, pushing my WACC up to 12%, I slide WACC up. Because we are discounting future money by a larger rate, the Present Value of the company drops drastically."

---

### [8:00 - 10:00] 5. Sensitivity Analysis

**Speaker:**
"Because guessing the exact WACC and Growth rate is impossible, the most valuable part of my app is the **Sensitivity Analysis** table at the bottom.

**What does this sensitivity analysis show?**
It shows the Implied Share Price across a grid of interconnected scenarios. The rows represent different WACCs, and the columns represent different Revenue Growth Rates. The app tests ranges specifically spanning ±2% from our base assumptions. 
This table proves which assumptions matter most. You can see moving vertically (changing WACC) causes a massive swing in the stock price—this represents the interest-rate sensitivity of the market. Moving horizontally (Growth) also creates price swings, but slightly less drastic in this model. 
For an investment decision, this heatmap tells me my 'margin of safety.' If the current stock price is only justified in the very top-right, dark-green cells (meaning I need high growth and low discount rates to break even), then the stock is likely overvalued and too risky. If the current price is easily beaten even in the red/yellow worst-case scenarios, it's a strong buy."

---

### [10:00 - 11:00] 6. Conclusion & AI Disclosure

**Speaker:**
"To wrap up, this tool brings financial theory to life dynamically. 

Finally, per the course guidelines, I would like to include my **AI Usage Disclosure**:
I utilized Generative AI (Google Deepmind Assistant) to help build this project. While I provided the financial logic, mathematical architecture, and directed the design, the AI assisted in formatting the Python Streamlit code, specifically writing the `yfinance` data extraction functions and scaffolding the pandas dataframe logic for the color-coded sensitivity heat map.

Thank you for your time, and I hope you enjoyed the tool!"

--- 
*(End of Recording)*
