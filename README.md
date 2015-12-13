pyAnsible
=========
A python module that interfaces with Ansible Runner and Inventory. Provides an API interface
to directly invoke ansible module from python API.

--------

+ [Introduction] (https://github.com/bdastur/spam/blob/master/README.md#introduction)

# Introduction<a name="introduction"></a>
If you are not familiar with Ansible, you can read the [Ansible documentation] (http://docs.ansible.com/ansible/index.html).
I will assume that you are familiar with Ansible, Ansible playbooks and ansible modules.
 
To give a very brief introduction: Ansible is an IT automation tool. It is excellent for 
configuration management, orchestration and deployment. Ansible in some ways surpasses other such
tools with it's simplicity in usage and installation. 

**So what is pyAnsible**
pyAnsible is a python module that interfaces with the Ansible.Runner and Ansible.Inventory modules
and provides a simple python API that you can invoke to directly access ansible modules.

*How is this useful?*: The most common way of using playbooks is great for most operations with ansible, 
but consider some use cases where you want to do discovery for instance, or take action based on the results
from output of the ansible modules run on remote hosts. 

Some usecases where I have used this module:
 - Given a list of hosts/hypervisors, get all the VMs running on them and check the linux distribution on them.
 - Developed a [remote execution CLI] (https://github.com/bdastur/relic) to execute commands on multiple hosts
   simultaneously.
 - Check disk utilization on hosts and send a warning email when disk usage exceeds a threshold. 

