# Ordering notes

## Mouser

- **Quantity 0 becomes 1.** Mouser's BOM upload enforces a minimum quantity of 1 per line, so a row with quantity 0 is added to the cart as 1. To leave a part out, delete its row from the BOM before uploading. Don't set it to 0. (Found 2026-11-20: the IRLZ44N row at quantity 0 became 1 MOSFET.)
- Mouser's BOM tool needs only the **Mouser Part Number** and **Quantity** columns. The other columns in `mouser_bom.xlsx` are notes for us.
- Unit prices in the BOM spreadsheet come from the Mouser API at the time it was made and don't follow price breaks when quantities change. Mouser shows live pricing on upload.

## OSH Park

- OSH Park parses the KiCad 10 `.kicad_pcb` directly, so we don't need to generate Gerbers.
- It detected the USB-C jack's plated shell slots as "supported drilled slots".
