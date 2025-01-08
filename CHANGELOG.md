# CHANGELOG

## 0.1.7

### Added
- Flag `--cloud` for selecting the provider (aws, gcp, azure, all)
- Tests for GCP

### Removed
- GCP & Azure options from the dropdown menu

### Changed
- `--deploy` doesn’t require the `--cloud` flag anymore
- Dropdown functionality now depends on the `--cloud` flag (including `all`)