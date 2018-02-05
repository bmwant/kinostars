deploy:
	@cd deployment && \
			ansible-playbook deploy.yml -i hosts.ini -l digital_ocean -vv -u centos --ask-pass
