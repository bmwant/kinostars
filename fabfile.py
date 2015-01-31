from fabric.api import *

env.user = 'bmwant'
env.hosts = ['77.47.205.142']
env.password = 'try-to-forget'
env.shell = "bash -c"

def uptime():
	run('uptime')

def host_type():
	run('uname -s')
	
def deploy():
	put('hello.py', '/data/projects/test1')
	put('requirements.txt', '/data/projects/test1')
	put('config.py', '/data/projects/test1')