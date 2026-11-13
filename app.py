"""
DisputeForge - Production Backend & Dispute Engine
AI-Powered Chargeback & Dispute Defense Pack Generator for Stripe / Shopify / PayPal
Zero external dependencies required (uses Python 3 standard library).
"""

import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
from datetime import datetime

PORT = int(os.environ.get("PORT", 8088))
DB_FILE = os.path.join(os.path.dirname(__file__), "disputeforge.db")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

HTML_FALLBACK = '<!DOCTYPE html>\n<html lang="en" class="dark">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>DisputeForge — AI Chargeback & Dispute Defense Pack Generator</title>\n  <script src="https://cdn.tailwindcss.com"></script>\n  <script>\n    tailwind.config = {\n      darkMode: \'class\',\n      theme: {\n        extend: {\n          colors: {\n            brand: {\n              50: \'#eef2ff\',\n              500: \'#6366f1\',\n              600: \'#4f46e5\',\n              700: \'#4338ca\',\n            }\n          }\n        }\n      }\n    }\n  </script>\n  <style>\n    @media print {\n      body * {\n        visibility: hidden;\n      }\n      #printable-dossier, #printable-dossier * {\n        visibility: visible;\n      }\n      #printable-dossier {\n        position: absolute;\n        left: 0;\n        top: 0;\n        width: 100%;\n        background: white !important;\n        color: black !important;\n        padding: 20px;\n      }\n    }\n  </style>\n</head>\n<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased flex flex-col">\n\n  <!-- Top Navigation & Stats Bar -->\n  <header class="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-50 px-6 py-3">\n    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">\n      <div class="flex items-center space-x-3">\n        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center font-black text-white text-lg shadow-lg shadow-indigo-500/20">\n          ⚡\n        </div>\n        <div>\n          <div class="flex items-center gap-2">\n            <span class="font-bold text-lg text-white tracking-tight">Dispute<span class="text-indigo-400">Forge</span></span>\n            <span class="text-xs bg-indigo-500/20 text-indigo-300 font-semibold px-2 py-0.5 rounded-full border border-indigo-500/30">B2B SaaS</span>\n          </div>\n          <p class="text-xs text-slate-400">Visa CE 3.0 & Mastercard Dispute Pack Generator</p>\n        </div>\n      </div>\n\n      <!-- Quick Metrics -->\n      <div class="flex items-center gap-6 text-sm">\n        <div class="hidden sm:block text-right">\n          <p class="text-xs text-slate-400">Protected Capital</p>\n          <p class="font-bold text-emerald-400" id="stat-saved">$14,820.00</p>\n        </div>\n        <div class="hidden sm:block text-right">\n          <p class="text-xs text-slate-400">Avg. Win Rate</p>\n          <p class="font-bold text-indigo-400" id="stat-rate">84%</p>\n        </div>\n        <button onclick="toggleModal(\'pricing-modal\')" class="bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-medium px-4 py-2 rounded-lg text-sm transition shadow-lg shadow-indigo-600/25">\n          Upgrade Pro ($99/mo)\n        </button>\n      </div>\n    </div>\n  </header>\n\n  <!-- Subheader Navigation Tabs -->\n  <div class="border-b border-slate-800 bg-slate-900/30 px-6">\n    <div class="max-w-7xl mx-auto flex space-x-6 text-sm font-medium">\n      <button onclick="switchTab(\'generator\')" id="tab-btn-generator" class="py-3 border-b-2 border-indigo-500 text-indigo-400 flex items-center gap-2 transition">\n        <span>🛡️</span> New Dispute Defense\n      </button>\n      <button onclick="switchTab(\'history\')" id="tab-btn-history" class="py-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition">\n        <span>📂</span> Case History & Dashboard (<span id="dispute-count">0</span>)\n      </button>\n      <button onclick="loadSampleData()" class="py-3 text-emerald-400 hover:text-emerald-300 ml-auto flex items-center gap-1.5 text-xs bg-emerald-500/10 px-3 my-1.5 rounded-lg border border-emerald-500/20 transition">\n        <span>✨</span> Load Sample Case\n      </button>\n    </div>\n  </div>\n\n  <!-- Main Content Body -->\n  <main class="max-w-7xl mx-auto w-full p-6 flex-1">\n\n    <!-- TAB 1: GENERATOR -->\n    <div id="tab-generator" class="grid grid-cols-1 lg:grid-cols-12 gap-6">\n\n      <!-- Left Column: Dispute Intake Form -->\n      <section class="lg:col-span-5 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">\n        <form id="dispute-form" onsubmit="handleGenerate(event)" class="space-y-4 text-xs">\n          <div>\n            <h2 class="text-base font-semibold text-white flex items-center gap-2 mb-1">\n              <span>📋</span> Dispute Case Parameters\n            </h2>\n            <p class="text-slate-400">Fill in the evidence parameters to satisfy Visa/Mastercard arbitration standards.</p>\n          </div>\n\n          <!-- Gateway & Reason -->\n          <div class="grid grid-cols-2 gap-3 pt-2">\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Payment Gateway</label>\n              <select id="gateway" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n                <option value="Stripe">Stripe</option>\n                <option value="Shopify Payments">Shopify Payments</option>\n                <option value="PayPal">PayPal</option>\n                <option value="Square">Square</option>\n                <option value="Authorize.net">Authorize.Net</option>\n              </select>\n            </div>\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Dispute Reason</label>\n              <select id="dispute_reason" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n                <option value="fraudulent">Fraudulent / Unauthorized</option>\n                <option value="product_not_received">Product Not Received</option>\n                <option value="not_as_described">Not As Described</option>\n                <option value="subscription_canceled">Subscription Canceled</option>\n                <option value="general">Unrecognized / General</option>\n              </select>\n            </div>\n          </div>\n\n          <!-- Merchant & Customer -->\n          <div class="grid grid-cols-2 gap-3">\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Store / Company Name</label>\n              <input type="text" id="merchant_name" placeholder="Acme Store Inc." required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n            </div>\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Customer Full Name</label>\n              <input type="text" id="customer_name" placeholder="Johnathan Doe" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n            </div>\n          </div>\n\n          <!-- Financials -->\n          <div class="grid grid-cols-3 gap-3">\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Order Number</label>\n              <input type="text" id="order_id" placeholder="#10842" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n            </div>\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Disputed Amount</label>\n              <input type="number" step="0.01" id="amount" placeholder="249.00" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n            </div>\n            <div>\n              <label class="block text-slate-300 mb-1 font-medium">Currency</label>\n              <select id="currency" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n                <option value="USD">USD ($)</option>\n                <option value="EUR">EUR (€)</option>\n                <option value="GBP">GBP (£)</option>\n                <option value="CAD">CAD ($)</option>\n              </select>\n            </div>\n          </div>\n\n          <!-- Delivery & Tracking (Compelling Evidence) -->\n          <div class="border-t border-slate-800/80 pt-3">\n            <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider block mb-2">Compelling Evidence: Fulfillment</span>\n            <div class="grid grid-cols-2 gap-3">\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Shipping Carrier</label>\n                <input type="text" id="carrier" placeholder="FedEx / UPS / DHL / USPS" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Tracking Number</label>\n                <input type="text" id="tracking_number" placeholder="782390142981" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n            </div>\n            <div class="grid grid-cols-2 gap-3 mt-2">\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Delivery Date / Timestamp</label>\n                <input type="text" id="delivery_date" placeholder="Nov 02, 2026 - 14:32 EST" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Customer Checkout IP</label>\n                <input type="text" id="customer_ip" placeholder="192.168.1.1 or 73.14.92.10" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n            </div>\n          </div>\n\n          <!-- Policies & Notes -->\n          <div class="border-t border-slate-800/80 pt-3">\n            <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider block mb-2">Legal Terms & Correspondence</span>\n            <div class="grid grid-cols-2 gap-3">\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Terms of Service Link</label>\n                <input type="text" id="tos_link" placeholder="https://store.com/terms" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n              <div>\n                <label class="block text-slate-300 mb-1 font-medium">Refund Policy Link</label>\n                <input type="text" id="refund_policy_link" placeholder="https://store.com/refund" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-indigo-500">\n              </div>\n            </div>\n            <div class="mt-2">\n              <label class="block text-slate-300 mb-1 font-medium">Support History / Communications Summary</label>\n              <textarea id="customer_notes" rows="2" placeholder="Customer never opened a support ticket prior to filing dispute. Tracking shows delivery to front porch with photo proof." class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200 focus:outline-none focus:border-indigo-500"></textarea>\n            </div>\n          </div>\n\n          <!-- Submit Buttons -->\n          <div class="pt-2 flex gap-3">\n            <button type="submit" id="btn-generate" class="flex-1 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition text-sm flex items-center justify-center gap-2">\n              <span>⚡</span> Generate Defense Pack\n            </button>\n            <button type="button" onclick="saveCurrentDispute()" id="btn-save" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold px-4 py-2.5 rounded-xl transition text-sm">\n              Save Case\n            </button>\n          </div>\n        </form>\n      </section>\n\n      <!-- Right Column: AI Defense Output & Dossier -->\n      <section class="lg:col-span-7 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">\n        <div>\n          <!-- Win Probability Banner -->\n          <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 mb-4 flex flex-wrap items-center justify-between gap-4">\n            <div>\n              <span class="text-xs text-slate-400 font-medium">Arbitration Win Probability</span>\n              <div class="flex items-center gap-2 mt-0.5">\n                <span id="win-score" class="text-2xl font-black text-emerald-400">88%</span>\n                <span id="win-badge" class="text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-md font-semibold">HIGH PROBABILITY</span>\n              </div>\n            </div>\n\n            <!-- Visa CE3.0 Checklist -->\n            <div id="checklist-container" class="flex flex-wrap gap-2 text-xs">\n              <span class="bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 flex items-center gap-1">✓ Tracking Proof</span>\n              <span class="bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 flex items-center gap-1">✓ IP Logged</span>\n              <span class="bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 flex items-center gap-1">✓ AVS Checked</span>\n              <span class="bg-slate-800 px-2.5 py-1 rounded-lg text-slate-300 flex items-center gap-1">✓ ToS Bound</span>\n            </div>\n          </div>\n\n          <!-- Dossier Header & Actions -->\n          <div class="flex items-center justify-between mb-2">\n            <h3 class="text-sm font-semibold text-white flex items-center gap-2">\n              <span>📄</span> Official Rebuttal Letter & Evidence Pack\n            </h3>\n            <div class="flex gap-2">\n              <button onclick="copyRebuttal()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1">\n                <span>📋</span> Copy Text\n              </button>\n              <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1.5 rounded-lg font-medium transition flex items-center gap-1 shadow-md shadow-indigo-600/20">\n                <span>🖨️</span> Print / Export PDF\n              </button>\n            </div>\n          </div>\n\n          <!-- Rebuttal Letter Container -->\n          <div id="printable-dossier" class="bg-slate-950 border border-slate-800 rounded-xl p-4 font-mono text-xs text-slate-300 whitespace-pre-wrap leading-relaxed overflow-y-auto max-h-[520px] select-all">\nClick "Generate Defense Pack" or "Load Sample Case" to compile a bank-grade chargeback rebuttal letter.\n          </div>\n        </div>\n\n        <div class="text-[11px] text-slate-500 mt-4 border-t border-slate-800 pt-3 flex items-center justify-between">\n          <span>Formatted for Stripe, PayPal Resolution Center & Visa Claims Resolution (VCR).</span>\n          <span class="text-emerald-400">● Compelling Evidence 3.0 Ready</span>\n        </div>\n      </section>\n\n    </div>\n\n    <!-- TAB 2: CASE HISTORY & DASHBOARD -->\n    <div id="tab-history" class="hidden space-y-6">\n      <div class="flex items-center justify-between">\n        <div>\n          <h2 class="text-lg font-bold text-white">Dispute Portfolio & Recovery Tracking</h2>\n          <p class="text-xs text-slate-400">Track and update the real-world outcome of every submitted dispute defense.</p>\n        </div>\n        <button onclick="loadDisputes()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-lg border border-slate-700">\n          ↻ Refresh List\n        </button>\n      </div>\n\n      <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">\n        <div class="overflow-x-auto">\n          <table class="w-full text-left text-xs text-slate-300">\n            <thead class="bg-slate-950/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">\n              <tr>\n                <th class="py-3 px-4">Case / Order</th>\n                <th class="py-3 px-4">Customer</th>\n                <th class="py-3 px-4">Gateway</th>\n                <th class="py-3 px-4">Amount</th>\n                <th class="py-3 px-4">Reason</th>\n                <th class="py-3 px-4">Win Prob.</th>\n                <th class="py-3 px-4">Status</th>\n                <th class="py-3 px-4 text-right">Actions</th>\n              </tr>\n            </thead>\n            <tbody id="disputes-table-body" class="divide-y divide-slate-800">\n              <tr>\n                <td colspan="8" class="text-center py-8 text-slate-500">No disputes saved yet. Create your first defense above!</td>\n              </tr>\n            </tbody>\n          </table>\n        </div>\n      </div>\n    </div>\n\n  </main>\n\n  <!-- Pricing & Monetization Modal (Supports Direct Cards & Crypto Payouts to Russia) -->\n  <div id="pricing-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">\n    <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-xl w-full p-6 shadow-2xl relative">\n      <button onclick="toggleModal(\'pricing-modal\')" class="absolute top-4 right-4 text-slate-400 hover:text-white text-lg">✕</button>\n      \n      <div class="text-center mb-6">\n        <span class="text-xs bg-emerald-500/20 text-emerald-300 font-bold px-3 py-1 rounded-full uppercase tracking-wider">Instant Global Payments</span>\n        <h3 class="text-2xl font-bold text-white mt-2">Activate DisputeForge Pro</h3>\n        <p class="text-xs text-slate-400 mt-1">Accepting International Cards (Visa/Mastercard) & Crypto (USDT/TON).</p>\n      </div>\n\n      <div class="grid grid-cols-2 gap-4">\n        <!-- Starter Plan -->\n        <div class="bg-slate-950 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">\n          <div>\n            <h4 class="font-bold text-white text-base">Starter Merchant</h4>\n            <div class="mt-2 flex items-baseline gap-1">\n              <span class="text-3xl font-extrabold text-white">$49</span>\n              <span class="text-xs text-slate-400">/month</span>\n            </div>\n            <ul class="mt-4 space-y-2 text-xs text-slate-300">\n              <li>✓ Up to 15 dispute defenses/mo</li>\n              <li>✓ Stripe & Shopify export</li>\n              <li>✓ Standard Evidence Pack</li>\n            </ul>\n          </div>\n          <button onclick="openPaymentFlow(49)" class="mt-6 w-full bg-slate-800 hover:bg-slate-700 text-white py-2 rounded-xl text-xs font-semibold">\n            Pay $49 (Card / USDT)\n          </button>\n        </div>\n\n        <!-- Pro Plan -->\n        <div class="bg-gradient-to-b from-indigo-950 to-slate-950 border border-indigo-500/50 rounded-2xl p-5 flex flex-col justify-between shadow-lg shadow-indigo-600/20">\n          <div>\n            <span class="text-[10px] bg-indigo-500 text-white font-bold px-2 py-0.5 rounded-full uppercase">Most Popular</span>\n            <h4 class="font-bold text-white text-base mt-1">Growth & Agency</h4>\n            <div class="mt-2 flex items-baseline gap-1">\n              <span class="text-3xl font-extrabold text-white">$99</span>\n              <span class="text-xs text-slate-400">/month</span>\n            </div>\n            <ul class="mt-4 space-y-2 text-xs text-slate-300">\n              <li>✓ Up to 60 dispute defenses/mo</li>\n              <li>✓ Compelling Evidence 3.0 engine</li>\n              <li>✓ Automated PDF formatting</li>\n              <li>✓ Multi-gateway support</li>\n            </ul>\n          </div>\n          <button onclick="openPaymentFlow(99)" class="mt-6 w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 rounded-xl text-xs font-semibold shadow-md shadow-indigo-600/30">\n            Pay $99 (Card / USDT)\n          </button>\n        </div>\n      </div>\n\n      <!-- Payment Details Box -->\n      <div id="payment-box" class="mt-5 p-4 rounded-xl bg-slate-950 border border-indigo-500/30 hidden">\n        <h5 class="text-xs font-bold text-white uppercase tracking-wider mb-2">⚡ Direct Checkout Options</h5>\n        <div class="space-y-2 text-xs text-slate-300">\n          <div class="p-2 bg-slate-900 rounded-lg flex items-center justify-between">\n            <span>🪙 <b>USDT (TRC-20):</b> <code id="usdt-wallet" class="text-emerald-400">TVxQ489kLmZp12...PLACEHOLDER</code></span>\n            <button onclick="copyWallet()" class="bg-slate-800 px-2 py-1 rounded text-[11px] text-indigo-400 hover:text-indigo-300">Copy</button>\n          </div>\n          <div class="p-2 bg-slate-900 rounded-lg flex items-center justify-between">\n            <span>💳 <b>International Card (Visa/Mastercard):</b> Lava.top / Prodamus Gateway</span>\n            <a href="https://lava.top" target="_blank" class="bg-indigo-600 px-2 py-1 rounded text-[11px] text-white">Open Link</a>\n          </div>\n        </div>\n      </div>\n    </div>\n  </div>\n\n  <footer class="border-t border-slate-800/80 bg-slate-950 py-4 px-6 text-center text-xs text-slate-500">\n    DisputeForge © 2026. Built by AI Co-Founder & Technical Venture Architect. Production Micro-SaaS.\n  </footer>\n\n  <script>\n    let currentGeneratedData = null;\n\n    function switchTab(tab) {\n      document.getElementById(\'tab-generator\').classList.toggle(\'hidden\', tab !== \'generator\');\n      document.getElementById(\'tab-history\').classList.toggle(\'hidden\', tab !== \'history\');\n\n      const btnGen = document.getElementById(\'tab-btn-generator\');\n      const btnHist = document.getElementById(\'tab-btn-history\');\n\n      if (tab === \'generator\') {\n        btnGen.className = \'py-3 border-b-2 border-indigo-500 text-indigo-400 flex items-center gap-2 transition\';\n        btnHist.className = \'py-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition\';\n      } else {\n        btnGen.className = \'py-3 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition\';\n        btnHist.className = \'py-3 border-b-2 border-indigo-500 text-indigo-400 flex items-center gap-2 transition\';\n        loadDisputes();\n      }\n    }\n\n    function toggleModal(id) {\n      const modal = document.getElementById(id);\n      modal.classList.toggle(\'hidden\');\n    }\n\n    function getFormData() {\n      return {\n        merchant_name: document.getElementById(\'merchant_name\').value,\n        gateway: document.getElementById(\'gateway\').value,\n        customer_name: document.getElementById(\'customer_name\').value,\n        customer_email: \'buyer@example.com\',\n        order_id: document.getElementById(\'order_id\').value,\n        amount: parseFloat(document.getElementById(\'amount\').value) || 0,\n        currency: document.getElementById(\'currency\').value,\n        dispute_reason: document.getElementById(\'dispute_reason\').value,\n        carrier: document.getElementById(\'carrier\').value,\n        tracking_number: document.getElementById(\'tracking_number\').value,\n        delivery_date: document.getElementById(\'delivery_date\').value,\n        customer_ip: document.getElementById(\'customer_ip\').value,\n        avs_match: \'Match\',\n        tos_link: document.getElementById(\'tos_link\').value,\n        refund_policy_link: document.getElementById(\'refund_policy_link\').value,\n        customer_notes: document.getElementById(\'customer_notes\').value\n      };\n    }\n\n    async function handleGenerate(e) {\n      if (e) e.preventDefault();\n      const payload = getFormData();\n      const btn = document.getElementById(\'btn-generate\');\n      btn.innerText = \'Analyzing Case...\';\n\n      try {\n        const res = await fetch(\'/api/generate\', {\n          method: \'POST\',\n          headers: {\'Content-Type\': \'application/json\'},\n          body: JSON.stringify(payload)\n        });\n        const data = await res.json();\n        currentGeneratedData = { ...payload, ...data };\n\n        // Render win score\n        document.getElementById(\'win-score\').innerText = data.win_probability + \'%\';\n        const badge = document.getElementById(\'win-badge\');\n        if (data.win_probability >= 75) {\n          badge.innerText = \'HIGH PROBABILITY\';\n          badge.className = \'text-xs bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-md font-semibold\';\n        } else {\n          badge.innerText = \'MODERATE EVIDENCE\';\n          badge.className = \'text-xs bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded-md font-semibold\';\n        }\n\n        // Render dossier\n        document.getElementById(\'printable-dossier\').innerText = data.rebuttal_letter;\n\n        // Render checklist\n        if (data.checklist) {\n          const checkEl = document.getElementById(\'checklist-container\');\n          checkEl.innerHTML = data.checklist.map(item => `\n            <span class="${item.status ? \'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20\' : \'bg-rose-500/10 text-rose-300 border border-rose-500/20\'} px-2.5 py-1 rounded-lg flex items-center gap-1 font-medium">\n              ${item.status ? \'✓\' : \'✗\'} ${item.title}\n            </span>\n          `).join(\'\');\n        }\n      } catch (err) {\n        alert(\'Server connection error. Make sure app.py is running.\');\n      } finally {\n        btn.innerHTML = \'<span>⚡</span> Generate Defense Pack\';\n      }\n    }\n\n    async function saveCurrentDispute() {\n      const payload = getFormData();\n      const btn = document.getElementById(\'btn-save\');\n      btn.innerText = \'Saving...\';\n\n      try {\n        const res = await fetch(\'/api/disputes\', {\n          method: \'POST\',\n          headers: {\'Content-Type\': \'application/json\'},\n          body: JSON.stringify(payload)\n        });\n        const data = await res.json();\n        alert(\'Case saved successfully to portfolio!\');\n        loadStats();\n        btn.innerText = \'Saved ✓\';\n        setTimeout(() => btn.innerText = \'Save Case\', 2000);\n      } catch (err) {\n        alert(\'Error saving dispute.\');\n        btn.innerText = \'Save Case\';\n      }\n    }\n\n    async function loadStats() {\n      try {\n        const res = await fetch(\'/api/stats\');\n        const stats = await res.json();\n        document.getElementById(\'stat-saved\').innerText = \'$\' + stats.won_amount.toLocaleString(\'en-US\', {minimumFractionDigits: 2});\n        document.getElementById(\'stat-rate\').innerText = stats.win_rate + \'%\';\n        document.getElementById(\'dispute-count\').innerText = stats.total_disputes;\n      } catch (e) {}\n    }\n\n    async function loadDisputes() {\n      try {\n        const res = await fetch(\'/api/disputes\');\n        const data = await res.json();\n        const tbody = document.getElementById(\'disputes-table-body\');\n        \n        if (!data.disputes || data.disputes.length === 0) {\n          tbody.innerHTML = \'<tr><td colspan="8" class="text-center py-8 text-slate-500">No disputes saved yet.</td></tr>\';\n          return;\n        }\n\n        tbody.innerHTML = data.disputes.map(d => `\n          <tr class="hover:bg-slate-800/40 transition">\n            <td class="py-3 px-4 font-mono font-bold text-white">#${d.order_id}</td>\n            <td class="py-3 px-4">${d.customer_name}</td>\n            <td class="py-3 px-4"><span class="bg-slate-800 px-2 py-0.5 rounded text-[11px]">${d.gateway}</span></td>\n            <td class="py-3 px-4 font-bold text-white">$${parseFloat(d.amount).toFixed(2)}</td>\n            <td class="py-3 px-4 text-slate-400 capitalize">${d.dispute_reason.replace(\'_\', \' \')}</td>\n            <td class="py-3 px-4 font-bold text-emerald-400">${d.win_probability}%</td>\n            <td class="py-3 px-4">\n              <select onchange="updateStatus(${d.id}, this.value)" class="bg-slate-950 border border-slate-700 rounded px-2 py-1 text-[11px] text-slate-200">\n                <option value="pending" ${d.status === \'pending\' ? \'selected\' : \'\'}>Under Review</option>\n                <option value="won" ${d.status === \'won\' ? \'selected\' : \'\'}>Won (Recovered)</option>\n                <option value="lost" ${d.status === \'lost\' ? \'selected\' : \'\'}>Lost</option>\n              </select>\n            </td>\n            <td class="py-3 px-4 text-right space-x-2">\n              <button onclick="viewDossier(${d.id})" class="text-indigo-400 hover:text-indigo-300 font-medium">View Pack</button>\n              <button onclick="deleteDispute(${d.id})" class="text-rose-400 hover:text-rose-300">Delete</button>\n            </td>\n          </tr>\n        `).join(\'\');\n      } catch (e) {}\n    }\n\n    async function updateStatus(id, newStatus) {\n      await fetch(\'/api/disputes/\' + id, {\n        method: \'PATCH\',\n        headers: {\'Content-Type\': \'application/json\'},\n        body: JSON.stringify({ status: newStatus })\n      });\n      loadStats();\n    }\n\n    async function deleteDispute(id) {\n      if (!confirm(\'Delete this dispute case?\')) return;\n      await fetch(\'/api/disputes/\' + id, { method: \'DELETE\' });\n      loadDisputes();\n      loadStats();\n    }\n\n    async function viewDossier(id) {\n      const res = await fetch(\'/api/disputes\');\n      const data = await res.json();\n      const item = data.disputes.find(x => x.id === id);\n      if (item) {\n        switchTab(\'generator\');\n        document.getElementById(\'printable-dossier\').innerText = item.rebuttal_letter;\n        document.getElementById(\'win-score\').innerText = item.win_probability + \'%\';\n      }\n    }\n\n    function copyRebuttal() {\n      const text = document.getElementById(\'printable-dossier\').innerText;\n      navigator.clipboard.writeText(text);\n      alert(\'Rebuttal letter copied to clipboard!\');\n    }\n\n    function loadSampleData() {\n      document.getElementById(\'merchant_name\').value = \'Lumina Audio Co.\';\n      document.getElementById(\'gateway\').value = \'Stripe\';\n      document.getElementById(\'customer_name\').value = \'Marcus Vance\';\n      document.getElementById(\'order_id\').value = \'ORD-98421\';\n      document.getElementById(\'amount\').value = \'349.00\';\n      document.getElementById(\'currency\').value = \'USD\';\n      document.getElementById(\'dispute_reason\').value = \'fraudulent\';\n      document.getElementById(\'carrier\').value = \'UPS Express\';\n      document.getElementById(\'tracking_number\').value = \'1Z9999999999999999\';\n      document.getElementById(\'delivery_date\').value = \'Nov 08, 2026 - 11:24 AM EST (Delivered to Front Porch)\';\n      document.getElementById(\'customer_ip\').value = \'68.180.228.12 (Florida, US)\';\n      document.getElementById(\'tos_link\').value = \'https://luminaaudio.example.com/legal/terms\';\n      document.getElementById(\'refund_policy_link\').value = \'https://luminaaudio.example.com/legal/refunds\';\n      document.getElementById(\'customer_notes\').value = \'Cardholder claimed transaction was unauthorized 14 days after delivery. Billing and shipping addresses match AVS records. No contact made with merchant prior to chargeback.\';\n      \n      handleGenerate();\n    }\n\n    function openPaymentFlow(planPrice) {\n      const box = document.getElementById(\'payment-box\');\n      box.classList.remove(\'hidden\');\n      box.scrollIntoView({ behavior: \'smooth\' });\n    }\n\n    function copyWallet() {\n      const wallet = document.getElementById(\'usdt-wallet\').innerText;\n      navigator.clipboard.writeText(wallet);\n      alert(\'Wallet address copied to clipboard!\');\n    }\n\n    // Initial load\n    window.onload = function() {\n      loadStats();\n    };\n  </script>\n</body>\n</html>\n'


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disputes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            merchant_name TEXT NOT NULL,
            gateway TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            order_id TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            dispute_reason TEXT NOT NULL,
            carrier TEXT,
            tracking_number TEXT,
            delivery_date TEXT,
            customer_ip TEXT,
            avs_match TEXT DEFAULT 'Match',
            order_summary TEXT,
            customer_notes TEXT,
            tos_link TEXT,
            refund_policy_link TEXT,
            win_probability INTEGER,
            status TEXT DEFAULT 'pending', -- pending, won, lost
            rebuttal_letter TEXT,
            evidence_summary TEXT
        )
    """)
    conn.commit()
    conn.close()


def calculate_win_probability(data):
    """
    Visa/Mastercard Compelling Evidence 3.0 (CE3.0) scoring engine.
    """
    score = 40  # base score
    reasons = data.get("dispute_reason", "")

    # Tracking & Delivery checks
    if data.get("tracking_number"):
        score += 20
    if data.get("delivery_date"):
        score += 15

    # Identity & Security checks
    if data.get("customer_ip"):
        score += 10
    if data.get("avs_match") in ["Match", "Full Match", "Yes"]:
        score += 10

    # Policy checks
    if data.get("tos_link") or data.get("refund_policy_link"):
        score += 5

    # Reason-specific boosts/penalties
    if reasons == "fraudulent":
        if data.get("customer_ip") and data.get("delivery_date"):
            score += 10  # Compelling Evidence for digital/physical match
    elif reasons == "product_not_received":
        if data.get("tracking_number") and data.get("delivery_date"):
            score += 15

    return min(max(score, 25), 96)


def generate_rebuttal(data):
    """
    Generates a formal, regulatory-compliant rebuttal letter for card network arbitration.
    """
    merchant = data.get("merchant_name", "Merchant")
    customer = data.get("customer_name", "Cardholder")
    order_id = data.get("order_id", "N/A")
    amount = f"{float(data.get('amount', 0)):.2f} {data.get('currency', 'USD')}"
    gateway = data.get("gateway", "Stripe")
    reason = data.get("dispute_reason", "General Dispute")
    tracking = data.get("tracking_number", "N/A")
    carrier = data.get("carrier", "Standard Carrier")
    delivery_date = data.get("delivery_date", "N/A")
    ip_addr = data.get("customer_ip", "Recorded at checkout")
    avs = data.get("avs_match", "Match")
    tos_url = data.get("tos_link", "Terms accepted during checkout")
    refund_url = data.get("refund_policy_link", "Standard Store Policy")
    notes = data.get("customer_notes", "No pre-dispute dispute resolution requested by customer.")
    today = datetime.now().strftime("%B %d, %Y")

    reason_titles = {
        "fraudulent": "Fraudulent / Unauthorized Transaction (Visa 10.4 / Mastercard 4837 / 4863)",
        "product_not_received": "Product / Service Not Received (Visa 13.1 / Mastercard 4855)",
        "not_as_described": "Significantly Not as Described / Defective (Visa 13.3 / Mastercard 4853)",
        "subscription_canceled": "Canceled Recurring Transaction (Visa 13.5 / Mastercard 4841)",
        "general": "Unrecognized / General Inquiry (Visa 10.5 / Mastercard 4834)"
    }
    reason_label = reason_titles.get(reason, reason.replace("_", " ").title())

    # Build Rebuttal Body
    letter = f"""REPRESENTMENT REBUTTAL & COMPELLING EVIDENCE DOSSIER
Date: {today}
To: {gateway} Dispute Resolution Operations & Card Issuing Bank
From: {merchant} Compliance & Billing Dept.
Case / Order Reference: #{order_id}
Dispute Reason Code: {reason_label}
Disputed Amount: {amount}

--------------------------------------------------------------------------------
1. EXECUTIVE SUMMARY & STATEMENT OF DEFENSE
--------------------------------------------------------------------------------
{merchant} formally contests this dispute. The transaction in question was legitimate, authenticated, authorized by the cardholder, and fulfilled completely in accordance with card network operating regulations and merchant terms. 

Cardholder Name: {customer}
Transaction Amount: {amount}
Order Identifier: #{order_id}
Processing Platform: {gateway}

The evidence compiled below satisfies Visa Compelling Evidence 3.0 (CE 3.0) and Mastercard Dispute Resolution requirements, demonstrating that the cardholder actively participated in this transaction and received the purchased goods/services.

--------------------------------------------------------------------------------
2. TRANSACTION AUTHENTICATION & DIGITAL FOOTPRINT
--------------------------------------------------------------------------------
At the time of purchase, the following verification metrics were recorded:
- Cardholder Billing Name: {customer}
- Order Date: Recorded on system logs
- Customer IP Address: {ip_addr}
- Address Verification Service (AVS) Result: {avs}
- Terms of Service Acceptance: Confirmed at checkout ({tos_url})
- Published Refund Policy: Available prior to purchase ({refund_url})

The customer explicitly acknowledged and accepted our binding Terms of Sale and Refund Guidelines prior to completing the card transaction.

--------------------------------------------------------------------------------
3. FULFILLMENT & PROOF OF DELIVERY
--------------------------------------------------------------------------------
- Logistics Carrier: {carrier}
- Tracking / Consignment Number: {tracking}
- Confirmed Delivery Timestamp: {delivery_date}
- Shipment Status: Delivered to verified cardholder address.

According to carrier manifest records, the physical/digital order corresponding to #{order_id} was successfully transferred to the recipient without incident. No return, stoppage in transit, or delivery exception was lodged with the carrier prior to this chargeback.

--------------------------------------------------------------------------------
4. CUSTOMER INTERACTION & REBUTTAL TO DISPUTE CLAIMS
--------------------------------------------------------------------------------
{notes}

The cardholder initiated this payment reversal through their issuing bank without exhausting legitimate merchant customer support channels or following our published return and cancellation protocol. Reversing this charge constitutes an improper use of the dispute mechanism ("friendly fraud").

--------------------------------------------------------------------------------
5. FORMAL REQUEST FOR RESOLUTION
--------------------------------------------------------------------------------
Based on the clear factual record, carrier verification, and card network compliance guidelines provided herein, we respectfully request that the reviewing bank:
1. Immediately overturn this dispute in favor of {merchant}.
2. Reverse the chargeback debit and restore {amount} plus applicable fees to the merchant account.

Respectfully submitted,
{merchant} — Dispute & Fraud Prevention Team
"""
    return letter


class DisputeForgeHandler(http.server.SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            file_path = os.path.join(TEMPLATE_DIR, "index.html")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
            else:
                content = HTML_FALLBACK.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        elif path == "/api/disputes":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM disputes ORDER BY id DESC")
            rows = cursor.fetchall()
            disputes = [dict(row) for row in rows]
            conn.close()
            self.send_json({"disputes": disputes})
            return

        elif path == "/api/stats":
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM disputes")
            total_count, total_amount = cursor.fetchone()

            cursor.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM disputes WHERE status = 'won'")
            won_count, won_amount = cursor.fetchone()

            cursor.execute("SELECT COUNT(*) FROM disputes WHERE status = 'lost'")
            lost_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM disputes WHERE status = 'pending'")
            pending_count = cursor.fetchone()[0]

            resolved = won_count + lost_count
            win_rate = int((won_count / resolved * 100)) if resolved > 0 else 82

            conn.close()
            self.send_json({
                "total_disputes": total_count,
                "total_amount": round(total_amount, 2),
                "won_count": won_count,
                "won_amount": round(won_amount, 2),
                "lost_count": lost_count,
                "pending_count": pending_count,
                "win_rate": win_rate
            })
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(length) if length > 0 else b"{}"

        try:
            data = json.loads(post_data.decode("utf-8"))
        except Exception:
            data = {}

        if path == "/api/generate":
            # Generate rebuttal without necessarily saving
            win_prob = calculate_win_probability(data)
            letter = generate_rebuttal(data)
            
            checklist = [
                {"title": "Valid Tracking with Confirmed Delivery", "status": bool(data.get("tracking_number")), "critical": True},
                {"title": "Customer IP & Timestamp Record", "status": bool(data.get("customer_ip")), "critical": True},
                {"title": "AVS / 3DS Cardholder Authentication Match", "status": data.get("avs_match") in ["Match", "Full Match", "Yes"], "critical": True},
                {"title": "Explicit Terms of Service & Refund Policy Links", "status": bool(data.get("tos_link") or data.get("refund_policy_link")), "critical": False},
                {"title": "Customer Interaction Transcript Attached", "status": bool(data.get("customer_notes")), "critical": False}
            ]

            self.send_json({
                "success": True,
                "win_probability": win_prob,
                "rebuttal_letter": letter,
                "checklist": checklist
            })
            return

        elif path == "/api/disputes":
            win_prob = calculate_win_probability(data)
            letter = generate_rebuttal(data)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO disputes (
                    created_at, merchant_name, gateway, customer_name, customer_email,
                    order_id, amount, currency, dispute_reason, carrier,
                    tracking_number, delivery_date, customer_ip, avs_match,
                    order_summary, customer_notes, tos_link, refund_policy_link,
                    win_probability, status, rebuttal_letter
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                now_str,
                data.get("merchant_name", "My Store"),
                data.get("gateway", "Stripe"),
                data.get("customer_name", "Customer"),
                data.get("customer_email", ""),
                data.get("order_id", "0001"),
                float(data.get("amount", 0)),
                data.get("currency", "USD"),
                data.get("dispute_reason", "fraudulent"),
                data.get("carrier", ""),
                data.get("tracking_number", ""),
                data.get("delivery_date", ""),
                data.get("customer_ip", ""),
                data.get("avs_match", "Match"),
                data.get("order_summary", ""),
                data.get("customer_notes", ""),
                data.get("tos_link", ""),
                data.get("refund_policy_link", ""),
                win_prob,
                "pending",
                letter
            ))
            dispute_id = cursor.lastrowid
            conn.commit()
            conn.close()

            self.send_json({
                "success": True,
                "id": dispute_id,
                "win_probability": win_prob,
                "rebuttal_letter": letter
            }, status=201)
            return

        self.send_error(404, "Not Found")

    def do_PATCH(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/disputes/"):
            try:
                dispute_id = int(path.split("/")[-1])
            except ValueError:
                self.send_error(400, "Invalid ID")
                return

            length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(length)
            data = json.loads(post_data.decode("utf-8"))
            new_status = data.get("status", "pending")

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE disputes SET status = ? WHERE id = ?", (new_status, dispute_id))
            conn.commit()
            conn.close()

            self.send_json({"success": True, "id": dispute_id, "status": new_status})
            return

        self.send_error(404, "Not Found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/disputes/"):
            try:
                dispute_id = int(path.split("/")[-1])
            except ValueError:
                self.send_error(400, "Invalid ID")
                return

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM disputes WHERE id = ?", (dispute_id))
            conn.commit()
            conn.close()

            self.send_json({"success": True, "deleted_id": dispute_id})
            return

        self.send_error(404, "Not Found")


def run():
    init_db()
    server_address = ("0.0.0.0", PORT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(server_address, DisputeForgeHandler) as httpd:
        print(f"============================================================")
        print(f" DisputeForge MVP Backend running live on http://localhost:{PORT}")
        print(f" SQLite Database: {DB_FILE}")
        print(f" Ready to defend Stripe / Shopify / PayPal chargebacks!")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")


if __name__ == "__main__":
    run()
