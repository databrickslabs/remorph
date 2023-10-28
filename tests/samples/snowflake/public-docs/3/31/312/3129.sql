clusteringAction ::=
  {
     CLUSTER BY ( <expr> [ , <expr> , ... ] )
   | { SUSPEND | RESUME } RECLUSTER
   | DROP CLUSTERING KEY
  }