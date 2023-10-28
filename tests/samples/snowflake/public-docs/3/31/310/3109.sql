alter view v1
  drop row access policy rap_v1_version_1,
  add row access policy rap_v1_version_2 on (empl_id);