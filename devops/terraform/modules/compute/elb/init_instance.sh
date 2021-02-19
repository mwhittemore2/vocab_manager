#!/bin/sh

#Install updates
yum update -y

#Install Ansible
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py" python /tmp/get-pip.py
pip install pip --upgrade
rm -fr /tmp/get-pip.py
pip install boto
pip install --upgrade ansible

#Install Git
yum install git -y

#Clone project
mkdir tmp
cd tmp
git clone https://github.com/mwhittemore2/vocab_manager.git

#Run Ansible playbooks
cd vocab_manager/devops/ansible
ansible_playbook setup_instance.yaml