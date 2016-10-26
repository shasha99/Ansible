These modules can be directly plugged-in with Ansible by copying them to :

/your_ansible_installation_directory/ansible/modules

Following are the work these modules are doing:

# vsphere_create_folder.py

This module is creating the folder on vCenter server and useful in case when you want to place the vm you are trying to deploy into some specified folder. So you paas the folder to this module through Ansible.


# vspgere_guest_copy_execute.py
This can be helpful when you do not have direct communication with your Vm and you are using it through vCenter instead.

