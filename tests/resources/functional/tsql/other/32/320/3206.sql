-- tsql sql:
CREATE USER CustomAppDev WITHOUT LOGIN;
GRANT IMPERSONATE ON USER::CustomAppDev TO [adventure-works\tengiz1];
