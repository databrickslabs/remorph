-- migrate an existing IDP configuration

select system$migrate_saml_idp_registration('my_fed_integration', 'http://my_idp.com');


-- view the newly created security integration

desc integration my_fed_integration;