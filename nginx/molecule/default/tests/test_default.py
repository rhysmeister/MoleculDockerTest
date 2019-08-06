import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_default_nginx_file(host):
    f = host.file('/usr/share/nginx/html/index.html')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert 'Hello from' in f.content_string


def test_nginx_is_installed(host):
    nginx = host.package("nginx")
    assert nginx.is_installed


def test_nginx_running_and_enabled(host):
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_listening(host):
    h = host.socket("tcp://0.0.0.0:80")
    assert h.is_listening

def test_nginx_default_page(host):
    cmd = host.run('curl -s http://localhost | grep "Hello from"')
    assert cmd.rc == 0
