README

This document explains how to use Commitizen to create conventional commits before pushing to the Git repository. It ensures consistent commit messages and enables automated semantic versioning.

⸻

1. Prerequisites
	•	Python (3.12.x recommended)
	•	Git
	•	Commitizen installed:

`pip install commitizen`

* You can skip this step, since poetry will install commitzen for you


2. Initialize Commitizen

In your project root (where pyproject.toml or setup.cfg lives), run:

`cz init`

When prompted, select the cz_conventional_commits adapter. This creates or updates your configuration so that Commitizen knows how to lint and generate commits.

3. Creating Commits

Instead of using git commit -m "...", use:

```bash
git add <files>
cz commit
```

Commitizen will prompt you for:
	•	Type: (feat, fix, chore, docs, ci, etc.)
	•	Scope (optional): a short label like api, auth, ci
	•	Short Description (required)
	•	Long Description (optional)
	•	Breaking Changes (optional)

Example flow:
```bash
$ cz commit
? Select the type of change you are committing: feat
? Denote the scope of this change (optional): api
? Write a short, imperative description of the change: add user endpoint
? Provide a longer description of the change (press enter to skip):
? Are there any breaking changes? No
```

This will generate a commit like:

`feat(api): add user endpoint`

4. Pushing to the Repository

Once your commit is created:

`git push origin <your-branch>`

Ensure that your branch’s history only contains conventional commits; this allows downstream tools (e.g., python-semantic-release) to automatically bump versions.

⸻

With conventional commits in place, tools like python-semantic-release can automatically parse your history, bump versions, generate changelogs, and publish releases without manual intervention.
