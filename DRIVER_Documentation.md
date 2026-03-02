# DCF Valuation Tool - DRIVER Documentation

### 1. Define
**Objective:** Create a Discounted Cash Flow (DCF) valuation tool using Streamlit that accepts any stock ticker (e.g., AAPL) and estimates its intrinsic value based on user-adjustable assumptions like WACC and Growth.
**Requirements:** 
- Automatically fetch financial data using `yfinance`.
- Calculate base metrics, project Free Cash Flows (FCF), discount them to present value, and compute Terminal Value.
- Show an Enterprise to Equity Value bridge and implied Per-Share Value.
- Include a dynamic sensitivity analysis matrix for WACC vs. Revenue Growth.

### 2. Represent
**Architecture:** 
The application was built entirely in Python using the Streamlit framework for instantaneous web UI rendering.
**Data Flow:**
User Input (Ticker) -> `yfinance` API Call -> Extract Current Revenue, Shares, Cash, Debt -> Compute 5-Year Projections (Revenue -> EBIT -> NOPAT ≈ FCF) -> Apply Gordon Growth for Terminal Value -> Present Outputs & Sensitivity Matrix using Pandas Styling.

### 3. Implement
**Code Structure:** 
We wrote `app.py` taking advantage of `streamlit` for the front end, `numpy` for range generation in the sensitivity matrix, and `pandas` for organizing the projection tables cleanly. We utilized Streamlit's `@st.cache_data` to ensure `yfinance` network requests are optimized and don't slow down the tool on every assumption tweak.

### 4. Validate
**Testing Strategy:** 
We ran the tool locally using the AAPL ticker.
- Validated that changing the WACC slider inversely impacts the valuation (Higher WACC = Lower PV).
- Validated that increasing Revenue Growth directly increases the Intrinsic Value.
- Checked the `yfinance` edge cases by providing fallbacks for missing data points on specific tickers.

### 5. Evolve
**Iterative Enhancements:** 
During development, we added a robust "Sensitivity Analysis" matrix. Why? Because DCFs are extremely sensitive to assumptions. A single point estimate is often wrong, but a range of estimates is practical. We evolved the initial layout into an interactive heatmap so the user can see worst-case and best-case scenarios instantly.

### 6. Reflect
**Final Thoughts & AI Usage:** 
The rapid prototyping of this complex financial model was made significantly smoother using AI assistance. The AI helped structure the nested loops required for generating the 5x5 sensitivity table and handled the styling of the Pandas DataFrame heatmap correctly. 
*Disclosure:* Generative AI (Google Deepmind Assistant) was used for structural scaffolding of the Python code, generating the `yfinance` caching logic, and drafting this DRIVER documentation template based on my project inputs.
