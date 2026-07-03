# FBA Manual Shipment Workflow

**Date:** 2026-06-15
**Source:** Joe Gray voice notes
**Purpose:** Document the current manual FBA shipment creation process. This is the "before" state — what automation would replace or assist. Seller Central navigation paths are useful for any browser-automation attempt.

---

## Process Overview

Three phases: Box Prep → Google Sheets Template → Seller Central "Send to Amazon"

---

## Phase 1: Box Prep (Warehouse)

1. **Identify shipment SKUs** from the Amazon Operations Worksheet (internal spreadsheet — not a Seller Central report)
2. **Divide quantity by 5** — all shipments use 5 boxes
3. **Pack the 5 boxes** with allocated quantities
4. **Record weight and dimensions** for each fully packed box

---

## Phase 2: Google Sheets Template

1. Open the **Shipment Template** in Google Drive (internal link)
2. Use **"Create Workflow Template"** — a function within the template sheet that generates a fresh shipment document
3. Enter **Merchant SKU** (M SKU) — pulled from Operations Worksheet
4. Enter **quantity** per SKU per box
5. **File → Download → Microsoft Excel (.xlsx)**

---

## Phase 3: Seller Central — Send to Amazon

### Navigation Path
1. Log into **Amazon Seller Central**
2. **Hamburger menu (☰)** — upper left corner
3. Click **Inventory** from the dropdown
4. Midway down the Inventory page, click **Shipments**
5. Upper right corner: click **"Send to Amazon"** link
   - Appears as a text link, not a button
   - Sits to the left of the "Fulfillment Center" button
6. Upload the .xlsx from Phase 2

### UI Notes
- "Send to Amazon" is a **link**, not a button — easy to miss on the page
- The hamburger → Inventory → Shipments path is the standard navigation for FBA shipment creation

---

## Key Resources

| Resource | Location |
|----------|----------|
| Amazon Operations Worksheet | Internal spreadsheet (not Seller Central) |
| Shipment Template | Google Drive — internal |
| Seller Central | sellercentral.amazon.com |

---

## Automation Implications

- The Google Sheets → .xlsx download step happens in Google Drive, not Seller Central
- The Shipment Template with "Create Workflow Template" function is the key document — automating this requires Google Sheets API access
- Seller Central navigation is standard and reachable via Playwright with saved auth state
- The Operations Worksheet being internal means any automation needs access to that spreadsheet separately from Seller Central reports
