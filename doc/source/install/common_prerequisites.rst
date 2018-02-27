Prerequisites
-------------

Before you install and configure the certbot-dns-openstack service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``certbot_dns_openstack`` database:

     .. code-block:: none

        CREATE DATABASE certbot_dns_openstack;

   * Grant proper access to the ``certbot_dns_openstack`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON certbot_dns_openstack.* TO 'certbot_dns_openstack'@'localhost' \
          IDENTIFIED BY 'CERTBOT_DNS_OPENSTACK_DBPASS';
        GRANT ALL PRIVILEGES ON certbot_dns_openstack.* TO 'certbot_dns_openstack'@'%' \
          IDENTIFIED BY 'CERTBOT_DNS_OPENSTACK_DBPASS';

     Replace ``CERTBOT_DNS_OPENSTACK_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``certbot_dns_openstack`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt certbot_dns_openstack

   * Add the ``admin`` role to the ``certbot_dns_openstack`` user:

     .. code-block:: console

        $ openstack role add --project service --user certbot_dns_openstack admin

   * Create the certbot_dns_openstack service entities:

     .. code-block:: console

        $ openstack service create --name certbot_dns_openstack --description "certbot-dns-openstack" certbot-dns-openstack

#. Create the certbot-dns-openstack service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        certbot-dns-openstack public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        certbot-dns-openstack internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        certbot-dns-openstack admin http://controller:XXXX/vY/%\(tenant_id\)s
