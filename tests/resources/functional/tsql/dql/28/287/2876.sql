--Query type: DQL
WITH session_data AS (
  SELECT 
    session_id,
    host_name,
    program_name,
    nt_domain,
    login_name,
    connect_time,
    last_request_end_time
  FROM (
    VALUES 
      (1, 'host1', 'program1', 'domain1', 'login1', '2022-01-01 12:00:00', '2022-01-01 12:00:00'),
      (2, 'host2', 'program2', 'domain2', 'login2', '2022-01-01 13:00:00', '2022-01-01 13:00:00')
  ) AS sessions (session_id, host_name, program_name, nt_domain, login_name, connect_time, last_request_end_time)
),
connection_data AS (
  SELECT 
    session_id,
    connection_id,
    connection_time
  FROM (
    VALUES 
      (1, 1, '2022-01-01 12:00:00'),
      (2, 2, '2022-01-01 13:00:00')
  ) AS connections (session_id, connection_id, connection_time)
)
SELECT 
  cd.session_id,
  sd.host_name,
  sd.program_name,
  sd.nt_domain,
  sd.login_name,
  sd.connect_time,
  sd.last_request_end_time
FROM session_data AS sd
JOIN connection_data AS cd ON sd.session_id = cd.session_id;