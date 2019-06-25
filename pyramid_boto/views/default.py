from pyramid.view import view_config


def is_active(state_code):
    return state_code != 16


@view_config(route_name='home', renderer='../templates/ec2_home.jinja2', request_method='GET')
def get_home_view(request):
    """Fetch instances and show it at UI"""
    return {}

