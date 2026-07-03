# FBA Shipment Creation — Manual SOP

Captured 2026-06-15 from Joe's voice dictation. This is the current manual process for creating an FBA shipment. Useful as reference for what to eventually automate, and as training documentation for team members.

The canonical working copy lives at:
`/root/.hermes/docs/Paul/workspace/FBA_Shipment_SOP_2026-06-15_Paul.md`

## Process Summary (Three Phases)

### Phase 1: Box Prep
- Identify shipment SKUs from Amazon Operations Worksheet (internal sheet, not Seller Central)
- Divide total quantity by 5 — all shipments use 5 boxes
- **Critical:** Every box must have the exact same unit count. Uneven distribution = placement fee (hundreds of dollars)
- Pack, seal, measure weight + dimensions for all 5 boxes

### Phase 2: Google Sheets Template
- Open Shipment Template in Google Drive (link TBD — Joe to provide)
- Use "Create Workflow Template" function (macro/button/menu — TBD)
- Enter M SKUs and quantities
- Download as .xlsx

### Phase 3: Seller Central "Send to Amazon"
- Navigate: ☰ → Inventory → Shipments → "Send to Amazon" link (upper right, text link left of Fulfillment Center button)
- SKU Selection: "File upload" (NOT "Select from list")
- Confirm ship-from address, marketplace = United States
- Skip past Amazon's native template section → Step 3: Upload completed file
- Upload the .xlsx → generates "Ready to pack" list
- "Pack individual units" → confirm units
- Packing info: "Multiple boxes will be needed" → 5 boxes → "Open web form"
- Web form: units per box (use Tab to rapid-fire through fields), weight, dimensions
- Dimensions: checkboxes at bottom — same-size boxes check once; different sizes add entries and check per-box
- Confirm packing information → generates shipment + labels

## Open Items
1. "Create Workflow Template" — macro, menu item, or button in the Google Sheet?
2. Shipment Template Google Drive link
