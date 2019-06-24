from pyramid.view import view_config
from pyramid_boto.ec2_manager import EC2Client


def is_active(state_code):
    return state_code != 16


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2', request_method='GET')
def get_home_view(request):
    """Fetch instances and show it at UI"""
    instances = []
    client = EC2Client()
    client.fetch()
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


@view_config(request_method='POST', renderer="json", route_name="home")
def post_home_view(request):
    """Receive start/stop signal and apply it"""
    data = request.json_body
    selected = EC2Client().get_specified_instance(data.get('id'), data.get('zone'))
    print(selected)
    if is_active(data.get('state')):
        selected.start()
        print('start')
    else:
        selected.stop()
        print('stop')
    return {'ID': data.get('id'), 'REGION': data.get('region')}
