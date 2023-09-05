# Simple dbt Runners

dbt Cloud: who needs it? With this repo, not you!

This repo gives you the ability to run dbt in production using GitHub Actions. There are several basic GH Action workflows you can take a modify for your needs: 

 - run dbt commands on a [schedule](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_dbt_on_cron.yml)
 - run dbt after merging in a PR to the main branch (we recommend only choosing one of these at a time)
   - [full run](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_dbt_on_merge.yml)
   - [state-aware run](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_incremental_dbt_on_merge.yml) (only modified models)
 - dbt CI runs on PR commits to make sure your changes will work

The state-aware workflow requires an S3 bucket for persisting the `manifest.json` file. We also take advantage of the S3 bucket to host your project's documentation website.

### S3 bucket notes

To help you get set up we've put together an AWS CloudFormation Template [here in the repo](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/aws_resources/bucket_and_s3_policy.yml). 
 1. Log in to the AWS Console and open [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/)
 2. Click "Create Stack"
 3. Under "Specify Template", choose "Upload a template file" and upload our template from the repo
 4. Click "next"
 5. Add tags if you want, click "next"
 6. Review the information and click "Submit"

This will create an S3 bucket you can use for holding any DAG info and hosting your dbt project's documentation website. **WARNING:** our template will make the bucket publicly accessible by default, please edit if you don't want a publicly hosted bucket and website.

## How To Set Up Your dbt Project

 1. Fork this repo and copy your whole dbt project into the `project_goes_here` folder.
 2. Update your repository settings to allow GitHub Actions to create PRs. This setting can be found in a repository's settings under Actions > General > Workflow permissions. [This is what it should look like.](https://user-images.githubusercontent.com/21294829/263915123-512bf335-6796-4ae3-a7dc-ad1cf6c4035f.png)
 3. Go to the Actions tab and run the `Project Setup` workflow, making sure to select the type of database you want to set up
    - This opens a PR with our suggested changes to your `profiles.yml` and `requirements.txt` files.
    - We assume if you're migrating to self-hosting you need to add a prod target to your `profiles.yml` file, so this action will do that for you and also add the db driver you indicate.
    - FYI we also assume you have a `profiles.yml` file.
 4. Add some environment variables to your GitHub Actions secrets in the Settings tab. You can see which vars are needed based on anything appended with `${{ secrets.` in the open PR.
    - Additional environment variables you'll need if you want to use the [state-aware dbt build](https://github.com/C00ldudeNoonan/simple-dbt-runner/blob/main/.github/workflows/run_incremental_dbt_on_merge.yml):
      - AWS_S3_BUCKET
      - AWS_ACCESS_KEY
      - AWS_SECRET_KEY
 5. Run the `Manual dbt Run` to test that you're good to go.
 6. Edit the Actions you want to keep and delete the ones you don't

# dbt Documentation

dbt documentation is pushed to a static website hosted on an s3 bucket. Example here: http://dbt-s3bucket-eywrs70vvmxj.s3-website-us-east-1.amazonaws.com/#!/overview

For 

That's it!
