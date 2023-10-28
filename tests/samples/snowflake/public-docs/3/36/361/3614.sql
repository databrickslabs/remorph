create or replace function my_st_x(G geography) returns real
language javascript
as
$$
  if (G["type"] != "Point")
  {
     throw "Not a point"
  }
  return G["coordinates"][0]
$$;

create or replace function my_st_makepoint(LNG real, LAT real) returns geography
language javascript
as
$$
  g = {}
  g["type"] = "Point"
  g["coordinates"] = [ LNG, LAT ]
  return g
$$;