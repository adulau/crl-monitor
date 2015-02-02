crl-monitor
===========

CRL Monitor - X.509 Certificate Revocation List monitoring 

X.509 Subject Cache
================

There is a set of tool to maintain a cache of certificate fingerprints
along with the IP addresses seen with a specific fingerprint and subject.

In order to feed the cache, dumps of SSL scans need to be imported.

If you use the great dumps from [scans.io](https://scans.io/), you can do the following to import the certificate data:

~~~~
zcat ./scans-io/data/20141208_certs.gz | python dumpx509subject.py -p 6381 -s
~~~~

This command parses all the certificates and extract the subjects and  imports these into the Redis-compatible database running on TCP port 6381. 

Then you need to import the mapping between scanned IP addresses and the fingerprint of the X.509 certificate seen:

~~~~
zcat ./scans-io/data/20141208_hosts.gz | python hoststoredis.py -p 6381
~~~~

The above procedure can be repeated with additional scans or you can import multiple scans in parallel using GNU Parallel.
 
IP Subnet Lookup in X.509 Subject Cache
================================

ip-ssl-subject.py can query a network subnet and display the known certificate seen and display the X.509 subject if known.

~~~~
python ./bin/x509/ip-ssl-subject.py -s 199.16.156.0/28 -p 6381
~~~~

~~~~
199.16.156.6
 1.3.6.1.4.1.311.60.2.1.3=US/1.3.6.1.4.1.311.60.2.1.2=Delaware/businessCategory=Private Organization/serialNumber=4337446, C=US/postalCode=94107, ST=California, L=San Francisco/street=795 Folsom St, Suite 600, O=Twitter, Inc., OU=Twitter Security, CN=twitter.com
 C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)06, CN=VeriSign Class 3 Extended Validation SSL CA
 add53f6680fe66e383cbac3e60922e3b4c412bed
 e3fc0ad84f2f5a83ed6f86f567f8b14b40dcbf12
199.16.156.7
 C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert High Assurance CA-3
 C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert SHA2 High Assurance Server CA
 C=US, ST=CA, L=San Francisco, O=Twitter, Inc., OU=Twitter Security, CN=tdweb.twitter.com
 859b86acd1604078f7d0f4680fdff59965096745
 1858b819fffad8c948fac853882c5e8bbc5e7953
199.16.156.8
 d8015bf46dfb91c6e4b1b6ab9a72c168933dc2d9
 C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)09, CN=VeriSign Class 3 Secure Server CA - G2
 C=US, ST=California, L=San Francisco, O=Twitter, Inc., OU=Twitter Security, CN=api.twitter.com
 C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 Secure Server CA - G3
199.16.156.9
 C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA
 serialNumber=X5-6oDhQgpWsUADnOU2IdZ38YWlIV8/8, C=US, ST=California, L=San Francisco, O=Twitter, Inc., CN=*.twitter.com
199.16.156.10
 add53f6680fe66e383cbac3e60922e3b4c412bed
 e3fc0ad84f2f5a83ed6f86f567f8b14b40dcbf12
199.16.156.11
 C=US, ST=California, L=San Francisco, O=Twitter, Inc., OU=Twitter Security, CN=t.co
 C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 Secure Server CA - G3
199.16.156.12
 C=US, ST=California, L=San Francisco, O=Twitter, Inc., OU=Twitter Security, CN=support.twitter.com
 C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=Terms of use at https://www.verisign.com/rpa (c)10, CN=VeriSign Class 3 Secure Server CA - G3
~~~~

## Data store format

~~~~
{IPv4} -> set of {SHA1 FP}
{SHA1 FP} -> set of {Subject}
~~~~

~~~~
{s:SHA1 FP} -> set of {IPv4}
~~~~
