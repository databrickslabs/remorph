SELECT DATE_FROM_PARTS(2004, 1, 1),   -- January 1, 2004, as expected.
       DATE_FROM_PARTS(2004, 0, 1),   -- This is one month prior to DATE_FROM_PARTS(2004, 1, 1), so it's December 1, 2003.
                                      -- This is NOT a synonym for January 1, 2004.
       DATE_FROM_PARTS(2004, -1, 1)   -- This is two months (not one month) before DATE_FROM_PARTS(2004, 1, 1), so it's November 1, 2003.
       ;