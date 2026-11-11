# Reusable Presentation Assets

This folder holds **reusable** external-presentation baselines — not opportunity-tailored materials.

It includes:
- Comprehensive resume content baseline (`Resume_Master/`); canonical experience remains in `02_Work_Experience/`
- DOCX and markdown templates (`Templates/`)
- Online profile text (`Online_Profiles/`)
- Non-opportunity shareable baselines (e.g. `shareable_*` resumes)
- Optional track-specific presentation baselines, with internal provenance recorded as described below

## Key Rule
This folder **consumes** information from other folders.
It should not be the place where experience is invented or remembered.

Opportunity-tailored resumes, cover letters, and application execution artifacts live in each opportunity folder under `../06_Job_Opportunities/<company>_<role>_<date>/` as:
- `resume.md`
- `cover-letter.md`
- `application-notes.md` / `application-record.md` / `next-steps.md`
- long-named `.docx`/`.pdf` shareables produced by `scripts/generate-*-docx.sh`

## How to Use
- Pull raw content from `02_Work_Experience`
- Pull positioning cues from `04_Career_Goals_and_Strategy`
- Use templates and the master resume as baselines for `/build-resume` and `/build-application`
- Optimize language for clarity and alignment, not completeness


## Track-Aware Resume Workflow

Career tracks and role-target mappings live in `../04_Career_Goals_and_Strategy/career-tracks.md`. Track 1 — Independent Consulting — is the long-term direction; the employment resume workflows use Tracks 2, 3, 4, 5, and 9.

| Track | Lead positioning | Governing role target |
|-------|------------------|-----------------------|
| `track-2` | Software product / engineering outcomes and the product-development system | `../04_Career_Goals_and_Strategy/Role_Targets/role-target-software-product-engineering-leadership.md` |
| `track-3` | MSP customer/account ownership, technical fluency, service coordination, and business judgment | `../04_Career_Goals_and_Strategy/Role_Targets/role-target-msp-technical-account-manager.md` |
| `track-4` | Strategic Portfolio & Transformation Governance: portfolio architecture, decision systems, transformation operating models, executive insight, and grounded value-realization evidence | `../04_Career_Goals_and_Strategy/Role_Targets/role-target-portfolio-transformation-governance.md` |
| `track-5` | Technology generalist focused on agentic engineering; hands-on software design, implementation, testing, and delivery | `../04_Career_Goals_and_Strategy/Role_Targets/role-target-hands-on-engineering.md` |
| `track-9` | Opportunistic Employment: no fixed headline; one functional frame chosen per posting from canonical evidence at actual scope | `../04_Career_Goals_and_Strategy/Role_Targets/role-target-opportunistic.md` |

### Choose the Track Before Tailoring

1. Complete opportunity analysis. `/build-resume` and `/build-application` use its `## Track` section, falling back to opportunity frontmatter when the analysis track is absent or `MISSING`; correct unsupported values before generation.
2. Require one valid employment track and its role target before generating or updating targeted materials. Resolve missing tracks or unresolved conflicts through `/analyze-opportunity`; an explicit, reasoned analysis reassignment can supersede the intake track.
3. Load the role target's Positioning Statement and Resume Tailoring Focus. Use its mandate and evidence boundaries to select the headline, summary, skills, and achievements.
4. Use a matching track baseline when available. Otherwise build from canonical evidence and the role target; a baseline is optional.
5. Save tailored materials in `../06_Job_Opportunities/<company>_<role>_<date>/`. Record track provenance in internal application notes/record and runtime context, not in submitted resume or cover-letter text.
6. Generate DOCX/PDF using the shared formatting templates after content is finalized. Formatting alone does not choose or change the track.

### Master and Track Baselines

The master is a comprehensive, track-neutral content pool. Its current summary is presentation wording and must not become the default for every track. Career facts remain authoritative in `02_`–`05_`.

Reusable track baselines may be stored here as `resume-product-engineering-leadership.md`, `resume-msp-advisory-account-growth.md`, `resume-portfolio-transformation-governance.md`, and `resume-agentic-engineering.md`, named from the track label in `../04_Career_Goals_and_Strategy/career-tracks.md` (Opportunistic Employment has no fixed baseline; it is built per posting); these are naming conventions, not a claim that the files already exist. Track baselines change selection, emphasis, and language without changing employers, titles, dates, metrics, or ownership.

For each baseline actually created, record the track, role-target path, baseline path, source references, last evidence review, and positioning review in this README. Baselines are optional and must be checked against current canonical evidence and the current role target before reuse. Rework any mismatched baseline rather than retaining another track's headline or summary.

| Track | Baseline path | Role target | Last evidence / positioning review |
|-------|---------------|-------------|------------------------------------|

Baselines are drafts until the owner completes the positioning review recorded above. Shared DOCX templates remain common to all tracks.
