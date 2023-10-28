select system$generate_saml_csr('my_idp', 'cn=juser, ou=dev, ou=people, o=eng, dc=com');

--------------------------------------------------------------------------------------------------+
SYSTEM$GENERATE_SAML_CSR('MY_IDP')                                                                |
--------------------------------------------------------------------------------------------------+
-----BEGIN NEW CERTIFICATE REQUEST-----                                                           |
MIICWzCCAUMCAQAwFjEUMBIGA1UEAxMLVEVTVEFDQ09VTlQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDCRpyZ  |
...                                                                                               |
-----END NEW CERTIFICATE REQUEST-----                                                             |
--------------------------------------------------------------------------------------------------+