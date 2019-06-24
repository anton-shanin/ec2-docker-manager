import boto3


class Singleton(type):
    """Implements Singleton type"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EC2Client(metaclass=Singleton):
    """Client for ec2 instances using boto3"""

    def __init__(self):
        """Initialise instances of client and resource"""
        self.ec2client = boto3.client('ec2')

    def get_client(self):
        """Return ec2 client instance"""
        return self.ec2client

    def get_specified_instance(self, instance_id, region:str):
        """Get specified instance by id"""
        if not region[-1].isdigit():
            region = region[:-1]
        return boto3.resource('ec2', region_name=region).Instance(instance_id)

    def get_instances(self):
        """Collect ec2 instances among regions and generates dictionary of it
            Dictionary scheme:   instance_id:instance
        """
        all_instances = {}
        for region in self.ec2client.describe_regions()['Regions']:
            response = boto3.client('ec2', region_name=region['RegionName']).describe_instances()

            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    all_instances[instance["InstanceId"]] = instance

        return all_instances


if __name__ == '__main__':
    client = EC2Client()
    print(client.get_instances())
