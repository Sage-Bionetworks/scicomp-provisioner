# Overview
Auto provision resources on AWS scicomp account. Cloudformation templates
in this repo build on top of CF templates in Sage-Bionetworks/scicomp-infra
repo.

## Instructions to create or update CF stacks


```
# Update CF stacks with sceptre:
# sceptre launch-stack prod <stack_name>
```

The above should setup resources for the AWS account.  Once the infrastructure
for the account has been setup you can access and view the account using the
[AWS console](https://AWS-account-ID-or-alias.signin.aws.amazon.com/console).

*Note - This project depends on CF templates from other accounts.*

## Scicomp

### Provision EC2 instances

```
aws --profile scicomp --region us-east-1 \
cloudformation create-stack --stack-name khai-instance1 \
--capabilities CAPABILITY_NAMED_IAM \
--template-url https://s3.amazonaws.com/bootstrap-awss3cloudformationbucket-114n2ojlbvj21/scicomp-infra/master/accounts.yaml \
--parameters \
ParameterKey=InstanceType,ParameterValue="t2.nano" \
ParameterKey=JcServiceApiKey,ParameterValue="abcd111122223333aaaabbbbccccddddeeeeffff" \
ParameterKey=JcSystemsGroupId,ParameterValue="1eabd8df45bf6d7d2a32d4ff" \
ParameterKey=JcConnectKey,ParameterValue="0123456789abcdef0123456789abcdef01234567" \
ParameterKey=KeyName,ParameterValue="scicomp" \
ParameterKey=VpcName,ParameterValue="computevpc" \
ParameterKey=VpcSubnet,ParameterValue="PrivateSubnet"
```
*Note* - check default parameters in the template

The above should create an EC2 instance and join the instance to a Sage Jumpcloud "system group"
identified by $JcSystemsGroupId.  Jumpcloud "User groups" that have access to $JcSystemsGroupId
will have access to this instance.

### Jumpcloud System Groups

Find [system groups](https://docs.jumpcloud.com/2.0/system-groups/list-all-systems-groups) by using the Jumpcloud API
```
curl -X GET https://console.jumpcloud.com/api/v2/systemgroups \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: abcd111122223333aaaabbbbccccddddeeeeffff'
```

### Jumpcloud Systems

Find [systems](https://docs.jumpcloud.com/1.0/systems/list-all-systems) by using the Jumpcloud API
```
curl -X GET https://console.jumpcloud.com/api/systems \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: abcd111122223333aaaabbbbccccddddeeeeffff'
```

### Workflow

This is how EC2 provisioning works for this account.

1. Create the EC2 instance with the above command.
2. Locate the IP address of the newly provisioned EC2 instance.
3. Login to the Sage VPN. (only required if the instance is in a private subnet)
4. ssh to the ip address with a jumpcloud user account and ssh key (i.e. ssh jsmith@10.5.67.102)


### Delete EC2 instances

Steps required to delete an instance.

1. Delete the stack from AWS.
```
aws --profile scicomp --region us-east-1 \
cloudformation delete-stack --stack-name khai-instance1
```
The above should delete the EC2 instance that was provisioned in the Provision EC2 instance step

2. Delete EC2 from Jumpcloud
```
curl -X DELETE https://console.jumpcloud.com/api/systems/5aabfa45f626352a235780a8 \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: abcd111122223333aaaabbbbccccddddeeeeffff'
```

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
