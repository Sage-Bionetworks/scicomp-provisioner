# Overview
Auto provision resources into AWS org-sagebase-scicomp account.

## Workflow
The workflow to provision AWS resources is done using pull requests.
Request using PRs provide history, gating, reviewing and an approval
process.

## Contributions
Contributions are welcome.

Requirements:
* Install [pre-commit](https://pre-commit.com/#install) app
* Clone this repo
* Run `pre-commit install` to install the git hook.

## Testing
As a pre-deployment step we syntatically validate our sceptre and
cloudformation yaml files with [pre-commit](https://pre-commit.com).

Please install pre-commit, once installed the file validations will
automatically run on every commit.  Alternatively you can manually
execute the validations by running `pre-commit run --all-files`.

## Provision resources
Instructions and workflow to auto provision and de-provision resources are
in [Example PRs](https://github.com/Sage-Bionetworks/scicomp-provisioner/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+%22Example+PR%22)

### Stack & config file names
The value of a stack's `stack_name` parameter must match the config's file
name.  Stack names can contain only alphanumeric characters (case-sensitive)
and hyphens. They must start with an alphabetic character and can't be longer
than 128 characters.

## Deployments
We use [sceptre](https://sceptre.github.io/) and [cloudformation](https://aws.amazon.com/cloudformation/)
to deploy resources onto an AWS account.

## Continuous Integration
We have configured [Travis](https://travis-ci.org) to deploy CF template updates.

## Issues
* https://sagebionetworks.jira.com/projects/IT

## Builds
* https://travis-ci.org/Sage-Bionetworks/scicomp-provisioner

## Secrets
* We use the [AWS SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
to store secrets for this project.  Sceptre retrieves the secrets using
a [sceptre ssm resolver](https://github.com/cloudreach/sceptre/tree/v1/contrib/ssm-resolver)
and passes them to the cloudformation stack on deployment.
