from boto3 import client

REGION_NAME = 'us-east-1'

# SAMPLE_INSTANCE_DATA = {
#     'Instances': [
#         {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-53d13a927070628de', 'Type': 'a1.2xlarge',
#          'ImageId': 'ami-03cf127a',
#          'LaunchTime': '2020-10-13T19:27:52.000Z', 'State': 'running',
#          'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
#          'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
#          'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
#          'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
#          'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
#          'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
#          'Tags': [{'Key': 'Name', 'Value': 'Jenkins Master'}]
#          },
#         {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-23a13a927070342ee', 'Type': 't2.medium',
#          'ImageId': 'ami-03cf127a',
#          'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Stopped',
#          'StateReason': 'Client.UserInitiatedShutdown: User initiated shutdown', 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
#          'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
#          'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
#          'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
#          'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
#          'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
#          'Tags': [{'Key': 'Name', 'Value': 'Consul Node'}]
#          },
#         {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-77z13a9270708asd', 'Type': 't2.xlarge',
#          'ImageId': 'ami-03cf127a',
#          'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Running',
#          'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
#          'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
#          'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
#          'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
#          'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
#          'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
#          'Tags': [{'Key': 'Name', 'Value': 'Grafana'}]
#          }
#     ]
# }


def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']
    
def create_instance_data_stracture(instance):
    my_instance = {}
    my_instance['Cloud'] = 'aws'
    my_instance['Region'] = 'us-east-1'
    my_instance['Id'] = str(instance['InstanceId'])
    my_instance['Type'] = str(instance['InstanceType'])
    my_instance['ImageId'] = str(instance['ImageId'])
    my_instance['LaunchTime'] = instance['LaunchTime']
    my_instance['State'] = str(instance['State']['Name'])
    my_instance['StateReason'] = get_state_reason(instance)
    my_instance['SubnetId'] = str(instance['NetworkInterfaces'][0]['SubnetId'])
    my_instance['VpcId'] = str(instance['NetworkInterfaces'][0]['VpcId'])
    my_instance['MacAddress'] = str(instance['NetworkInterfaces'][0]['MacAddress'])
    my_instance['NetworkInterfaceId'] = str(instance['NetworkInterfaces'][0]['NetworkInterfaceId'])
    my_instance['PrivateDnsName'] = instance['PrivateDnsName']
    my_instance['PrivateIpAddress'] = instance['PrivateIpAddress']
    my_instance['PublicDnsName'] = instance['PublicDnsName']
    my_instance['PublicIpAddress'] = instance.get("PublicIpAddress", None)
    my_instance['RootDeviceName'] = instance['RootDeviceName']
    my_instance['RootDeviceType'] = instance['RootDeviceType']
    my_instance['SecurityGroups'] = instance['SecurityGroups']
    my_instance['Tags'] = instance['Tags']

    return my_instance



class InstanceData:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

   
    def get_instances(self):
        # TODO:
        # The below JSON should be populated using real instance data (instead of the SAMPLE_INSTANCE_DATA)
        # The format of SAMPLE_INSTANCE_DATA (field names and JSON structure)
        # must be kept in order to be properly displayed in the application UI
        #
        # Notice that when the machine is running the "StateReason" filed should be set to None
        # and will not be shown in the UI
        #
        # NOTE: the `self.ec2_client` is an object that is returned from doing `boto3.client('ec2')` as you can
        # probably find in many examples on the web
        # Example of using the describe_instances method:
        # my_instances = self.ec2_client.describe_instances()
        # To read more on how to use Boto for EC2 look for the original Boto documentation
        my_instances = self.ec2_client.describe_instances()
        REAL_INSTANCE_DATA = {'Instances':[]}
        for reservations in my_instances['Reservations']:
            for instance in reservations['Instances']:
                add_instance = create_instance_data_stracture(instance)
                REAL_INSTANCE_DATA['Instances'].append(add_instance)
        
        print (REAL_INSTANCE_DATA)
        return REAL_INSTANCE_DATA

### for testing locally
# ec2 = client('ec2')
# test = InstanceData(ec2)
# test.get_instances()

