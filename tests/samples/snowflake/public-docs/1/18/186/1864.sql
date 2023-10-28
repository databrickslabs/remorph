use role accountadmin;

select SYSTEM$GET_PRIVATELINK(
    '185...',
    '{
      "Credentials": {
          "AccessKeyId": "ASI...",
          "SecretAccessKey": "enw...",
          "SessionToken": "Fwo...",
          "Expiration": "2021-01-07T19:06:23+00:00"
      },
      "FederatedUser": {
          "FederatedUserId": "185...:sam",
          "Arn": "arn:aws:sts::185...:federated-user/sam"
      },
      "PackedPolicySize": 0
  }'
  );