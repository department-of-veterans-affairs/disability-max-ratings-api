# Configuration Guide

## Code Coverage Setup

This repository uses CodeClimate for code coverage and maintainability reporting.

### Required Setup Steps

#### In CodeClimate:
1. [Enable CodeClimate](https://github.com/apps/codeclimate) for the repository
2. [Enable "Pull Request Status Updates"](https://codeclimate.com/repos/676364ba629a59031e118d21/settings/github/edit) in Repo Settings > GitHub
3. [Enable Test Coverage and Maintainability checks](https://codeclimate.com/repos/676364ba629a59031e118d21/settings/test_reporter)

#### In GitHub:
1. Add `CC_TEST_REPORTER_ID` to [GitHub Actions secrets](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/settings/secrets/actions)
2. Ensure [Actions have "Read and write permissions"](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/settings/actions) under repository Settings > Actions > General
3. Enable [branch protection](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/settings/branches) for the following status checks:
   - `codeclimate/test-coverage`
   - `codeclimate/maintainability`

### Verification

After setup, CodeClimate will:
- Run on every PR and push to main
- Post coverage reports as PR comments
- Show coverage changes inline with code changes
- Block PR merging if coverage drops below configured thresholds (if set)

### Troubleshooting

If coverage reports are not appearing:
1. Verify the `CC_TEST_REPORTER_ID` is correctly set
2. Check GitHub Actions logs for any coverage upload errors
3. Ensure the repository is properly connected in CodeClimate's UI
