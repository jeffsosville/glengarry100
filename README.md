# ⭐ Glengarry100

**The open-source trust layer for business brokers.**
No paywalls. No spam. Just verified listings, public broker rankings, and radical transparency.

> **"We're building the Wikipedia of business-for-sale marketplaces."**

---

## 🚨 Why This Matters

Brokers are buried under outdated tools, fake leads, and \$1,000/month paywalls to access *their own listings*.
Meanwhile, buyers can't tell what's real — and sellers drown in spam.

**Glengarry100 changes that.**

We track the top 100 brokers by *real listings* — not paid placement.
And we’re launching the first open-source index of verified businesses for sale.

---

## 💡 What We're Building

* ✅ **Verified Broker Leaderboard** (live at [glengarry100.vercel.app](https://glengarry100.vercel.app))
* 🔍 **Daily Matched Listings** (linked directly to broker sites)
* 📦 **Open JSON & CSV** of real, public business listings
* 🔐 **Broker Claim Flow** (submit your verified listings)
* 🔐 **Spider Queue** for franchise brokers like Sunbelt, Transworld, VR, Murphy
* 🩼 **"Glengarry Index" audit** of stale vs real listings from BizBuySell

---

## 🧱 Repo Structure

```bash
/frontend        # Next.js site (leaderboard, daily feed)
/lib             # Supabase, JSON loaders, util functions
/pages           # Leaderboard + /daily route
bizbuysell_listings.json   # Raw scraped data sample
.env.local.example         # Example Supabase env
tailwind.config.js         # UI styling
```

---

## 🔜 Coming Soon

* `/api/submit-listings` endpoint for verified broker feeds
* `/broker/[id]` dynamic profiles
* Franchise broker spiders (Transworld, Sunbelt, Murphy, VR)
* Public trust scores (based on verified listing volume + freshness)
* Discord + Community Chat

---

## 🤝 How to Contribute

1. **Star this repo**
2. Fork & clone
3. `cd frontend && npm install`
4. `npm run dev`
5. Open a PR — we’ll review fast
6. Help improve the spiders, frontend, or data matching
7. Check the [Issues tab](https://github.com/jeffsosville/glengarry100/issues)

🫠 Have data sources? Know a franchise broker site? Submit them via [Issues](https://github.com/jeffsosville/glengarry100/issues) or PRs!

---

## 🔍 Current Data Focus

* 2,000+ broker listing URLs (in-progress)
* Matching each to broker metadata and scraping live data
* Phase 1 = Broker-only listings
* Phase 2 = Verified sellers
* Phase 3 = CRE disruption — yes, we’re coming for that next

---

## 🔓 Our Values

* **Transparency over Paywalls**
* **Verification over Volume**
* **Open Listings > Spam**
* **Public Data, Forever**

> “We’re not here to extract rent. We’re here to expose it.”

---

## 🧠 Governance

* Led by [@jeffsosville](https://github.com/jeffsosville) (benevolent dictator model)
* Core decisions will always favor transparency, data accuracy, and public trust
* PRs welcome — final merges will protect mission integrity
* License: **Apache 2.0** — fork it, build it, just don’t close it

---

## 🧫 Inspired By

> “Don’t ever make your users pay to access their own contributions.”
> — **Jimmy Wales**, Wikipedia

> “You need to be stubborn on vision, flexible on implementation.”
> — **Paul Graham**, Y Combinator

> “If the data isn’t open, it’s already obsolete.”
> — **Luis von Ahn**, Duolingo / reCAPTCHA


> “Talk is cheap. Show me the code.”
> — **Linus Torvalds**, Linux

---

## 📣 Join the Movement

→ [Twitter](https://twitter.com/jeffsosville)
→ [glengarry100.vercel.app](https://glengarry100.vercel.app)
→ \[Substack Coming Soon]
→ \[Discord Invite Coming Soon]

---

> *“Let the brokers take back control. Let the buyers see the truth. Let the data breathe.”*

**No paywalls. No stale listings. No BS. Just trust.**
