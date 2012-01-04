## INSTRUCTIONS

1. Modify the template .conf files in templates/ for your usage, 
   or create a new one for your specific phone. Bear in mind the
   following replacements can be pasted into the config anywhere
   to insert a phone-specific value:

   * %(phone_name)s
   * %(sip_name)s
   * %(sip_server)s
   * %(config_server)s
   * %(firmware_server)s
   * %(sip_auth)s
   * %(sip_pass)s
   * %(auth_prepend)s
   * %(auth_append)s
   * %(xml_path)s

   It is also possible to add vars to the equipment and phones
   sections of the gxpgen.conf file, and these will be combined
   together for each phone (e.g. each phone has access to the
   contents of the 'equipment' section and the specific 'phones'
   section that matches its' MAC.

   *e.g. It would be possible to add "sip_port: 5061" to
   gxpgen.conf, and then refer to it in a template using 
   "%(sip_port)s".*

2. Modify the gxpgen.conf file to contain the correct values for 
   your setup ('equipment' section settings apply for all phones,
   and each specific phone takes extra values from the 'phones'
   section based on its' MAC address. Phone specific settings are
   things like sip_auth and sip_pass, whereas equipment settings
   would be suitable for setting dns_server or the like.

3. Execute ./gxpgen.py and check output.

4. Serve the newly created cfg directory via HTTP, and tell your
   phones to use that address as their configuration server. 


## LICENSE

Copyright © 2011-2012, Ben Agricola. See the `COPYING` file for 
license rights and limitations (MIT).
