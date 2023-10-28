select column1 as orig_value,
   to_char(column1, '">"$99.0"<"') as D2_1,
   to_char(column1, '">"B9,999.0"<"') as D4_1,
   to_char(column1, '">"TME"<"') as TME,
   to_char(column1, '">"TM9"<"') as TM9,
   to_char(column1, '">"0XXX"<"') as X4,
   to_char(column1, '">"S0XXX"<"') as SX4
from values (-12.391), (0), (-1), (0.10), (0.01), (3987), (1.111);
