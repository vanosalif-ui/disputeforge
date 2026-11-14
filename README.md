# ⚡ DisputeForge — AI Chargeback & Dispute Defense Pack Generator

[![Live Demo](https://img.shields.io/badge/Live_App-vanosalif--ui.github.io%2Fdisputeforge-indigo?style=for-the-badge&logo=github)](https://vanosalif-ui.github.io/disputeforge/)
[![Visa CE 3.0 Ready](https://img.shields.io/badge/Visa_CE_3.0-Compliant-emerald?style=for-the-badge)](https://vanosalif-ui.github.io/disputeforge/)
[![Mastercard Rules](https://img.shields.io/badge/Mastercard_Dispute-Supported-orange?style=for-the-badge)](https://vanosalif-ui.github.io/disputeforge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> **DisputeForge** is a production-grade B2B SaaS tool designed to help e-commerce merchants (Shopify, WooCommerce, Stripe, PayPal) defend against and overturn illegitimate chargebacks ("friendly fraud") with bank-ready evidence dossiers.

👉 **Launch the Web App Live:** **[https://vanosalif-ui.github.io/disputeforge/](https://vanosalif-ui.github.io/disputeforge/)**

---

## 🎯 The Problem
Merchants lose over **$100 Billion** annually to friendly fraud (customers claiming *“I never ordered this”* or *“Item never arrived”* after receiving the goods). 
- Issuing banks reject **80%+** of standard merchant dispute responses because they lack formal network citations.
- Gathering carrier logs, IP timestamps, and legal clauses takes **45–60 minutes per dispute**.

## 💡 The Solution: DisputeForge
1. **Automated Evidence Assessment:** Evaluates evidence against the **Visa Compelling Evidence 3.0 (CE 3.0)** framework.
2. **Win Probability Scoring Engine:** Gives merchants instant feedback on case strength (0–100%) before submitting.
3. **Official Bank Rebuttal Letters:** Auto-generates structured, formal legal dossiers with relevant reason code citations (Visa 10.4, 13.1, Mastercard 4837, 4855).
4. **1-Click Print / PDF Export:** Ready to upload directly into the Stripe Dashboard, PayPal Resolution Center, or Shopify Admin.
5. **Zero-Knowledge Privacy:** 100% of data processing occurs client-side in the merchant's browser — customer PII never touches intermediate third-party servers.

---

## 💳 Supported Payment Networks & Processors
- **Gateways:** Stripe, Shopify Payments, PayPal, Square, Authorize.Net.
- **Card Networks:** Visa Claims Resolution (VCR), Mastercard Dispute Resolution, American Express, Discover.
- **Reason Codes:**
  - `Fraudulent / Unauthorized Transaction` (Visa 10.4 / Mastercard 4837 / 4863)
  - `Product Not Received` (Visa 13.1 / Mastercard 4855)
  - `Not As Described / Defective` (Visa 13.3 / Mastercard 4853)
  - `Subscription Canceled` (Visa 13.5 / Mastercard 4841)
  - `Unrecognized / General Inquiry` (Visa 10.5 / Mastercard 4834)

---

## 🚀 Live Access & Pricing
- **Free Tier:** Instant free generation for any open dispute.
- **Starter ($49/mo):** Up to 15 dispute defenses/mo. [Get Starter](https://app.lava.top/products/a26d6639-eb45-4bff-a506-dd4eb2758eb9)
- **Pro ($99/mo):** Up to 60 dispute defenses/mo + Multi-gateway support. [Get Pro](https://app.lava.top/products/05388c66-a742-4da8-930e-70952e32a5f8)

---

## 💻 Local Development & Self-Hosting

### Quick Run (Zero Dependencies):
```bash
git clone https://github.com/vanosalif-ui/disputeforge.git
cd disputeforge
python app.py
```
Open your browser at `http://localhost:8088`.

---

© 2026 DisputeForge. Open-Source Commercial SaaS.
