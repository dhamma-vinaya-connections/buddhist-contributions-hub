# Implementation Checklist

## Phase 1: Foundation (Current Status)
- [x] Initialize Git Repository.
- [x] Define Directory Architecture.
- [x] Create `.gitignore`.
- [x] Create `.clinerules` & `specs.md`.
- [ ] Define `requirements.txt`.

## Phase 2: The Scripts (Development)

- [x] Citation `scripts/citation_scanner.py` (The shared brain that finds citations).
- [ ] PDF converter `scripts/pdf_converter.py` (The machine that processes books).
- [x] EPUB converter `scripts/epub_converter.py` (The machine that processes books).
- [x] **Gatekeeper:** Implement `scripts/gatekeeper.py` (Validation).
	- [x] Implement with split-citation validation.
- [x] **Librarian:** Implement `scripts/librarian.py` (Main Loop).
	- [x] Implement routing logic (Dhamma vs Vinaya folders).
- [x] **Citation Engine:** Create `scripts/citation_sorter.py` module. - *Logic:* Distinguishes `Vin/Pvr` from `DN/MN`.
- [x] **PDF Engine:** Implement `scripts/pdf_converter.py` using `pymupdf4llm`.
- [x] **EPUB Engine:** Implement `scripts/epub_converter.py`.
- [x] **MD Handler:** Implement `scripts/md_copier.py`.

## Phase 3: Automation (GitHub Actions)
- [x] Create `.github/workflows/validate_pr.yml` (Runs Gatekeeper).
- [x] Create `.github/workflows/process_library.yml` (Runs Librarian).
- [x] Create `.github/workflows/release.yml` (Zips & Publishes).

## Phase 4: Infrastructure
- [x] Resolve Git LFS installation (Deferred).

## Phase 5 Documentation
- [x] Add `CONTRIBUTING.md` guide for users.
- [x] Add `README.md` with download instructions.