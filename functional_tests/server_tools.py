from fabric.api import run
from fabric.context_managers import settings

def _get_manage_py_file(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'

def reset_database(host):
    manage_py = _get_manage_py_file(host)
    with settings(host_string=f'osboxes@{host}'):
        run(f'{manage_py} flush --noinput')

def create_session_on_server(host, email):
    manage_py = _get_manage_py_file(host)
    with settings(host_string=f'osboxes@{host}'):
        session_key = run(f'{manage_py} create_session {email}')
        return session_key.strip()