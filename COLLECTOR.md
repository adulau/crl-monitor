
Building your own SSL certificate collector
===========================================

In order to build your own collector box for SSL certificate, ssldump
is required. The best is clone my ssldump version including recent
patches and some fixes for tapping monitored uplinks.

~~~~
git clone https://github.com/adulau/ssldump.git
cd ssldump
./configure --with-pcap-lib=/usr/lib/x86_64-linux-gnu/
~~~~

ssldump needs to be built *WITHOUT* OpenSSL support. We gather the raw
certificate extracted with ssldump directly.

Starting collection
===================

To test the compiled ssldump binary:

~~~~
cd ssldump
sudo ./ssldump -ANn -i eth1
~~~~

To test the parsing of the raw certificates:

~~~~
cd ssldump
sudo ./ssldump -ANn -i eth1 | python ../crl-monitor/bin/x509/pcap-sslcert.py -v
~~~~

Feeding the certificate store:



