# The Real Estate Roundup — Website

New website for **The Real Estate Roundup** (Lincoln County Edition & Otero County Edition,
Ruidoso, New Mexico — 26 years in print).

**Current status (October 2026): WORKING PROTOTYPE with real data.**
The homepage now renders all 358 listings extracted from the October 2026 Lincoln County
Edition's InDesign (IDML) files — price, MLS #, beds/baths, acreage, status badges, agent
contact where printed — with working search, town filters, status filter and price sort.
Listings data pipeline: IDML → extract.py → listings.json → generate_site.py → index.html
(see ~/workspace/real-estate-round-up-extraction/ MONTHLY-PIPELINE.md for the runbook;
not in this repo).

Publisher rules encoded here (per Susan Hixon, 2026-10-13):
- Title is NEVER hyphenated in visible copy: "The Real Estate Roundup".
- The old phone number is retired — never publish it.
- The advertising phone appears ONLY behind the "Advertise in The Real Estate Roundup"
  click-to-reveal.
- No general contact info / no free-magazine request form: viewers contact listing
  agents/brokerages directly.

Open items:
- Listing photos: Susan's Drive upload contained only logo/headshot links; the MLS-named
  photo files (327 referenced) still need uploading from her machine, then
  photo_extract.py populates them.
- Otero County Edition: same pipeline once its package arrives.
- Custom domain: old domain appears lapsed/taken over (as of 2025); recovery or a
  replacement domain is still to be decided with the family.
