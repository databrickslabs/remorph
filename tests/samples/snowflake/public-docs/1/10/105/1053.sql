SELECT ST_MAKELINE(
                   TO_GEOGRAPHY('POINT(-122.306067 37.55412)'),
                   TO_GEOGRAPHY('MULTIPOINT((-122.32328 37.561801), (-122.325879 37.586852))')
                  ) AS line_between_point_and_multipoint;