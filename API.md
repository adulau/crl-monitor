
Passive SSL
-----------

Passive SSL is a database storing historical X.509 certificates seen per IP address. The Passive SSL historical data is indexed per IP address, which makes it searchable for incident handlers, security analysts or researchers.

## How can you collect SSL certificates?

The Passive SSL database can public scanning datasets like the excellent [scans.io project](http://scans.io/).

For more information, [Passive SSL was presented at FIRST 2015 in Berlin](https://www.first.org/resources/papers/conf2015/first_2015_-_leverett_-_dulaunoy_-_passive_detection_20150604.pdf).

## How to start the API service?

You have to run [ip-ssl-subject-api.py](https://github.com/adulau/crl-monitor/blob/master/bin/x509/ip-ssl-subject-api.py) on the server where the import was done in the redis server.

## How to use the service?

Passive SSL is accessible via a REST API and the output is in JSON format.

The REST API is accessible via the following URLs. 'query' is to query IP address or CIDR blocks (/32 up to /23). 'cquery' is to query per certificate fingerprint and find where the certificate is used per IP address. 'cfetch' is to fetch and parse a specified certificate from the Passive SSL store by its fingerprint.

~~~
https://<yourserver>/v2pssl/query/<CIDR block>
https://<yourserver>/v2pssl/cquery/<SHA1 certificate fingerprint>
https://<yourserver>/cfetch/<SHA1 certificate fingerprint>
~~~

Query values can be IP addresses or CIDR blocks between /32 up to /23:

~~~
https://<yourserver>/v2pssl/query/172.228.24.0/28
~~~

and a sample JSON output:

~~~ json
{"172.228.24.7": {"certificates": ["37221925980c05deefac014f9a72b4765e716341", "3209cc3ce4f1c22ab64b2e4284100b0022ad2739", "4d34ea92764b3a3149119952f41930ca11348361", "6ad2b04e2196e48bf685752890e811cd2ed60606", "c43b30bf08bfb0b92c070f42f51b6980c8ada064", "30d1fd4a296ab1a8831cd56b4110a227f557bfff", "79068f16776372aa6b12b83dd2b7288298727f54"], "subjects": {"37221925980c05deefac014f9a72b4765e716341": {"values": ["C=JP, ST=Tokyo, L=Minato-ku, O=Sony corporation, OU=NPS, CN=psn-rsc.prod.dl.playstation.net"]}, "3209cc3ce4f1c22ab64b2e4284100b0022ad2739": {"values": ["C=NL, L=Amsterdam, O=Verizon Enterprise Solutions, OU=Cybertrust, CN=Verizon Akamai SureServer CA G14-SHA1"]}, "4d34ea92764b3a3149119952f41930ca11348361": {"values": ["C=IE, O=Baltimore, OU=CyberTrust, CN=Baltimore CyberTrust Root"]}, "c43b30bf08bfb0b92c070f42f51b6980c8ada064": {"values": ["C=CY, ST=Cyprus, L=Limassol, O=Blue Capital Markets Limited, OU=IT, CN=www.easy-forex.com"]}, "6ad2b04e2196e48bf685752890e811cd2ed60606": {"values": ["C=NL, L=Amsterdam, O=Verizon Enterprise Solutions, OU=Cybertrust, CN=Verizon Akamai SureServer CA G14-SHA2"]}, "30d1fd4a296ab1a8831cd56b4110a227f557bfff": {"values": ["O=Cybertrust Inc, CN=Cybertrust Public SureServer SV CA"]}, "79068f16776372aa6b12b83dd2b7288298727f54": {"values": ["C=CY, ST=Cyprus, L=Limassol, O=Easy Forex, OU=IT, CN=www.easy-forex.com"]}}}, "172.228.24.8": {"certificates": ["4ab70b97decd784aa60395a351daf4274fd37fca", "e3fc0ad84f2f5a83ed6f86f567f8b14b40dcbf12", "c46fed822dadac3f31f9bb4d1a78a1d9eae4567b", "4d34ea92764b3a3149119952f41930ca11348361", "30d1fd4a296ab1a8831cd56b4110a227f557bfff", "32f30882622b87cf8856c63db873df0853b4dd27"], "subjects": {"4ab70b97decd784aa60395a351daf4274fd37fca": {"values": ["C=US, ST=MARYLAND, L=Hanover, O=Allegis Group Inc, OU=IT, CN=*.apac.allegisgroup.com"]}, "e3fc0ad84f2f5a83ed6f86f567f8b14b40dcbf12": {"values": ["C=US, O=Symantec Corporation, OU=Symantec Trust Network, CN=Symantec Class 3 EV SSL CA - G3"]}, "c46fed822dadac3f31f9bb4d1a78a1d9eae4567b": {"values": ["1.3.6.1.4.1.311.60.2.1.3=AU/businessCategory=Private Organization/serialNumber=85 092 445 442, C=AU/postalCode=1230, ST=NSW, L=Sydney/street=680 George Street, O=HotelClub Pty. Ltd., OU=Engineering, CN=www.hotelclub.cn"]}, "4d34ea92764b3a3149119952f41930ca11348361": {"values": ["C=IE, O=Baltimore, OU=CyberTrust, CN=Baltimore CyberTrust Root"]}, "30d1fd4a296ab1a8831cd56b4110a227f557bfff": {"values": ["O=Cybertrust Inc, CN=Cybertrust Public SureServer SV CA"]}, "32f30882622b87cf8856c63db873df0853b4dd27": {"values": ["C=US, O=VeriSign, Inc., OU=VeriSign Trust Network, OU=(c) 2006 VeriSign, Inc. - For authorized use only, CN=VeriSign Class 3 Public Primary Certification Authority - G5"]}}}, "172.228.24.9": {"certificates": ["780a06f6e9b4061cad0c6502710606eb535f1c26", "08ff9ecb28facd74dd125ded44f4e0dd6707f902", "2ea71c367d178c843fd21db4fdb630ba54a20dc5", "d10050dad40f850c2f84c215929e344ff8c9c552"], "subjects": {"780a06f6e9b4061cad0c6502710606eb535f1c26": {"values": ["C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA"]}, "08ff9ecb28facd74dd125ded44f4e0dd6707f902": {"values": ["serialNumber=Dyi4QNdi9bHxOhWakExUXmDdd09Ny/kj, C=US, ST=Texas, L=Dallas, O=FareCompare, LP, OU=Information Technology, CN=www.farecompare.com"]}, "2ea71c367d178c843fd21db4fdb630ba54a20dc5": {"values": ["C=US, O=thawte, Inc., CN=thawte SSL CA - G2"]}, "d10050dad40f850c2f84c215929e344ff8c9c552": {"values": ["C=US, ST=California, L=San Jose, O=Altera Corporation, OU=IT, CN=*.altera.com.cn"]}}}, "172.228.24.10": {"certificates": ["4b948bf1b5852e1fc0a4ffd73a4087c967e2c968", "780a06f6e9b4061cad0c6502710606eb535f1c26", "de28f4a4ffe5b92fa3c503d1a349a7f9962a8212"], "subjects": {"4b948bf1b5852e1fc0a4ffd73a4087c967e2c968": {"values": ["serialNumber=votSFS5N71H6C8XC9xvyFnfXnCbjfirr, C=GB, ST=London, L=London, O=News Group Newspapers Ltd, CN=join.thesun.co.uk"]}, "780a06f6e9b4061cad0c6502710606eb535f1c26": {"values": ["C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA"]}, "de28f4a4ffe5b92fa3c503d1a349a7f9962a8212": {"values": ["C=US, O=GeoTrust Inc., CN=GeoTrust Global CA"]}}}, "172.228.24.11": {"certificates": ["780a06f6e9b4061cad0c6502710606eb535f1c26", "de28f4a4ffe5b92fa3c503d1a349a7f9962a8212", "542ff5a0a035c1e2f0845fd0ed54ccf9bee2517c"], "subjects": {"780a06f6e9b4061cad0c6502710606eb535f1c26": {"values": ["C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA"]}, "de28f4a4ffe5b92fa3c503d1a349a7f9962a8212": {"values": ["C=US, O=GeoTrust Inc., CN=GeoTrust Global CA"]}, "542ff5a0a035c1e2f0845fd0ed54ccf9bee2517c": {"values": ["serialNumber=Y8t0npKVp3Fpoq45a6WRSh/ZdY9/FX3r, C=US, ST=California, L=San Diego, O=INTUIT INC., OU=Tech_Ops, CN=quickbase.intuit.com"]}}}, "172.228.24.12": {"certificates": ["c53e73073f93ce7895de7484126bc303dab9e657", "503006091d97d4f5ae39f7cbe7927d7d652d3431", "3209cc3ce4f1c22ab64b2e4284100b0022ad2739", "aca9789a735eb253b410ccb979bb35e5e7dcdea9", "4d34ea92764b3a3149119952f41930ca11348361", "43b31c858772f17f87235272cf339c29160727c7"], "subjects": {"c53e73073f93ce7895de7484126bc303dab9e657": {"values": ["C=US, O=Entrust, Inc., OU=www.entrust.net/rpa is incorporated by reference, OU=(c) 2009 Entrust, Inc., CN=Entrust Certification Authority - L1C"]}, "503006091d97d4f5ae39f7cbe7927d7d652d3431": {"values": ["O=Entrust.net, OU=www.entrust.net/CPS_2048 incorp. by ref. (limits liab.), OU=(c) 1999 Entrust.net Limited, CN=Entrust.net Certification Authority (2048)"]}, "3209cc3ce4f1c22ab64b2e4284100b0022ad2739": {"values": ["C=NL, L=Amsterdam, O=Verizon Enterprise Solutions, OU=Cybertrust, CN=Verizon Akamai SureServer CA G14-SHA1"]}, "aca9789a735eb253b410ccb979bb35e5e7dcdea9": {"values": ["C=US, ST=WA, L=Seattle, O=Getty Images, Inc., OU=iStockphoto, CN=secure.istockphoto.com"]}, "4d34ea92764b3a3149119952f41930ca11348361": {"values": ["C=IE, O=Baltimore, OU=CyberTrust, CN=Baltimore CyberTrust Root"]}, "43b31c858772f17f87235272cf339c29160727c7": {"values": ["C=US, ST=Georgia, L=Atlanta, O=The Home Depot, CN=kdlms.homedepot.com"]}}}, "172.228.24.13": {"certificates": ["780a06f6e9b4061cad0c6502710606eb535f1c26", "1a7d8d6e58caeb72bb4237ffc1c04e8d368c913a"], "subjects": {"780a06f6e9b4061cad0c6502710606eb535f1c26": {"values": ["C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA"]}, "1a7d8d6e58caeb72bb4237ffc1c04e8d368c913a": {"values": ["serialNumber=dVn4HhED532-1HQOwGkA/TovT-JtOEMN, C=US, ST=California, L=Rancho Dominguez, O=Onestop Internet Inc., OU=Onestop Internet, CN=www.onestop.com"]}}}, "172.228.24.14": {"certificates": ["1ae8aaddeb4e27392c4a549a7df2d6aef4e95e7a", "30d1fd4a296ab1a8831cd56b4110a227f557bfff", "ac8f7c5bc86ef1896f2d161c32a57aab37d364da", "4136bb45dd375b8cba5f430d0a03e50edbe7410a", "4d34ea92764b3a3149119952f41930ca11348361"], "subjects": {"1ae8aaddeb4e27392c4a549a7df2d6aef4e95e7a": {"values": ["C=US, ST=SOUTH CAROLINA, L=Hilton Head Island, O=Hilton Head Island-Bluffton Chamber of Commerce, OU=IT, CN=*.hiltonheadisland.org"]}, "30d1fd4a296ab1a8831cd56b4110a227f557bfff": {"values": ["O=Cybertrust Inc, CN=Cybertrust Public SureServer SV CA"]}, "4d34ea92764b3a3149119952f41930ca11348361": {"values": ["C=IE, O=Baltimore, OU=CyberTrust, CN=Baltimore CyberTrust Root"]}, "4136bb45dd375b8cba5f430d0a03e50edbe7410a": {"values": ["C=DE, ST=Baden-Wuerttemberg, L=Walldorf, O=SAP SE, OU=Cloud Infrastructure Delivery, CN=pilot.support.sap.com"]}, "ac8f7c5bc86ef1896f2d161c32a57aab37d364da": {"values": ["C=US, O=GeoTrust Inc., CN=GeoTrust SSL CA - G4"]}}}, "172.228.24.15": {"certificates": ["780a06f6e9b4061cad0c6502710606eb535f1c26", "afe5fac5f3dae7523b7e2948d72f95f80a5b0e42"], "subjects": {"780a06f6e9b4061cad0c6502710606eb535f1c26": {"values": ["C=US, O=GeoTrust, Inc., CN=GeoTrust SSL CA"]}, "afe5fac5f3dae7523b7e2948d72f95f80a5b0e42": {"values": ["serialNumber=2Fr160kmOjBTWTTIe/pv4hmFm0kiNYOP, C=US, ST=California, L=Ventura, O=Patagonia, OU=Ventura, CN=www.patagonia.com"]}}}}
~~~

Query value in cquery is the SHA1 fingerprint of a certificate:

~~~
https://<yourserver>/v2pssl/cquery/c46fed822dadac3f31f9bb4d1a78a1d9eae4567b
~~~

and returns a list of seen IP addresses for the requested certificate:

~~~json
{"seen": ["149.13.33.13", "149.13.33.11", "149.13.33.4", "149.13.33.9"], "hits": 4, "certificate": "7c552ab044c76d1df4f5ddf358807bfdcd07fa57"}
~~~

The X509 certificate can be requested by its fingerprint:

~~~
https://<yourserver>/v2pssl/cfetch/7c552ab044c76d1df4f5ddf358807bfdcd07fa57
~~~

the raw certificate will be returned, including its readable output:

~~~json
{
  "icsi": {
    "last_seen": "16596",
    "times_seen": "5",
    "validated": "1",
    "version": "1",
    "first_seen": "16469"
  },
  "pem": "-----BEGIN CERTIFICATE-----\nMIIFvDCCBKSgAwIBAgIDBivRMA0GCSqGSIb3DQEBBQUAMEUxCzAJBgNVBAYTAkxV\nMRYwFAYDVQQKEw1MdXhUcnVzdCBTLkEuMR4wHAYDVQQDExVMdXhUcnVzdCBRdWFs\naWZpZWQgQ0EwHhcNMTQwNzE3MTIyNDE2WhcNMTYwNzE3MTIyNDE2WjCBwDELMAkG\nA1UEBhMCTFUxEzARBgNVBAgTCkx1eGVtYm91cmcxEzARBgNVBAcTCkx1eGVtYm91\ncmcxPTA7BgNVBAoTNENJUkNMIC0gQ29tcHV0ZXIgSW5jaWRlbnQgUmVzcG9uc2Ug\nQ2VudGVyIEx1eGVtYm91cmcxFTATBgNVBAsTDFdlYiBTZXJ2aWNlczETMBEGA1UE\nAxQKKi5jaXJjbC5sdTEcMBoGCSqGSIb3DQEJARYNaW5mb0BjaXJjbC5sdTCCASIw\nDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALz26kXiY2TfqHukFJMy9BMvWjyS\nQntEMZc2VV/uWW8nQ9BT43aEVBK0Y7JcLfEPd72oDs7yQrhqyuSiXVLrJzOu7nI9\nLWmEqX/WVZHbS4mdmdo/d2gllirmpClpI6W5v68qUd4zxlSQxrnPzpyVWtmih8Nw\nRHGIo/YttLAqjao37CuGHS3ltRTaAB30ToJgfK5fDWvtOjoomRvjZNhTNO/ZEdaw\nwygsF8NBDoWyOwoSRqNA9UOuBM70Bdu4VJkCyDJVQzaTx0mPbV+iXmKFj33MyfTx\nZMASXiG+e0+Q1ih53X2+GeDWElbM6lv2XKVP3Ueo4qh43CgBtX1El0zCzf8CAwEA\nAaOCAjcwggIzMAwGA1UdEwEB/wQCMAAwYAYIKwYBBQUHAQEEVDBSMCMGCCsGAQUF\nBzABhhdodHRwOi8vb2NzcC5sdXh0cnVzdC5sdTArBggrBgEFBQcwAoYfaHR0cDov\nL2NhLmx1eHRydXN0Lmx1L0xUUUNBLmNydDCCAQAGA1UdIASB+DCB9TCB6AYIK4Er\nAQECBgEwgdswga0GCCsGAQUFBwICMIGgGoGdTHV4VHJ1c3QgU2VydmVyIENlcnRp\nZmljYXRlLiBOb3Qgc3VwcG9ydGVkIGJ5IFNTQ0QsIEtleSBHZW5lcmF0aW9uIGJ5\nIFN1YnNjcmliZXIuIEdUQywgQ1AgYW5kIENQUyBvbiBodHRwOi8vcmVwb3NpdG9y\neS5sdXh0cnVzdC5sdS4gU2lnbmVkIGJ5IGEgUXVhbGlmaWVkIENBLjApBggrBgEF\nBQcCARYdaHR0cDovL3JlcG9zaXRvcnkubHV4dHJ1c3QubHUwCAYGBACPegEDMBEG\nCWCGSAGG+EIBAQQEAwIF4DAOBgNVHQ8BAf8EBAMCBLAwJwYDVR0lBCAwHgYIKwYB\nBQUHAwEGCCsGAQUFBwMCBggrBgEFBQcDBDAfBgNVHSMEGDAWgBSNkKMH3RoTd5lM\nkqtNQ94/zSlkBTAxBgNVHR8EKjAoMCagJKAihiBodHRwOi8vY3JsLmx1eHRydXN0\nLmx1L0xUUUNBLmNybDAdBgNVHQ4EFgQUfxT4ZRAbCmnrRK2KZDrE4Dxp7dIwDQYJ\nKoZIhvcNAQEFBQADggEBAIeg9n+bdv0RouFl++1BlotUD3fXRbhURL0Bzpe6w2hy\nRGAFxA1u1AWwtrowQ53Awh6ZJxntHmeYTlchl1Hc79Gt7wHeBI4phack5iTFKJzL\nvdLeGYjj4qJ9LNNt2hNf8Z5u72oMe6xq9naBWJibyzrHQgBsdl/iSMBEQbEkcfXW\nCDpqMrvhHapkL3zJZE0mIOb2wZ+Xqh7XG+9qqfTVjq+Bi/Ihja2ueV8X+TI/cizr\nFU3QrEV4rwIb6FcSX6R5qnlIh8bfm+aDAZCQZXJa9eheeYJw39ibYRxmc6FvR35c\n5zWFlvTe1e7OuPN09CyPJHCxfidIFlBDnQzxAiHBgLs=\n-----END CERTIFICATE-----\n",
  "info": {
    "subject": "C=LU, ST=Luxembourg, L=Luxembourg, O=CIRCL - Computer Incident Response Center Luxembourg, OU=Web Services, CN=*.circl.lu/emailAddress=info@circl.lu",
    "not_before": "2014-07-17T12:24:16+00:00",
    "issuer": "C=LU, O=LuxTrust S.A., CN=LuxTrust Qualified CA",
    "fingerprint": "7C552AB044C76D1DF4F5DDF358807BFDCD07FA57",
    "key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvPbqReJjZN+oe6QUkzL0\nEy9aPJJCe0QxlzZVX+5ZbydD0FPjdoRUErRjslwt8Q93vagOzvJCuGrK5KJdUusn\nM67ucj0taYSpf9ZVkdtLiZ2Z2j93aCWWKuakKWkjpbm/rypR3jPGVJDGuc/OnJVa\n2aKHw3BEcYij9i20sCqNqjfsK4YdLeW1FNoAHfROgmB8rl8Na+06OiiZG+Nk2FM0\n79kR1rDDKCwXw0EOhbI7ChJGo0D1Q64EzvQF27hUmQLIMlVDNpPHSY9tX6JeYoWP\nfczJ9PFkwBJeIb57T5DWKHndfb4Z4NYSVszqW/ZcpU/dR6jiqHjcKAG1fUSXTMLN\n/wIDAQAB\n-----END PUBLIC KEY-----\n",
    "keylength": 2048,
    "not_after": "2016-07-17T12:24:16+00:00",
    "extension": {
      "basicConstraints": "CA:FALSE",
      "subjectKeyIdentifier": "7F:14:F8:65:10:1B:0A:69:EB:44:AD:8A:64:3A:C4:E0:3C:69:ED:D2",
      "authorityKeyIdentifier": "keyid:8D:90:A3:07:DD:1A:13:77:99:4C:92:AB:4D:43:DE:3F:CD:29:64:05\n",
      "extendedKeyUsage": "TLS Web Server Authentication, TLS Web Client Authentication, E-mail Protection",
      "crlDistributionPoints": "\nFull Name:\n  URI:http://crl.luxtrust.lu/LTQCA.crl\n",
      "keyUsage": "Digital Signature, Key Encipherment, Data Encipherment",
      "certificatePolicies": "Policy: 1.3.171.1.1.2.6.1\n  User Notice:\n    Explicit Text: LuxTrust Server Certificate. Not supported by SSCD, Key Generation by Subscriber. GTC, CP and CPS on http://repository.luxtrust.lu. Signed by a Qualified CA.\n  CPS: http://repository.luxtrust.lu\nPolicy: 0.4.0.2042.1.3\n",
      "nsCertType": "SSL Client, SSL Server, S/MIME",
      "authorityInfoAccess": "OCSP - URI:http://ocsp.luxtrust.lu\nCA Issuers - URI:http://ca.luxtrust.lu/LTQCA.crt\n"
    }
  }
}

~~~

