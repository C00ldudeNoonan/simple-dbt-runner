# Simple dbt Runners

dbt Cloud: who needs it? With this repo, not you!

This repo gives you the ability to run dbt in production using GitHub Actions. There are several basic GH Action workflows you can take a modify for your needs: 

 - run dbt commands on a schedule
 - run dbt after merging in a PR to the main branch
 - dbt CI runs on PR commits to make sure your changes will work

## How To Set Up Your Project

 1. Fork this repo and copy your whole dbt project into the `project_goes_here` folder.
 2. Update your repository settings to allow GitHub Actions to create PRs.
 3. Go to the Actions tab and run the `Project Setup` workflow, making sure to select the type of database you want to set up
    - We assume if you're migrating to self-hosting you need to add a prod target to your `profiles.yml` file. Feel free to skip this step if you already have a production target set in that file.
    - We also assume you have a `profiles.yml` file
    - This opens a PR with our suggested changes to your `profiles.yml` file
 4. Add some environment variables to your GitHub Actions Secrets in the Settings tab. You can see which vars are needed based on the open PR.
 5. Run the `Manual dbt Run` to test that you're good to go
 6. Edit the Actions you want to keep and delete the ones you don't

That's it!
