# CHANGELOG

## 0.1.15

### Changed/fixed
- Fixed aws query bug
- Fixed deployment wihtout .env file
- Fixed gcp deployment, and querying

## 0.1.12

### Changed/fixed
- Fixed active endpoint fetching making it conditional based on cloud flag

## 0.1.10

### Added
- Flag `--cloud` for selecting the provider (aws, gcp, azure, all)
- Tests for GCP
- Delete, query and list view are conditional upon the `--cloud` flag

### Removed
- GCP & Azure options from the dropdown menu (WIP)

### Changed/fixed
- `--deploy` doesn’t require the `--cloud` flag anymore
- Dropdown functionality now depends on the `--cloud` flag (including `all`)
- Query for AWS config path issue
