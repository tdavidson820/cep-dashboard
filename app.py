You are enhancing the current codebase you already updated for the CEP advocacy website. This is not a rebuild and not a redesign from scratch. This is a targeted enhancement pass on top of the current working version.

KEYWORD: ENHANCE THE CURRENT IMPLEMENTATION

The Wisconsin page is improved, but there are still important accuracy and usability issues that must be corrected. Update the existing code to address the following four items precisely.

PRIMARY GOAL
Enhance the existing Wisconsin inner state page so that:
- state executives visually reflect political affiliation
- the county coverage map accurately reflects Full CEP vs Partial CEP vs No CEP
- the county table filtering is cleaner and only attached to table headers
- the CEP status in the county table is clearly visible

Do not undo the prior improvements. Build on what already exists.

==================================================
REQUIRED ENHANCEMENTS
==================================================

1) STATE EXECUTIVES: COLOR NAMES BY POLITICAL AFFILIATION
The State Leadership / Key State Executives section needs one additional enhancement.

Requirement:
- The executive’s NAME should be colored according to political affiliation:
  - Republican = maroon
  - Democrat = blue

Implementation requirements:
- This must be data-driven, not hardcoded directly in the JSX/HTML
- Add a party field for each executive in the state executive data structure if it does not already exist
- Only the executive name should receive the political color treatment
- The role/title label should remain neutral and readable
- The color styling should still look polished and professional, not overly saturated or cartoonish
- Use a consistent maroon for Republican and a consistent blue for Democrat
- Preserve accessibility and sufficient contrast

Preferred executive data model:
- role
- name
- party

Example concept:
[
  { role: "Governor", name: "...", party: "Republican" },
  { role: "Treasurer", name: "...", party: "Democrat" }
]

Create a reusable helper or mapping so this can scale to South Carolina, New Jersey, and future states without reworking the component.

2) COUNTY COVERAGE MAP IS STILL INCORRECT
The county map for Wisconsin is still wrong. It is currently showing only one county as Full CEP, which is not correct.

This must be fixed so the county map fully and accurately reflects county CEP status based on the source data.

Required county map status categories:
- Full CEP = green
- Partial CEP = yellow
- No CEP = red

Requirements:
- The county-level choropleth or fill logic must map every Wisconsin county to the correct CEP status
- The county map must use the same underlying county status logic as the county detail table and any summary counts
- There must be a single source of truth for county status classification so the map, table, and summary metrics cannot drift apart
- Remove any stale or conflicting map logic that is causing the current mismatch
- Verify that the Wisconsin county map accurately reflects all counties, not just one or a small subset
- Ensure county FIPS / county names / join logic is working correctly so the proper fill colors are applied to all counties

Map colors must be exactly interpreted as:
- Full CEP = green
- Partial CEP = yellow
- No CEP = red

Implementation guidance:
- Audit the current join between county data and map geometry
- Confirm whether the error is caused by:
  - incorrect county name normalization
  - incorrect FIPS mapping
  - incorrect status mapping
  - fallback/default fill logic overriding real values
  - incomplete county dataset
- Fix the root cause, not just the visual symptom

Important:
The county map must visually agree with the county table and with the recalculated state metrics.

3) COUNTY DETAILS TABLE: FILTER FEATURE SHOULD ONLY BE FOR TABLE HEADERS
The County Details table still needs UX cleanup.

Requirement:
- The filter feature should only exist at the table header level
- Do not place filter UI inside random cells or in a way that disrupts the body rows
- The table should feel clean and structured
- If there are dropdowns, sort controls, or filter indicators, they must live in the header row only
- Body rows should contain only the county data, not extra filter controls
- Preserve readability and spacing

Interpretation:
- Header-based filtering/sorting is acceptable
- Floating filter elements embedded within the table body is not acceptable
- Do not clutter the rows with controls that make the table feel broken or jumbled

Please refactor the current table implementation so the filtering interaction is attached cleanly to the column headers only.

4) COUNTY DETAILS TABLE: CEP STATUS IS NOT VISIBLE ENOUGH
I still cannot clearly see the CEP status in the County Details table.

Requirement:
- Make the CEP status fully visible and immediately understandable
- The CEP Coverage Status column must clearly display:
  - Full CEP
  - Partial CEP
  - No CEP

Implementation requirements:
- Use strong, high-contrast status badges or pills
- Ensure the text itself is fully readable and not cut off
- Do not let the badge width collapse so tightly that the label becomes unreadable
- Increase padding, min-width, alignment, and contrast as needed
- Make sure the entire badge is visible in the table layout on desktop
- Preserve responsiveness on smaller screens
- If the current column width is too narrow, widen it
- Prevent overflow, clipping, truncation, or awkward wrapping that hides the status

Color system for badges:
- Full CEP = green
- Partial CEP = yellow
- No CEP = red

Design goal:
The status should be instantly scannable from the table without squinting or hovering.

==================================================
ARCHITECTURE REQUIREMENTS
==================================================

These enhancements must be applied to the CURRENT codebase, not by replacing everything.

Please preserve:
- the current page structure
- the current reusable state page architecture
- the current Google Sheet-driven Wisconsin data logic
- the current visual direction, unless adjustment is required for clarity and accuracy

Please improve:
- executive color treatment
- county map data accuracy and status rendering
- table header filtering behavior
- table status visibility

Use a shared status normalization approach so the same status value powers:
- summary cards
- county map
- county detail table
- any legends or counts

Avoid duplicate logic across components.

==================================================
VALIDATION REQUIREMENTS
==================================================

Before finalizing, validate all of the following:

STATE EXECUTIVES
- Executive names are color-coded by party
- Republican names are maroon
- Democrat names are blue
- Role labels remain neutral
- Styling still looks professional

COUNTY MAP
- Wisconsin county map correctly reflects Full CEP, Partial CEP, and No CEP across all counties
- Map coloring uses green / yellow / red exactly for those three categories
- Map status classification matches the county table and summary counts
- The prior issue where only one county appears Full CEP is resolved

COUNTY TABLE
- Filter functionality is attached only to table headers
- Table body contains only county data
- CEP Coverage Status is clearly visible
- Status badges are fully legible and not clipped or jumbled
- Status text is readable at a glance

REUSABILITY
- These enhancements are implemented in a reusable way so other state pages can use the same component logic

==================================================
OUTPUT FORMAT
==================================================

Do not give me pseudocode.
Do not give me a high-level plan only.
Do not describe what you might do.

I want:
1. The updated code in full for every file that changed
2. Any new helper, config, or mapping files required
3. A short explanation of what was fixed
4. A clear explanation of how county status is now normalized and shared across the map and table
5. Confirmation that this enhancement builds on the current implementation rather than replacing it

If you need to make reasonable implementation assumptions, proceed directly and update the code.
