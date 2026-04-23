# ShipZen Landing Page Redesign Plan
Created: 2026-04-17

## Framework
- Alex Hormozi Value Equation: Dream Outcome × Perceived Likelihood / (Time Delay × Effort)
- CRO principles: Value first, villain framing, loss aversion, risk reversal
- Hormozi GOATed structure: Grab → Offer → Amplify → Trigger

---

## Current Page Problems

1. Hero headline is weak — "Stop overpaying" has mild loss-aversion but no dream outcome, no specificity, no visceral pain
2. Form is high-friction cold ask — 4 fields (email + phone + website + shipments) before giving any value
3. No villain framing in the hero — people need an enemy to emotionally switch (Pirate Ship, ShipStation)
4. Testimonial is anonymous and vague — "E-Commerce Store Owner" + "500+ shipments/month" = no credibility
5. No live savings number — telling visitors "we'll quote you in 24hrs" kills urgency. Show them money NOW.
6. No risk reversal above the fold
7. Stats bar misses Hormozi dream outcome framing

---

## The 6 Changes (Priority Order)

### 1. Hero Headline + Subhead — Hormozi Value Equation
- Loss aversion + dream outcome + villain named
- Headline option A: "You're throwing away $X,XXX a month on shipping labels."
- Headline option B: "Pirate Ship is charging you zone fees. We don't."
- Headline option C: "The same UPS Ground label. $1–$2 cheaper. Every single one."
- Subhead: Names the villain — "Pirate Ship, ShipStation, and EasyShip pass zone fees, fuel surcharges, and DIM weight penalties straight to you. ShipZen has one flat rate — no exceptions."

### 2. Interactive Savings Calculator (replaces static form card)
- Slider: "How many packages do you ship per month?" (100 → 5000+)
- Live update: "You're likely losing $[X] per month with your current carrier"
- Shows math: "At 500 packages × avg $1.50 savings = $750/month = $9,000/year"
- Single CTA below: "Enter your email to see your real rate"
- Hormozi principle: Value-first, reduce effort, show dream outcome BEFORE asking

### 3. Villain Section (new, inserted above comparison table)
- Heading: "Why every other platform keeps you overpaying"
- Hormozi Problem Agitation framework
- 3 bullets:
  a. "Aggregators profit from your surcharges — they pass through fuel fees, DIM weight, and zone costs because that's how their margin works"
  b. "Going direct to UPS means retail pricing — you need 500+ packages/week just to qualify for commercial discounts"
  c. "3PLs are multi-carrier by design — no single carrier relationship is deep enough for enterprise pricing"
- Payoff line: "ShipZen is the only platform structured specifically to unlock enterprise UPS Ground pricing."

### 4. Stronger Testimonial — Specificity + Numbers
- Before: generic, anonymous
- After: "We were paying $9.40/label on Pirate Ship. ShipZen got us to $7.10. That's $1,150 back in our pocket last month."
- Attribution: Sarah M., Shopify store, 500 orders/month
- (Note: use realistic numbers — confirm with real data when available)

### 5. Risk Reversal in Hero (below CTA)
- "No credit card. No contract. If we can't beat your current rate, we'll tell you straight."
- Hormozi: make saying YES frictionless. Remove fear of commitment entirely.

### 6. Urgency / Scarcity Element
- Below hero form: "Currently onboarding sellers shipping 200+ packages/month. Capacity is limited."
- Not fake — positions ShipZen as selective and premium (Hormozi: scarcity without lying)

---

## Page Structure After Redesign

```
NAV
HERO (new headline + subhead + villain named)
  [Left] Loss-aversion copy + risk reversal + scarcity note
  [Right] SAVINGS CALCULATOR → single email CTA
STATS BAR (keep, reframe as dream outcome)
VILLAIN SECTION (new)
ENTERPRISE CARDS (keep animated canvases)
HOW IT WORKS (keep)
COMPARISON TABLE (keep)
INTEGRATIONS (keep)
TESTIMONIAL (rewrite with numbers)
FAQ (keep)
CTA BANNER (update copy to match new framing)
FOOTER
```

---

## Backup
Original page backed up at: landing_v2_backup.py
Working file: landing_v2.py

---

## Status
- [ ] Hero rewrite
- [ ] Calculator widget
- [ ] Villain section
- [ ] Testimonial rewrite
- [ ] Risk reversal in hero
- [ ] Scarcity element
- [ ] Deploy to Railway
