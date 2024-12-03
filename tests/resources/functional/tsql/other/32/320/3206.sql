--Query type: DCL
CREATE USER CustomAppDev WITHOUT LOGIN;
GRANT IMPERSONATE ON USER::CustomAppDev TO [adventure-works\tengiz1];
