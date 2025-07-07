#Glengarry100

**The open-source trust layer for business brokers.**  
No paywalls. No spam. Just verified listings, public broker rankings, and radical transparency.

> **"We're building the Wikipedia of business-for-sale marketplaces."**

---

## Why This Matters

Brokers are buried under outdated tools, fake leads, and $1,000/month paywalls to access *their own listings*.  
Meanwhile, buyers can't tell what's real — and sellers drown in spam.

**Glengarry100 changes that.**

We track the top 100 brokers by *real listings* — not paid placement.  
And we’re launching the first open-source index of verified businesses for sale.

---

## 💡 What We're Building

- ✅ **Verified Broker Leaderboard** (live at [glengarry100.vercel.app](https://glengarry100.vercel.app))  
- 🔍 **Daily Matched Listings** (linked directly to broker sites)  
- 📦 **Open JSON & CSV** of real, public business listings  
- 🔐 **Broker Claim Flow** (submit your verified listings)  
- 🔌 **Spider Queue** for franchise brokers like Sunbelt, Transworld, VR, Murphy  
- 🧼 **"Glengarry Index" audit** of stale vs real listings from BizBuySell

---

## 🧱 Repo Structure

```bash
/frontend        # Next.js site (leaderboard, daily feed)
/lib             # Supabase, JSON loaders, util functions
/pages           # Leaderboard + /daily route
bizbuysell_listings.json   # Raw scraped data sample
.env.local.example         # Example Supabase env
tailwind.config.js         # UI styling
