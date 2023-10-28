clusteringAction ::=
  {
     CLUSTER BY ( <expr> [ , <expr> , ... ] )
     /* RECLUSTER is deprecated */
   | RECLUSTER [ MAX_SIZE = <budget_in_bytes> ] [ WHERE <condition> ]
     /* { SUSPEND | RESUME } RECLUSTER is valid action */
   | { SUSPEND | RESUME } RECLUSTER
   | DROP CLUSTERING KEY
  }