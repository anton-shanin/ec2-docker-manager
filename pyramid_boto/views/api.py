import botocore
from pyramid.view import view_config
from pyramid_boto.ec2_manager import EC2Client


def is_active(state_code):
    return state_code != 16


@view_config(route_name='api_ec2', renderer='json', request_method='GET')
def get_api_ec2_view(request):
    """Fetch instances and show it at UI"""
    instances = []
    try:
        client = EC2Client()
        client.fetch()
    except botocore.exceptions.ClientError:
        request.response.status = 400
        return {'error': 'Wrong AWS credentials'}
    except botocore.exceptions.EndpointConnectionError:
        request.response.status = 400
        return {'error': 'Could not connect to the Internet'}

    instance_dict = client.get_instances()
    for instance in instance_dict:
        instances.append({
            'instance_id': instance,
            'name': instance_dict[instance]['InstanceType'],
            'zone': instance_dict[instance]['Placement']['AvailabilityZone'],
            'state': instance_dict[instance]['State']['Name'],
            'state_code': instance_dict[instance]['State']['Code'],
            'is_active': is_active(instance_dict[instance]['State']['Code'])
        })
    return {'instances': instances}


@view_config(route_name='api_ec2', renderer='json', request_method='POST')
def post_api_ec2_view(request):
    """Receive start/stop signal and apply it"""
    data = request.json_body
    try:
        selected = EC2Client().get_specified_instance(data.get('id'), data.get('zone'))
    except botocore.exceptions.ClientError:
        request.response.status = 400
        return {'error': 'Wrong AWS credentials'}

    if is_active(data.get('state')):
        selected.start()
    else:
        selected.stop()
    return {'ID': data.get('id'), 'REGION': data.get('region')}
