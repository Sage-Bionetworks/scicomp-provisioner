# Overview
Auto provision resources on AWS scicomp account. Cloudformation templates
in this repo build on top of CF templates in Sage-Bionetworks/scicomp-infra
repo.

*Note - This project depends on CF templates from other accounts.*

## Workflow
The workflow to provision AWS resources is done using pull requests.
PRs provide history, gating, and a way to review and approve resource
requests.

### Provision EC2 instances
Instructions and workflow to auto provision and de-provision an EC2 is in
[Example PR: Auto provision an EC2 instance](https://github.com/Sage-Bionetworks/scicomp-provisioner/pull/3)

Merging the above should create an EC2 instance and join the instance to a Sage
Jumpcloud "system group" identified by $JcSystemsGroupId.  Jumpcloud
"User groups" that have access to $JcSystemsGroupId will have access to
the provisioned instance.

#### EC2 AMIs
We allow provisioning based on custom AMIs.  List of Sage IT managed AMIs:

Instance ID|Distribution|Volume|Comment|
-----------|------------|---------|-------|
ami-0ddee041772c2d9f8|AWS linux|8GB encrypted boot volume|Default AMI|


## Jumpcloud
We use a directory service [Jumpcloud](https://jumpcloud.com/)
to manage user access to EC2 instances.  


### Jumpcloud System Groups
Find [system groups](https://docs.jumpcloud.com/2.0/system-groups/list-all-systems-groups)
by using the Jumpcloud API:
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: abcd111122223333aaaabbbbccccddddeeeeffff'
```

### Jumpcloud Systems
Find [systems](https://docs.jumpcloud.com/1.0/systems/list-all-systems)
by using the Jumpcloud API:
```
curl -X GET https://console.jumpcloud.com/api/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: abcd111122223333aaaabbbbccccddddeeeeffff'
```

### Provision a Synapse external S3 bucket
Instructions and workflow to auto provision a
[Synapse external S3 bucket](http://docs.synapse.org/articles/custom_storage_location.html) 
can be found in 
[Example PR: Auto provision a synapse bucket](https://github.com/Sage-Bionetworks/scicomp-provisioner/pull/14)

Merging the above should create a synapse bucket with the configurations defined in
the documentation.

## Continuous Integration
We have configured Travis to deploy CF template updates.  Travis deploys using
[sceptre](https://sceptre.cloudreach.com/latest/about.html)

# Contributions

## Issues
* https://sagebionetworks.jira.com/projects/IT

## Builds
* https://travis-ci.org/Sage-Bionetworks/scicomp-infra

## Secrets
* We use the [AWS SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
to store secrets for this project.  Sceptre retrieves the secrets using
a [sceptre ssm resolver](https://github.com/cloudreach/sceptre/tree/v1/contrib/ssm-resolver)
and passes them to the cloudformation stack on deployment.
