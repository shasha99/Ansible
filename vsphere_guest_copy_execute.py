#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
author: Shashank Awasthi
module: vsphere_guest_copy_execute
short description: Copy and execute the scripts on the guest
description:
  - This module copies one or multiple files from local machine to the guest
  - This module also excutes the files it copied on the vsphere guest
  - If files are already present on the guest, they will be overwritten
  - This module requires login to the guest
  - This module requires python pysphere module
options:
  host:
    description:
      - The vSphere server from the cluster the virtual server is located on.
    required: true
  login:
    description:
      - The login name to authenticate on the vSphere cluster.
    required: true
  password:
    description:
      - The password to authenticate on the vSphere cluster.
    required: true
  guest:
    description:
      - The virtual server to gather facts for on the vSphere cluster.
    required: true
  guestlogin:
    description:
      - The login name for the guest OS.
    required: true
  guestpassword:
    description:
      - The password for the guest OS.
    required: true
  srcdir:
    description:
     - local directory containing files to be copied
    required: true
  destdir:
    description:
      - directory on the remote host where the files are to be copied.
    required: true
  files:
    description:
      -multiple comma seperated file names.
    required: true
examples:
  - description: copy test.sh from /home/src to /etc/destdir
    code:
      - local_action: vsphete_guest_copy_execute host=$esxserver login=$esxlogin                                                                                                                                                              password=$esxpassword guest=$guestname guestlogin=root guestpassword=secret src                                                                                                                                                             dir=/home/src destdir=/etc/dest files="test.sh"

notes:
  - This module ought to be run from a system that can access vSphere directly.
  - You will not recieve output of the command executed, the command is forked i                                                                                                                                                             n the background and only
'''

import sys
try:
        import pysphere
        from pysphere import VIServer
except ImportError:
        print "failed=True msg='pysphere python module unavailable'"
        sys.exit(1)

def main():
        module=AnsibleModule(
                argument_spec = dict(
                        host = dict(required = True),
                        login = dict(required=True),
                        password = dict(required=True),
                        guestlogin = dict(required=True),
                        guestpassword = dict(required=True),
                        guest = dict(required=True),
                        srcdir = dict(required=True),
                        destdir = dict(required=True),
                        files = dict(requred=True)
                )
        )

        host = module.params.get('host')
        login = module.params.get('login')
        password = module.params.get('password')
        guest = module.params.get('guest')
        guestlogin = module.params.get('guestlogin')
        guestpassword = module.params.get('guestpassword')
        srcdir = module.params.get('srcdir')
        destdir=module.params.get('destdir')
        files =  module.params.get('files')



        server=VIServer()
        try:
                server.connect(host,login,password)
        except Exception, e:
                module.fail_json(msg='Failed to connect to %s: %s'%(host,e))

        try:
                vm_target=server.get_vm_by_name(guest)
        except pysphere.resources.vi_exception.VIException, e:
                module.fail_json(msg=e.message)

        try:
                if vm_target.get_status() != 'POWERED ON':
                        task = vm_target.power_on()
                        status = task.wait_for_state(['running','error'],timeout                                                                                                                                                              = 70)
                        if status == 'error':
                                module.fail_json(msg = 'Failed to start the VM %                                                                                                                                                             s' % guest)
        except Exception, e:
                module.fail_json(msg="Error while powering on the machine.Timeou                                                                                                                                                             t occured: "+e.message)

        vm_target.wait_for_tools(timeout=90)

        files=files.split(" ")

        try:
                vm_target.login_in_guest(guestlogin,guestpassword)

                for f in files:
                        vm_target.send_file(srcdir+"/"+f,destdir+"/"+f,True)
                        #vm_target.start_process("/bin/chmod",["+x",destdir+"/"+                                                                                                                                                             f],"","")
                        #pid=vm_target.start_process("/bin/bash",[destdir+"/"+f]                                                                                                                                                             ,"","")

        except Exception, e:
                module.fail_json(msg=e.message)

        server.disconnect()
        module.exit_json(changed=True, pid=pid)

#<<INCLUDE_ANSIBLE_MODULE_COMMON>>
main()
