# Pipeline Setup — Session Details (2026-06-03)

## Credentials

| Service | Account | Password/Key | Notes |
|---------|---------|-------------|-------|
| Amazon Seller Central | paul@5crests.com | JtwP!JV5qFUjQs | Paul Stone, employee of Gray Caravan Co UK (read-only) |
| Twilio | paul@5crests.com | JtwP!JV5qFUjQs | Recovery: 2QUHERDQS28EW87NXPJME7JC |
| Twilio Phone | (855) 956-2656 | — | Toll-free, for Amazon SMS verification |
| Email (Hostinger) | paul@5crests.com | fcYopz1*rEp%lI | IMAP: imap.hostinger.com:993, SMTP: smtp.hostinger.com:587 |

## Amazon Reports to Automate

Joe's workflow — five reports, currently manual (weekly → target: daily):

1. **Restock Inventory** (FBA Fulfillment) — TXT
2. **Fee Preview** (FBA Fulfillment) — TXT
3. **Third FBA report** (name TBD by Joe) — TXT
4. **Sales by ASIN — 30-day rolling** (Business Reports) — CSV
5. **Sales by ASIN — 90-day rolling** (Business Reports) — CSV

## Google Sheets

- **Nerve Center:** Joe's business dashboard
- **Cron writes to:** Raw data dump tabs (not the dashboard layer)
- **Tabs are named consistently** — exact names TBD
- **Paste method:** Clear old data, paste new data to A1
- **Access:** Service account (not yet created) with Editor role

## Current State (2026-06-03)

**BLOCKED:** Amazon login not completed.
- Account created (Paul Stone / paul@5crests.com)
- Registration form submitted (hit CAPTCHA on step 2)
- Five failed headless Playwright attempts — STOPPED before ban threshold
- Joe cannot complete login from his browser (account linking risk)
- Next attempt: X11 forwarding (`ssh -X paul chromium-browser`) for one-time cookie grab, OR SP-API path

**Ready infrastructure:**
- Playwright + playwright-stealth installed
- Chromium installed (`/snap/bin/chromium`)
- himalaya CLI working for paul@5crests.com
- Twilio phone (855) 956-2656 ready for verification
- Google Sheets integration pending sheet access
