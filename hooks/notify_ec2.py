import logging

from sceptre.hooks import Hook
from botocore.exceptions import ClientError

"""
The purpose of this hook is to run additional setup after creating
an EC2 instance.

Does the following after creation of the bucket:
* Send an email to the EC2 owner with the EC2 info.

Example:

    template_path: templates/managed-ec2.yaml
    stack_name: my-fun-ec2
    parameters:
      # The Sage deparment for this resource
      Department: "Platform"
      # The Sage project this resource will be used for
      Project: "Infrastructure"
      # EC2 owner's email address
      OwnerEmail: "jsmith@sagebase.org"
      # EC2 instance type to deploy
      InstanceType: "t2.nano"
    hooks:
      after_create:
        - !notify_ec2

"""
class NotifyEC2(Hook):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, *args, **kwargs):
        super(NotifyEC2, self).__init__(*args, **kwargs)

    def run(self):
        """
        run is the method called by Sceptre. It should carry out the work
        intended by this hook.
        """
        region = self.environment_config['region']
        stack_name = self.stack_config['stack_name']

        # Defaults parameters allows user to optionally specify them in scepter
        # Therefore we need to get parameter values from cloudformation
        response = self.request_cf_decribe_stacks(stack_name)
        stack_parameters = response['Stacks'][0]['Parameters']
        stack_outputs = response['Stacks'][0]['Outputs']
        owner_email = self.get_parameter_value(stack_parameters, 'OwnerEmail')

        # EC2 info is auto assigned and only available in CF outputs
        ec2_info ={}
        ec2_info['id'] = self.get_output_value(stack_outputs,
                                               region + '-' + stack_name + '-' + 'Ec2InstanceId')
        ec2_info['private_ip'] = self.get_output_value(stack_outputs,
                                           region + '-' + stack_name + '-' + 'Ec2InstancePrivateIp')

        # EC2 in private subnet will not have a pubilc IP
        try:
            ec2_info['public_ip'] = self.get_output_value(stack_outputs,
                                               region + '-' + stack_name + '-' + 'Ec2InstancePublicIp')
        except UndefinedExportException as e:
            pass

        self.logger.info("EC2 instance id: " +  ec2_info['id'])

        self.email_owner(owner_email, ec2_info)

    def request_cf_decribe_stacks(self, stack_name):
        client = self.connection_manager.boto_session.client('cloudformation')

        try:
            response = client.describe_stacks(StackName=stack_name)
            return response
        except ClientError as e:
            self.logger.error(e.response['Error']['Message'])

    def get_parameter_value(self, parameters, key):
        for parameter in parameters:
            if parameter['ParameterKey'] == key:
                return parameter['ParameterValue']

        raise UndefinedParameterException("Parameter not found: " + key)

    def get_output_value(self, exports, name):
        for export in exports:
            if export['ExportName'] == name:
                return export['OutputValue']

        raise UndefinedExportException("Export not found: " + name)

    def email_owner(self, owner_email, ec2_info):
        client = self.connection_manager.boto_session.client('ses')

        # This address must be verified with Amazon SES.
        SENDER = "AWS Scicomp <aws.scicomp@sagebase.org>"

        # if SES is still in the sandbox, this address must be verified.
        RECIPIENT = owner_email

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        # CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        # AWS_REGION = "us-west-2"

        # The subject line for the email.
        SUBJECT = "Scicomp Automated Provisioning"

        # The email body for recipients with non-HTML email clients.
        info = ''
        for k, v in ec2_info.items():
            info = info + k + ": " + v + "<br />"

        BODY_TEXT = ("An EC2 instance has been provisioned on your behalf. "
                     "<br />" + info +
                     "<br />To connect to this resource, login to the Sage VPN, open a terminal, then type " +
                     "ssh YOUR_JUMPCLOUD_USERNAME@IP_ADDRESS (i.e. ssh jsmith@" + ec2_info["private_ip"] + ")")

        # The HTML body of the email.
        BODY_HTML1 = """<html>
        <head></head>
        <body>
          <p>"""
        BODY_HTML2 = """</p>
        </body>
        </html>
        """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML1 + BODY_TEXT + BODY_HTML2,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        except ClientError as e:
            self.logger.error(e.response['Error']['Message'])
        else:
            self.logger.info("Email sent to " + RECIPIENT)
            self.logger.info("Message ID: " + response['MessageId'])


class UndefinedExportException(Exception):
    pass


class UndefinedParameterException(Exception):
    pass
