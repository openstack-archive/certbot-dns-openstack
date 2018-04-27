===============================
certbot-dns-openstack
===============================

OpenStack DNS Authenticator plugin for Certbot

To Install:

``pip install certbot-dns-openstack``

To run: 

``certbot -a certbot-dns-openstack:dns-openstack certonly -d example.com``

This uses ``os-client-config`` ``clouds.yaml`` for configuring the user access
which by default will look in ``~/.config/openstack/clouds.yaml``, 
and ``/etc/openstack/clouds.yaml``. If your ``clouds.yaml`` file is stored else
where, you can add by adding 
``--certbot-dns-openstack:dns-openstack-config /path/to/clouds.yaml`` to the 
command.

* Free software: Apache license
* Source: https://git.openstack.org/cgit/openstack/certbot-dns-openstack
* Bugs: https://bugs.launchpad.net/certbot-dns-openstack

Features
--------

* dns-01 ACME challenge
