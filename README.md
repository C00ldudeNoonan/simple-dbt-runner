# Simple dbt Runners

dbt Cloud: who needs it? With this repo, not you!

This repo gives you the ability to run dbt in production using GitHub Actions. There are several basic GH Action workflows you can take and modify for your needs: 

 - run dbt commands on a [schedule](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_dbt_on_cron.yml)
 - run dbt after merging in a PR to the main branch (we recommend only choosing one of these at a time)
   - [full run](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_dbt_on_merge.yml)
   - [state-aware run](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_incremental_dbt_on_merge.yml) (only modified models)
 - dbt CI runs on PR commits to make sure your changes will work

The state-aware workflow will look for the `manifest.json` file in a branch called `gh-pages`. We also take advantage of that branch to host your project's documentation website.

## How To Set Up Your dbt Project

 1. Fork this repo and copy your whole dbt project into the `project_goes_here` folder.
 2. Create a [Personal Access Token](https://github.com/settings/tokens?type=beta) with Workflows (Read/Write) permission and add it to the repository action secrets with key WORKFLOW_TOKEN
 3. Update your repository settings to allow GitHub Actions to create PRs. This setting can be found in a repository's settings under Actions > General > Workflow permissions. [This is what it should look like.](https://user-images.githubusercontent.com/21294829/263915123-512bf335-6796-4ae3-a7dc-ad1cf6c4035f.png)
 4. Go to the Actions tab and run the `Project Setup` workflow, making sure to select the type of database you want to set up
    - This opens a PR with our suggested changes to your `profiles.yml` and `requirements.txt` files.
    - We assume if you're migrating to self-hosting you need to add a prod target to your `profiles.yml` file, so this action will do that for you and also add the db driver you indicate.
    - FYI we also assume you have a `profiles.yml` file.
 5. Add some environment variables to your GitHub Actions secrets in the Settings tab. You can see which vars are needed based on anything appended with `${{ secrets.` in the open PR. You might need to slightly edit this PR based on your project setup.
 6. Run the `Manual dbt Run` to test that you're good to go.
 7. Edit the Actions you want to keep and delete the ones you don't

# dbt Documentation

dbt documentation is pushed to Github Pages. If you are using Github Enterprise, the pages are automatically secured behind Github SSO. Hosting your dbt docs is highly contextual based on your organization. There are proven patterns for shipping dbt docs to netlify, confluence and many other targets.

If using GH Pages, the only manual configuration required for hosting your dbt docs is to set it to run off the root directory of the `gh-pages` branch. You can configure this in your Github repo's Settings > Pages. Once you set that up it will looks like [this](https://c00ldudenoonan.github.io/simple-dbt-runner/#!/overview)

**WARNING**: if you do not have Gitub Enterprise and you set up the documentation hosting your page might be publicly accessible. Please review [their docs](https://pages.github.com/).

# Acknowledgements & Notes

Thank you to [dwreeves](https://github.com/dwreeves) for both highlighting an issue with initial deployment with regard to public s3 buckets as well as providing the [template for deploying to github pages](https://github.com/dwreeves/dbt_docs_ghpages_example).
