import multiprocessing

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
        manager = multiprocessing.Manager()
        self.ec2client = boto3.client('ec2')
        self.regions = self.ec2client.describe_regions()['Regions']
        self.instances = manager.dict()
        self.processes = []

    def get_client(self):
        """Return ec2 client instance"""
        return self.ec2client

    def get_specified_instance(self, instance_id, region: str):
        """Get specified instance by id"""
        if not region[-1].isdigit():
            region = region[:-1]
        return boto3.resource('ec2', region_name=region).Instance(instance_id)

    def instances_in_region(self, region):
        """Append to instance dictionary all instances of specified region"""
        response = boto3.client('ec2', region_name=region).describe_instances()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                self.instances[instance["InstanceId"]] = instance

    def fetch(self):
        """Fetch actual data of instances"""
        for region in self.regions:
            t = multiprocessing.Process(target=self.instances_in_region, args=(region['RegionName'],))
            self.processes.append(t)
            t.start()

        for one_process in self.processes:
            one_process.join()

    def get_instances(self):
        """Return dictionary with data of active ec2 instances
        """

        return self.instances


if __name__ == '__main__':
    client = EC2Client()
    client.fetch()
    print(client.get_instances())
