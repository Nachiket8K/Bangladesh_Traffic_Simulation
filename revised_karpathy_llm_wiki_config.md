---
version: 2
updated: 2026-07-06
auto_suggestion_count: 5
schema_name: Second Brain Knowledge Graph Schema
governs:
  - Obsidian vault structure
  - Karpathy LLM Wiki output
  - AI-assisted note creation
  - textbook ingestion
  - project documentation
  - model registry
---

# Wiki Schema Configuration
## Second Brain Knowledge Graph Operating Standard

This file governs how the LLM builds, updates, links, classifies, and maintains the Obsidian second brain.

The vault is not a passive note store. It is a persistent knowledge graph for:

- research
- simulation and modelling
- decision support
- project execution
- reusable model development
- computational policy analysis
- geospatial and spatial data science
- DMDU, ABM, DES, SD, and hybrid modelling workflows

The vault is the authoritative source of truth. AI agents are assistants to the vault and must preserve structure, traceability, and reusability.

---

# 1. Governing Principles

## 1.1 Knowledge Is Permanent

The LLM MUST NOT delete, erase, or overwrite knowledge simply because it appears outdated.

Instead, it MUST:

- archive old information
- mark knowledge as superseded
- preserve historical context
- link old and new versions
- record contradictions with attribution

Destructive edits require explicit human instruction.

## 1.2 Every Note Has a Purpose

Every note MUST belong to one primary knowledge category:

- source
- concept
- method
- model
- project
- decision
- entity
- asset
- index
- log

The LLM MUST classify new notes before writing them.

## 1.3 Single Source of Truth

The LLM MUST avoid duplicate notes.

Before creating a page, the LLM MUST check whether an equivalent note already exists.

If a note already exists, the LLM MUST enrich the existing note rather than create a duplicate.

Allowed duplication only applies to:

- source notes preserving original material
- historical snapshots
- explicit versioned model cards
- reviewed human-created exceptions

## 1.4 Atomic Knowledge

Each concept, method, decision, model, or project note SHOULD focus on one primary idea.

Large topics MUST be decomposed into smaller notes and connected through links or MOCs.

Good note names:

- `concepts/urban-heat-island.md`
- `concepts/land-surface-temperature.md`
- `methods/performing-sensitivity-analysis.md`
- `models/abm-001-urban-heat-model.md`

Bad note names:

- `concepts/simulation-techniques-overview.md`
- `concepts/climate-modelling-gis-python-and-abm.md`

## 1.5 Reusability First

When project-specific knowledge can be reused, the LLM MUST extract it into a reusable note.

Reusable knowledge belongs in:

- `concepts/`
- `methods/`
- `models/`
- `decisions/`

Project folders should contain execution context, not the only copy of reusable knowledge.

---

# 2. Wiki Structure

The LLM MUST use the following structure unless explicitly instructed otherwise.

```text
wiki/
  index.md
  log.md
  sources/
  entities/
  concepts/
  methods/
  models/
  projects/
  decisions/
  assets/
  mocs/
  audits/
```

## 2.1 Page Locations

- Entity pages: `entities/`
- Concept pages: `concepts/`
- Method pages: `methods/`
- Model pages: `models/`
- Project pages: `projects/`
- Decision pages: `decisions/`
- Source pages: `sources/`
- Asset pages: `assets/`
- Map of Content pages: `mocs/`
- Audit reports: `audits/`
- Index: `index.md`
- Log: `log.md`

## 2.2 Legacy Compatibility

If the plugin expects only `entities/`, `concepts/`, and `sources/`, then:

- methods MAY be written as `concepts/` with `category: method`
- models MAY be written as `entities/` with `category: model`
- projects MAY be written as `entities/` with `category: project`
- decisions MAY be written as `concepts/` with `category: decision`

However, where possible, the preferred folders above SHOULD be used.

---

# 3. Frontmatter Standard

All LLM-created notes MUST include YAML frontmatter.

## 3.1 Required Common Fields

```yaml
type:
category:
created:
updated:
sources:
aliases:
tags:
status:
reviewed:
```

## 3.2 Field Definitions

- `type`: broad page class. Valid values: `source`, `entity`, `concept`, `method`, `model`, `project`, `decision`, `asset`, `moc`, `log`, `audit`
- `category`: more specific subtype, chosen from the category rules below
- `created`: ISO date of first creation, set by system where possible
- `updated`: ISO date of last update, set by system where possible
- `sources`: array of source file wiki-links
- `aliases`: optional alternative names, abbreviations, translations
- `tags`: controlled tags only
- `status`: `draft`, `active`, `review`, `evergreen`, `superseded`, `archived`
- `reviewed`: boolean; if true, the LLM MUST preserve the page and only append clearly new information

## 3.3 Date Fields

- `created:` and `updated:` SHOULD be filled by the system programmatically where supported.
- If the LLM must create them, use ISO format: `YYYY-MM-DD`.
- `created:` must be preserved during merge.
- `updated:` may be refreshed during merge.
- The LLM MUST NOT invent source publication dates unless present in the source.

---

# 4. Classification Rules

## 4.1 Entity Pages

Location:

```text
entities/
```

Valid categories:

- person
- organization
- project
- product
- event
- place
- institution
- dataset
- software
- other

Entity pages describe real-world or named things.

## 4.2 Concept Pages

Location:

```text
concepts/
```

Valid categories:

- theory
- field
- phenomenon
- standard
- term
- framework
- variable
- metric
- principle
- other

Concept pages describe ideas, phenomena, theories, or terms.

## 4.3 Method Pages

Location:

```text
methods/
```

Valid categories:

- workflow
- protocol
- algorithm
- procedure
- analysis-method
- modelling-method
- validation-method
- calibration-method
- data-processing-method
- uncertainty-method
- other

Method pages describe repeatable procedures.

## 4.4 Model Pages

Location:

```text
models/
```

Valid categories:

- abm
- des
- sd
- geospatial-model
- remote-sensing-model
- dmdu-model
- optimization-model
- ml-model
- hybrid-model
- other

Model pages describe reusable analytical or simulation models.

## 4.5 Project Pages

Location:

```text
projects/
```

Valid categories:

- client-project
- research-project
- internal-project
- proof-of-concept
- proposal
- case-study
- other

Project pages describe executed or planned work.

## 4.6 Decision Pages

Location:

```text
decisions/
```

Valid categories:

- technical-decision
- modelling-decision
- data-decision
- architecture-decision
- research-decision
- project-decision
- other

Decision pages record reasoning behind choices.

## 4.7 Source Pages

Location:

```text
sources/
```

Valid categories:

- paper
- book
- textbook
- report
- documentation
- website
- conversation
- note
- dataset
- other

Source pages preserve external or original material.

---

# 5. Naming Conventions

## 5.1 File Names

Filenames MUST be lowercase-with-hyphens.

Examples:

```text
concepts/urban-heat-island.md
methods/performing-sensitivity-analysis.md
models/abm-001-urban-heat-model.md
projects/2026-aurangabad-urban-heat.md
decisions/decision-use-h3-grid.md
```

## 5.2 Page Titles

Page titles SHOULD preserve the original language and accepted terminology.

The LLM MUST NOT translate entity or concept names unless the source itself provides a translated name.

## 5.3 Wiki Links

Use full-path wiki links:

```markdown
[[concepts/urban-heat-island|Urban Heat Island]]
[[methods/performing-sensitivity-analysis|Performing Sensitivity Analysis]]
[[models/abm-001-urban-heat-model|ABM_001 Urban Heat Model]]
```

Avoid vague links such as:

```markdown
[[analysis]]
[[model]]
[[data]]
```

---

# 6. Page Templates

## 6.1 Entity Page Template

Pages in `entities/` MUST follow this structure:

```markdown
---
type: entity
category:
created:
updated:
sources:
aliases:
tags:
status: draft
reviewed: false
---

# Page Title

## Basic Information

- Type:
- Category:
- Source file:

## Description

3-6 sentences with concrete facts and relevant bidirectional links.

## Related Entities

- [[entities/...|...]]

## Related Concepts

- [[concepts/...|...]]

## Related Methods

- [[methods/...|...]]

## Related Projects

- [[projects/...|...]]

## Mentions in Source

- "Verbatim quote" — [[sources/...|Source]]
```

## 6.2 Concept Page Template

Pages in `concepts/` MUST follow this structure:

```markdown
---
type: concept
category:
created:
updated:
sources:
aliases:
tags:
status: draft
reviewed: false
---

# Page Title

## Definition

Clear, concise definition.

## Why It Matters

Explain why this concept is useful in research, modelling, or project work.

## Key Characteristics

- Characteristic 1
- Characteristic 2
- Characteristic 3

## Related Concepts

- [[concepts/...|...]]

## Methods Using This Concept

- [[methods/...|...]]

## Models Using This Concept

- [[models/...|...]]

## Projects Using This Concept

- [[projects/...|...]]

## References

- [[sources/...|...]]

## Mentions in Source

- "Verbatim quote" — [[sources/...|Source]]
```

## 6.3 Method Page Template

Pages in `methods/` MUST follow this structure:

```markdown
---
type: method
category:
created:
updated:
sources:
aliases:
tags:
status: draft
reviewed: false
---

# Method Name

## Purpose

What the method is used for.

## Inputs

- Required input 1
- Required input 2

## Procedure

1. Step one
2. Step two
3. Step three

## Outputs

- Output 1
- Output 2

## Assumptions

- Assumption 1
- Assumption 2

## Limitations

- Limitation 1
- Limitation 2

## Related Concepts

- [[concepts/...|...]]

## Related Methods

- [[methods/...|...]]

## Example Applications

- [[projects/...|...]]

## Mentions in Source

- "Verbatim quote" — [[sources/...|Source]]
```

## 6.4 Model Page Template

Pages in `models/` MUST follow this structure:

```markdown
---
type: model
category:
model_id:
created:
updated:
sources:
aliases:
tags:
status: draft
reviewed: false
---

# Model Name

## Purpose

What problem the model solves.

## Domain

Relevant domain or application area.

## Methodology

ABM, DES, SD, DMDU, geospatial, hybrid, or other approach.

## Inputs

- Input 1
- Input 2

## Outputs

- Output 1
- Output 2

## Assumptions

- Assumption 1
- Assumption 2

## Calibration

How the model is calibrated.

## Validation

How the model is validated.

## Limitations

Known limitations.

## Related Concepts

- [[concepts/...|...]]

## Related Methods

- [[methods/...|...]]

## Projects Using This Model

- [[projects/...|...]]

## Version History

- Version:
- Change:
- Date:
```

## 6.5 Project Page Template

Pages in `projects/` MUST follow this structure:

```markdown
---
type: project
category:
project_id:
created:
updated:
sources:
aliases:
tags:
status: active
reviewed: false
---

# Project Name

## Problem Statement

What problem the project addresses.

## Objectives

- Objective 1
- Objective 2

## Stakeholders

- [[entities/...|...]]

## Data

- Dataset 1
- Dataset 2

## Methods

- [[methods/...|...]]

## Models

- [[models/...|...]]

## Assumptions

- Assumption 1
- Assumption 2

## Experiments

- Experiment 1
- Experiment 2

## Results

Main findings and outputs.

## Decisions

- [[decisions/...|...]]

## Lessons Learned

Reusable lessons extracted from the project.

## Reusable Knowledge Extracted

- [[concepts/...|...]]
- [[methods/...|...]]
- [[models/...|...]]
```

## 6.6 Decision Page Template

Pages in `decisions/` MUST follow this structure:

```markdown
---
type: decision
category:
created:
updated:
sources:
aliases:
tags:
status: active
reviewed: false
---

# Decision - Topic

## Problem

What decision had to be made.

## Context

Relevant project, model, method, or source context.

## Options Considered

### Option 1

Pros:
- ...

Cons:
- ...

### Option 2

Pros:
- ...

Cons:
- ...

## Decision

Final choice.

## Reason

Why this option was selected.

## Consequences

Expected implications, risks, and trade-offs.

## Related Notes

- [[projects/...|...]]
- [[models/...|...]]
- [[methods/...|...]]
```

## 6.7 Source Page Template

Pages in `sources/` MUST follow this structure:

```markdown
---
type: source
category:
created:
updated:
sources:
aliases:
tags:
status: draft
reviewed: false
source_note:
---

# Source Title

## Summary

Brief description of the source content.

## Key Points

- Main insight 1
- Main insight 2
- Main insight 3

## Mentioned Pages

- [[entities/...|...]]
- [[concepts/...|...]]
- [[methods/...|...]]

## Extracted Concepts

- [[concepts/...|...]]

## Extracted Methods

- [[methods/...|...]]

## Extracted Models

- [[models/...|...]]

## Project Applications

- [[projects/...|...]]
```

---

# 7. Link Creation Rules

The vault is a knowledge graph. Links are mandatory.

## 7.1 Minimum Link Requirements

Every LLM-created note MUST have:

- at least 1 outgoing link
- preferably 3 meaningful outgoing links
- source attribution where applicable

Target:

- 5-15 meaningful links per mature note

Avoid:

- 50+ low-quality links
- links created only because pages are in the same folder
- vague links to generic terms

## 7.2 Link Types

The LLM MUST create meaningful links of the following types where relevant.

### Upward Links

Connect a note to broader concepts.

Example:

```markdown
[[concepts/land-surface-temperature|Land Surface Temperature]]
is part of
[[concepts/urban-heat-modelling|Urban Heat Modelling]]
```

### Downward Links

Connect a broad note to sub-concepts.

Example:

```markdown
[[concepts/urban-heat-modelling|Urban Heat Modelling]]
links to:
- [[concepts/land-surface-temperature|Land Surface Temperature]]
- [[concepts/albedo|Albedo]]
- [[concepts/vegetation-cooling|Vegetation Cooling]]
```

### Lateral Links

Connect related but non-hierarchical ideas.

Example:

```markdown
[[methods/agent-based-modelling|Agent-Based Modelling]]
relates to
[[methods/system-dynamics|System Dynamics]]
and
[[methods/discrete-event-simulation|Discrete Event Simulation]]
```

### Project Links

Projects MUST link to concepts, methods, models, data, and decisions used.

### Model Links

Models MUST link to methods, assumptions, validation procedures, and projects using them.

### Decision Links

Decision notes MUST link to the affected project, model, method, or source.

## 7.3 Bidirectional Link Policy

When adding a major link from Note A to Note B, the LLM SHOULD update Note B with a reciprocal contextual link if safe.

Example:

If a project links to a model, the model should include the project under `Projects Using This Model`.

## 7.4 No Orphan Notes

The LLM MUST NOT intentionally create orphan notes.

An orphan note is a note with no meaningful inbound or outbound links.

If a note cannot be linked, it should be placed in review status.

---

# 8. Maps of Content

MOC pages live in:

```text
mocs/
```

## 8.1 MOC Creation Criteria

Create a MOC when:

- a domain contains more than 20 notes
- a project area becomes hard to navigate
- multiple sub-domains emerge
- a field is central to the user’s work

## 8.2 MOC Template

```markdown
---
type: moc
category:
created:
updated:
sources:
aliases:
tags:
status: active
reviewed: false
---

# MOC - Domain Name

## Purpose

Navigation entry point for this domain.

## Core Concepts

- [[concepts/...|...]]

## Core Methods

- [[methods/...|...]]

## Models

- [[models/...|...]]

## Projects

- [[projects/...|...]]

## Sources

- [[sources/...|...]]

## Open Questions

- Question 1
```

---

# 9. Tagging Policy

Tags are secondary. Links are primary.

The LLM MUST NOT create uncontrolled tags from extracted concept names.

Tags should describe workflow, status, domain, or note role.

## 9.1 Valid Status Tags

- `#draft`
- `#active`
- `#review`
- `#evergreen`
- `#superseded`
- `#archived`

## 9.2 Valid Role Tags

- `#source`
- `#concept`
- `#method`
- `#model`
- `#project`
- `#decision`
- `#asset`
- `#moc`
- `#audit`

## 9.3 Valid Domain Tags

- `#geospatial`
- `#simulation`
- `#abm`
- `#des`
- `#system-dynamics`
- `#dmdu`
- `#remote-sensing`
- `#climate`
- `#urban-systems`
- `#transport`
- `#energy`
- `#water`
- `#disaster-risk`
- `#policy`
- `#spatial-data-science`

## 9.4 Valid Source Tags

- `#source/textbook`
- `#source/paper`
- `#source/report`
- `#source/documentation`
- `#source/dataset`
- `#source/conversation`

## 9.5 Invalid Tag Behaviour

If a potential tag is not in the controlled vocabulary:

- do not add it as a tag
- create or link to a concept page instead

Example:

Do not create:

```markdown
#urban-heat-island
```

Use:

```markdown
[[concepts/urban-heat-island|Urban Heat Island]]
```

---

# 10. Textbook Ingestion Rules

The LLM may process textbooks, books, PDFs, or long documents.

## 10.1 Ingestion Workflow

```text
Original Source
↓
Source Page
↓
Chapter / Section Summaries
↓
Atomic Concept Notes
↓
Method Notes
↓
Model Notes
↓
MOC Updates
↓
Project Application Links
```

## 10.2 Textbook Output Locations

Original source summary:

```text
sources/
```

Concepts:

```text
concepts/
```

Methods:

```text
methods/
```

Models:

```text
models/
```

Navigation pages:

```text
mocs/
```

Review queue where available:

```text
review/
```

## 10.3 Chunking Rules

When breaking a textbook into chunks, the LLM MUST:

- preserve the source reference
- maintain chapter and section context
- avoid creating notes that are too broad
- avoid creating notes that are too small to be useful
- create one note per reusable concept or method
- link child notes back to the source page
- preserve verbatim quotes only in `Mentions in Source`

## 10.4 Textbook Chunk Size Guidance

Preferred chunk sizes:

- chapter summaries: 500-1000 words
- section summaries: 250-600 words
- atomic concept notes: 150-500 words
- method notes: 300-800 words

The LLM should prioritize conceptual coherence over exact word count.

---

# 11. Research Processing Workflow

The LLM MUST NOT leave research notes isolated.

Research should flow as follows:

```text
Source
↓
Source Note
↓
Extracted Concepts
↓
Extracted Methods
↓
Extracted Models
↓
Project Applications
```

Each source note SHOULD list:

- extracted concepts
- extracted methods
- extracted models
- related projects
- key quotes
- unresolved questions

---

# 12. Project Lifecycle Rules

Projects MUST act as execution records.

They MUST link outward to reusable knowledge.

## 12.1 Required Project Files or Sections

Each project should contain:

- problem statement
- stakeholders
- data
- assumptions
- methods
- model design
- experiments
- results
- decisions
- lessons learned
- reusable knowledge extracted

## 12.2 Project Closure Rule

At project completion, the LLM MUST create or update:

- project summary
- lessons learned
- decision records
- model cards
- reusable method notes
- relevant MOCs

---

# 13. Model Registry Rules

Every reusable model MUST have a model card.

## 13.1 Required Model Card Fields

- purpose
- domain
- methodology
- inputs
- outputs
- assumptions
- calibration
- validation
- limitations
- example applications
- projects using the model
- version history

## 13.2 Model IDs

Use this naming pattern:

```text
MODELTYPE_###_Name
```

Examples:

```text
ABM_001_UrbanHeat
DES_003_ClinicFlow
SD_002_WaterDemand
DMDU_001_AdaptationPathways
GEO_001_HeatExposure
```

---

# 14. Multi-Source Merge Rules

When new information is extracted into an existing note:

## 14.1 Sources

Append new sources. Never overwrite the existing sources array.

## 14.2 Aliases

Append new aliases. Never remove existing aliases unless explicitly instructed.

## 14.3 Reviewed Pages

If `reviewed: true`, preserve all existing content.

The LLM may only append clearly new information and must not restructure reviewed pages without explicit permission.

## 14.4 Contradictions

If sources disagree, preserve both views with attribution.

Create a section:

```markdown
## Contradictions

- Source A says ...
- Source B says ...
- Status: unresolved
```

Severity levels:

- warning
- conflict
- error

## 14.5 No New Content

Return or log:

```text
NO_NEW_CONTENT
```

if the source adds nothing materially new.

---

# 15. Mentions Format

Mentions in Source entries use academic-footnote style with source attribution.

Format:

```markdown
- "Verbatim quote in original language" — [[sources/source-name|Display Name]]
```

Rules:

- quotes must be verbatim
- quotes must not be paraphrased
- quotes must not be translated away from the original
- the source wiki-link is required
- multiple quotes from the same source may appear in the same section

Summaries and descriptions may be written in the wiki output language, but mentions must preserve original wording.

---

# 16. AI Behaviour Rules

The LLM MUST:

- preserve structure
- maintain links
- avoid duplication
- classify notes before writing
- extract reusable knowledge from projects
- record decisions
- update project memory where available
- prefer existing notes over new notes
- preserve human-reviewed content
- use source attribution
- create review status when uncertain
- write in clear, reusable language

The LLM MUST NOT:

- delete information without explicit instruction
- create duplicate concepts
- create orphan notes
- invent tags outside the controlled vocabulary
- store reusable knowledge only inside projects
- break established naming conventions
- hallucinate sources
- invent dates
- silently overwrite reviewed notes
- create broad unstructured notes where atomic notes are more appropriate

---

# 17. Human Review Rules

The LLM SHOULD place uncertain outputs into review status.

Use:

```yaml
status: review
reviewed: false
```

Human-reviewed notes may be marked:

```yaml
reviewed: true
status: evergreen
```

Once reviewed, the LLM must treat the note as protected.

---

# 18. Maintenance Policies

The LLM or audit process should periodically evaluate:

## 18.1 Orphan Notes

Target: 0

## 18.2 Notes With No Outgoing Links

Target: 0

## 18.3 Duplicate Concepts

Target: 0

## 18.4 Notes With Fewer Than 3 Links

Status: review recommended

## 18.5 Stale Notes

Stale threshold: 90 days without updates.

Stale does not mean wrong. Stale means review may be useful.

## 18.6 Broken Links

Missing page references should be listed in an audit report.

## 18.7 Outdated MOCs

MOCs should be reviewed when many new notes are added to a domain.

---

# 19. Audit Report Template

Audit reports live in:

```text
audits/
```

Template:

```markdown
---
type: audit
category: vault-audit
created:
updated:
sources:
aliases:
tags:
  - audit
status: review
reviewed: false
---

# Vault Audit - YYYY-MM-DD

## Summary

Brief summary of graph health.

## Orphan Notes

- Note 1

## Duplicate Candidates

- Note A / Note B

## Broken Links

- Missing link

## Notes Needing More Links

- Note 1

## MOCs Needing Updates

- MOC 1

## Recommended Actions

1. Action
2. Action
```

---

# 20. Output Language

The LLM should write summaries, descriptions, and explanations in the configured wiki output language.

Entity and concept names should preserve their original source language unless an accepted English technical term already exists.

---

# 21. Final Operating Rule

When uncertain, the LLM should prefer:

```text
Create Link
```

rather than:

```text
Create Folder
```

and prefer:

```text
Create Reusable Knowledge
```

rather than:

```text
Store Information Only Inside a Project
```

The vault succeeds when knowledge becomes increasingly:

- reusable
- traceable
- connected
- clear
- source-grounded
- useful for future modelling and project execution
