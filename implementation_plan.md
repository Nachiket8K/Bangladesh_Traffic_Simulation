# Implementation Plan

[Overview]
Create beginner-friendly documentation in the `docs/` site that explains the Assignment 1 data sources and preprocessing workflow, with the first deliverable focused on `docs/method/data.md` and the material in `Lab 1/`.

The repository already has a Jekyll documentation structure under `docs/`, and the navigation is prepared for a `Data & Preprocessing` page via `docs/method/data.md` and the link in `docs/toc.md`. However, the current page is only a placeholder and does not explain what data exists, where it comes from, how it is structured, or how the Assignment 1 notebooks clean it. The implementation should replace that placeholder with an explanatory document that is understandable to someone who has never seen the repository before.

The documentation should use `Lab 1` as the authoritative source for the data-cleaning story because that folder contains the assignment brief, the team report, the notebooks (`TCVData.ipynb`, `RoadsLRP.ipynb`, `Bridges.ipynb`), the raw/processed data artifacts in `Lab 1/data/`, and the assignment-specific README. The content should explain the relationship between the RMMS and BMMS-derived files, identify the key fields used by later labs, and narrate the actual cleaning logic that appears in the notebooks rather than giving only high-level claims.

The documentation should also be honest about limitations and incompleteness visible in the notebooks and report. For example, some bridge-cleaning steps are exploratory and not fully completed, the road-cleaning notebooks rely on heuristics and manual inspection, and later labs may consume cleaned infrastructure files without reproducing every transformation. The page should therefore distinguish between raw inputs, cleaned outputs, implemented cleaning rules, and proposed-but-unfinished next steps.

[Types]
No application type system changes are required; the only structured additions are documentation content sections that describe existing dataset schemas and preprocessing concepts.

- Documentation section structure for `docs/method/data.md`:
  - `Overview of Assignment 1 Data`
  - `Where the Data Comes From`
  - `Core Files Used in Preprocessing`
  - `Raw vs Processed Data Layout`
  - `Road Geometry Data: _roads.tcv`
  - `Road LRP Table: Roads_InfoAboutEachLRP.xlsx`
  - `Bridge Inventory: BMMS_overview.xlsx`
  - `Cleaning Workflow Implemented in the Notebooks`
  - `Known Data Quality Issues`
  - `Outputs Passed to Later Stages`
  - `Limitations and Open Questions`

- Dataset descriptions to include explicitly:
  - `_roads.tcv`: tab-separated road geometry file storing one road per line with repeated `(lrp, lat, lon)` triplets.
  - `Roads_InfoAboutEachLRP.xlsx`: row-based table of LRPs with road id, coordinates, chainage, and descriptive attributes.
  - `BMMS_overview.xlsx`: bridge inventory table with bridge identifiers, road/LRP references, coordinates, dimensions, condition, and year/span metadata.

- Validation rules to document in prose:
  - Latitude/longitude values must be numeric for downstream plotting and network construction.
  - `road + lrp` or `road + LRPName` combinations are used as location keys during matching and duplicate detection.
  - Duplicate bridge rows are resolved by preferring rows with fewer missing values and newer construction year ordering in the notebook logic.
  - Missing or obviously invalid road coordinates are corrected heuristically using neighboring LRP points.

[Files]
The implementation only modifies documentation and planning artifacts, while referencing existing Assignment 1 source materials.

- New files to be created:
  - None required for this first documentation slice unless the implementation agent decides to add an image/table partial under `docs/assets/` after confirming it improves clarity.

- Existing files to be modified:
  - `implementation_plan.md` - create and maintain this documentation-focused implementation plan.
  - `docs/method/data.md` - replace the placeholder text with a detailed explanation of Assignment 1 data and preprocessing.
  - `docs/method.md` - optionally expand the section intro so the `Data & Preprocessing` page is introduced as the Lab 1 foundation of the project.
  - `docs/index.md` - optionally adjust the home-page summary so newcomers know the documentation now includes a data-origins explanation.
  - `docs/toc.md` - only modify if the page title or location changes; otherwise leave as-is because it already links to `/method/data/`.

- Existing source/reference files to read but not modify:
  - `Lab 1/README.md`
  - `Lab 1/TCVData.ipynb`
  - `Lab 1/RoadsLRP.ipynb`
  - `Lab 1/Bridges.ipynb`
  - `Lab 1/data/raw/_roads.tcv`
  - `Lab 1/data/processed/_roads.tcv`
  - `Lab 1/data/raw/BMMS_overview.xlsx`
  - `Lab 1/data/processed/BMMS_overview.xlsx`
  - `EPA1352 Assignment 1 - Data Quality v2.pdf`
  - `Lab 1/EPA1352-G17-A1.pdf`

- Files to be deleted or moved:
  - None.

- Configuration file updates:
  - None expected; the current Jekyll front matter in `docs/method/data.md` should remain compatible.

[Functions]
No production-code function changes are required; the work consists of documentation authoring grounded in existing notebook logic.

- New functions:
  - None.

- Modified functions:
  - None.

- Removed functions:
  - None.

[Classes]
No class modifications are required because the deliverable is repository documentation rather than executable feature work.

- New classes:
  - None.

- Modified classes:
  - None.

- Removed classes:
  - None.

[Dependencies]
No dependency changes are required; the existing fresh virtual environment should only be used for inspection or optional validation of notebook-readable assets.

- Use the repository’s fresh environment at `.venv_fresh` for any verification commands that need Python.
- Prefer existing libraries already present in the coursework environment, especially `pandas`, `openpyxl`, and notebook tooling, if the implementation agent wants to inspect spreadsheet headers or sample rows.
- Do not add packages unless a documentation-generation step proves impossible with the current environment.

[Testing]
Testing focuses on documentation accuracy, completeness, and successful site integration rather than unit tests.

- Validation steps:
  1. Re-read `docs/method/data.md` after editing and confirm it explains the three primary Assignment 1 data assets, their purpose, and their cleaned outputs.
  2. Confirm every major cleaning claim in the document is traceable to at least one of `Lab 1/TCVData.ipynb`, `Lab 1/RoadsLRP.ipynb`, `Lab 1/Bridges.ipynb`, `Lab 1/README.md`, or `Lab 1/EPA1352-G17-A1.pdf`.
  3. Ensure the page distinguishes clearly between implemented cleaning steps and unfinished/proposed next steps, especially for bridge-road matching.
  4. Verify the front matter in `docs/method/data.md` remains valid so the page stays in the Method & Model navigation tree.
  5. Optionally run a local docs preview or inspect the markdown rendering if a local Jekyll workflow already exists; if not, at minimum check for broken markdown structure.

[Implementation Order]
Implement the documentation in the order that minimizes re-reading and keeps every narrative section grounded in specific Assignment 1 evidence.

1. Re-read the current `docs/method/data.md` placeholder and replace its outline with a detailed content structure aligned to newcomer needs.
2. Inspect the Assignment 1 notebooks and report closely enough to extract exact dataset roles, cleaning steps, heuristics, and limitations.
3. Cross-check the raw/processed file layout in `Lab 1/data/` so the documentation names the correct source and output artifacts.
4. Write the new `docs/method/data.md` content, explaining the available data, the required cleaning steps, and how those steps were actually carried out.
5. Make any minimal supporting updates to `docs/method.md` or `docs/index.md` only if needed to better surface the new page.
6. Re-read the edited documentation for factual consistency, markdown quality, and alignment with the existing docs navigation.
