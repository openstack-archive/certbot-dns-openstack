2. Edit the ``/etc/certbot_dns_openstack/certbot_dns_openstack.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://certbot_dns_openstack:CERTBOT_DNS_OPENSTACK_DBPASS@controller/certbot_dns_openstack
