pyAnsible
=========
[![PyPI Version](https://img.shields.io/pypi/v/pyansible.svg)](https://pypi.python.org/pypi/pyansible)

A python module that interfaces with Ansible Runner and Inventory. Provides an API interface
to directly invoke ansible module from python API.

--------

+ [Introduction] (https://github.com/bdastur/spam/blob/master/README.md#introduction)
+ [Installation] (https://github.com/bdastur/spam/blob/master/README.md#installation)
+ [Sample Usage] (https://github.com/bdastur/spam/blob/master/README.md#usage)


# Introduction<a name="introduction"></a>
[Ansible] (http://docs.ansible.com/ansible/index.html) is an IT automation tool. It is 
excellent for configuration management, orchestration and deployment automation. Ansible
is gaining popularity over other tools due to it's simplicity in usage and architecture.
If you are not familiar with Ansible, you can read the [Ansible documentation] (http://docs.ansible.com/ansible/index.html).
 
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

# Installation:<a name="installation"></a>

```
    pip install pyansible
```

# Sample Usage:<a name="usage"></a>
Here's a simple example of using pyAnsible library to execute operations on multiple remote hosts:

```
    import sys
    # 1. Imports
    import pyansible.ansirunner
    import pyansible.ansiInventory
    
    # 2. Using inventory.
    myhostgroup = "nova"
    inventory = pyansible.ansiInventory.AnsibleInventory("./ansible_invfile")
    if not inventory.get_hosts(myhostgroup)
        print "No host for group %s found " % myhostgroup
        sys.exit()
    hostlist = inventory.get_hosts(myhostgroup[0]['hostlist'])

    # 3. Using runner: Try a simple connectivity test.
    runner = pyansible.ansirunner.AnsibleRunner()
    result, _ = runner.ansible_perform_operation(
        host_list=hostlist,
        remote_user=myusername,
        remote_pass=mypass,
        module="ping")

    for host in result['dark'].keys():
        print "%s: %s" % (host, "failed")

    for host in result['contacted'].keys():
        print "%s: %s" % (host, "OK")                

    # 4. Using runner: Execute a command. (with sudo) if required.
 
    cmd = "grep rabbit_hosts /etc/nova/nova.conf" 
    result, _ = self.runner.ansible_perform_operation(
        host_list=hostlist,
        remote_user=username,
        remote_pass=password,
        sudo=self.sudo,
        sudo_user=self.sudo_user,
        sudo_pass=self.sudo_pass,
        module="shell",
        module_args=cmd)
  
    # Display result.
    for host in result['contacted'].keys():
        try:
            print result['contacted'][host]['stdout']
        except KeyError:
            print "No data for %s " % host

```

