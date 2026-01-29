# Implementation Checklist

## Phase 1: Foundation (Current Status)
- [x] Initialize Git Repository.
- [x] Define Directory Architecture.
- [x] Create `.gitignore`.
- [x] Create `.clinerules` & `specs.md`.
- [ ] Define `requirements.txt`.

## Phase 2: The Scripts (Development)

- [ ] Citation `scripts/citation_scanner.py` (The shared brain that finds citations).
- [ ] PDF converter `scripts/pdf_converter.py` (The machine that processes books).
- [ ] EPUB converter `scripts/epub_converter.py` (The machine that processes books).
- [ ] **Gatekeeper:** Implement `scripts/gatekeeper.py` (Validation).
	- [ ] Implement with split-citation validation.
- [ ] **Librarian:** Implement `scripts/librarian.py` (Main Loop).
	- [ ] Implement routing logic (Dhamma vs Vinaya folders).
- [ ] **Citation Engine:** Create `scripts/citation_sorter.py` module. - *Logic:* Distinguishes `Vin/Pvr` from `DN/MN`.
- [ ] **PDF Engine:** Implement `scripts/pdf_converter.py` using `pymupdf4llm`.
- [ ] **EPUB Engine:** Implement `scripts/epub_converter.py`.
- [ ] **MD Handler:** Implement `scripts/md_copier.py`.

## Phase 3: Automation (GitHub Actions)
- [ ] Create `.github/workflows/validate_pr.yml` (Runs Gatekeeper).
- [ ] Create `.github/workflows/process_library.yml` (Runs Librarian).
- [ ] Create `.github/workflows/release.yml` (Zips & Publishes).

## Phase 4: Infrastructure
- [ ] Resolve Git LFS installation (Deferred).
- [ ] Add `CONTRIBUTING.md` guide for users.
- [ ] Add `README.md` with download instructions.