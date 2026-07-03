---
name: amazon-seller-automation
description: Automate Amazon Seller Central report downloads, parsing, and delivery to Google Sheets. Covers Playwright browser automation, SP-API integration, credential management, CAPTCHA avoidance, and the full pipeline architecture.
category: productivity
---

# Amazon Seller Central Report Automation

## When to Use

When the user wants to automate downloading reports from Amazon Seller Central — especially FBA fulfillment reports, sales reports, and inventory reports — and deliver them to Google Sheets or another destination on a schedule.

## Architecture Decision: Playwright vs SP-API

### Playwright (Browser Automation)

**Quick to build, fragile long-term.** Scripts log into Seller Central as the user, click through report requests, wait for generation, and download. Works immediately but breaks when Amazon redesigns their UI.

**When to use:** Rapid prototyping, one-off data pulls, testing report formats before committing to SP-API.

**Requirements:**
- Amazon Seller Central credentials with report access
- Playwright + playwright-stealth installed
- A cookie/session persistence strategy (save storage state after manual login)
- Twilio or similar for phone verification (if 2FA is enabled)

### SP-API (Selling Partner API)

**Permanent solution.** Amazon's official API for sellers. No browser, no CAPTCHAs, no UI fragility. One-time setup pain for permanent access.

**When to use:** Production automation, cron jobs, anything you're charging money for.

**Setup required:**
- Developer registration in Seller Central
- IAM role with Reports API access only (read-only — no inventory modification)
- App listing (for public distribution) or private authorization (for single account)
- SP-API access keys and refresh token

**Monetization angle:** Amazon's report automation is a gap in the market — multi-million dollar industry, Amazon won't build scheduled report delivery, Amazon employees run competing solutions. A simple SP-API → Google Sheets pipeline is a legitimate SaaS product at $4.99/mo.

## Anti-Bot Pitfalls (HARD RULES)

### 1. Stop After 2-3 Failed Login Attempts

Amazon's anti-bot detection is among the most aggressive of any platform. Multiple rapid headless login attempts from a VPS IP will trigger a permanent ban — not just CAPTCHA, but account termination. **Stop after 2-3 failures and pivot to a different path.**

### 2. Account Linking Risk

Amazon detects when the same browser/IP/machine is used for multiple seller accounts. This means:
- **Never log into Paul's Seller Central from Joe's browser.** If Amazon detects both accounts on the same machine, both get banned.
- **Use a clean environment for first login.** Fresh browser profile, different IP. Coffee shop WiFi on a phone works. X11 forwarding from VPS (`ssh -X`) works because Amazon sees the VPS IP, not the local one.

### 3. Headless Detection

`playwright-stealth` helps but isn't foolproof. Amazon's two-step login (email → password) is particularly difficult in headless mode because the password field appears dynamically via JavaScript. Even with stealth, the transition may fail.

**Known working approach:** Manual login once via X11 Chromium (`ssh -X paul chromium-browser`), then save the authenticated browser storage state. Subsequent automation uses the saved state to skip login entirely. Cookies typically last weeks to months.

## Pipeline Architecture

```
Cron fires daily
  → Playwright (with saved auth state) navigates to Seller Central
  → Requests reports with date parameters
  → Waits for generation (polling)
  → Downloads CSV/TXT files
  → Parses data
  → Clears target tab in Google Sheet
  → Pastes data to A1
  → Deletes local files
  → DMs user confirmation (or error details)
```

## Google Sheets Integration

The cron job writes to raw data dump tabs only — not the dashboard/nerve center layer. Google Sheets formulas in the dashboard pull from these tabs.

**Access model:** Service account with Editor role on the sheet, shared via the service account email. User can revoke access anytime. Never use the user's personal Google credentials.

## Standard Amazon Reports

Common report types for FBA sellers:

| Report | Type | Frequency |
|--------|------|-----------|
| Restock Inventory | FBA Fulfillment | Daily |
| Fee Preview | FBA Fulfillment | Daily |
| Inventory Health | FBA Fulfillment | Daily |
| Sales by ASIN (30-day) | Business Reports | Daily |
| Sales by ASIN (90-day) | Business Reports | Daily |

Report formats vary — some are CSV, some are TXT (tab-delimited). Amazon occasionally changes column layouts. Build parsing with defensive defaults.

## Infrastructure Checklist

- [ ] Playwright installed (`pip install playwright --break-system-packages && playwright install chromium`)
- [ ] playwright-stealth installed (`pip install playwright-stealth --break-system-packages`)
- [ ] Chromium available on VPS (`/snap/bin/chromium` or apt install)
- [ ] Twilio account with funded phone number for SMS verification
- [ ] himalaya CLI configured for receiving verification emails
- [ ] Google Sheets service account with Editor access
- [ ] Saved browser auth state from one-time manual login
- [ ] Cron job configured with the automation script

## References

- `references/pipeline-setup.md` — Session-specific setup details: credentials, report types, sheet structure
- `references/fba-shipment-sop.md` — Manual FBA shipment creation SOP (three-phase process: Box Prep → Google Sheets Template → Seller Central "Send to Amazon"). Documented from Joe's voice dictation 2026-06-15. Two open items pending.
- `references/fba-manual-shipment-workflow.md` — Current manual FBA shipment creation process: box prep → Google Sheets template → Seller Central "Send to Amazon." Includes Seller Central navigation paths useful for browser automation.
