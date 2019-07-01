# Overview
Auto provision resources on AWS org-sagebase-scicomp account. 

## Workflow
The workflow to provision AWS resources is done using pull requests.
Request using PRs provide history, gating, reviewing and an approval
process.

## Provision resources
Instructions and workflow to auto provision and de-provision resources are
in [Example PRs](https://github.com/Sage-Bionetworks/scicomp-provisioner/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+%22Example+PR%22)

## Deployments
We use [sceptre](https://sceptre.github.io/) and [cloudformation](https://aws.amazon.com/cloudformation/)
to deploy resources onto an AWS account.

## Testing
As a pre-deployment step we syntatically validate our sceptre and cloudformation templates with
[yamllint](https://yamllint.readthedocs.io/en/stable/) and
[cfn-lint](https://github.com/aws-cloudformation/cfn-python-lint).
It is recommended that you do the same before creating a PR. 

## Continuous Integration
We have configured Travis to deploy CF template updates.

# Contributions

## Issues
* https://sagebionetworks.jira.com/projects/IT

## Builds
* https://travis-ci.org/Sage-Bionetworks/scicomp-provisioner

## Secrets
* We use the [AWS SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
to store secrets for this project.  Sceptre retrieves the secrets using
a [sceptre ssm resolver](https://github.com/cloudreach/sceptre/tree/v1/contrib/ssm-resolver)
and passes them to the cloudformation stack on deployment.
