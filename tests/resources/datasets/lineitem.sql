--------------------------------------------------------------------------------
CREATE TABLE lineitem (
  l_orderkey BIGINT,
  l_partkey BIGINT,
  l_suppkey BIGINT,
  l_linenumber INT,
  l_quantity DECIMAL(18,2),
  l_extendedprice DECIMAL(18,2),
  l_discount DECIMAL(18,2),
  l_tax DECIMAL(18,2),
  l_returnflag VARCHAR(500),
  l_linestatus VARCHAR(500),
  l_shipdate DATE,
  l_commitdate DATE,
  l_receiptdate DATE,
  l_shipinstruct VARCHAR(500),
  l_shipmode VARCHAR(500),
  l_comment VARCHAR(500)
  );

--------------------------------------------------------------------------------

INSERT INTO lineitem (l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment) VALUES
(1, 155189345, 7689361, 1, 17.00, 24252.03, 0.04, 0.02, 'N', 'O', '1996-03-13', '1996-02-12', '1996-03-22', 'DELIVER IN PERSON', 'TRUCK', 'egular courts above the'),
 (1, 67309080, 7309081, 2, 36.00, 39085.92, 0.09, 0.06, 'N', 'O', '1996-04-12', '1996-02-28', '1996-04-20', 'TAKE BACK RETURN', 'MAIL', 'ly final dependencies: slyly bold '),
 (1, 63699776, 3699777, 3, 8.00, 14180.72, 0.10, 0.02, 'N', 'O', '1996-01-29', '1996-03-05', '1996-01-31', 'TAKE BACK RETURN', 'REG AIR', 'riously. regular, express dep'),
 (1, 2131495, 4631496, 4, 28.00, 42738.92, 0.09, 0.06, 'N', 'O', '1996-04-21', '1996-03-30', '1996-05-16', 'NONE', 'AIR', 'lites. fluffily even de'),
 (1, 24026634, 1526641, 5, 24.00, 37426.32, 0.10, 0.04, 'N', 'O', '1996-03-30', '1996-03-14', '1996-04-01', 'NONE', 'FOB', ' pending foxes. slyly re'),
 (1, 15634450, 634453, 6, 32.00, 44277.44, 0.07, 0.02, 'N', 'O', '1996-01-30', '1996-02-07', '1996-02-03', 'DELIVER IN PERSON', 'MAIL', 'arefully slyly ex'),
 (2, 106169722, 1169743, 1, 38.00, 67883.96, 0.00, 0.05, 'N', 'O', '1997-01-28', '1997-01-14', '1997-02-02', 'TAKE BACK RETURN', 'RAIL', 'ven requests. deposits breach a'),
 (3, 4296962, 1796963, 1, 45.00, 88143.75, 0.06, 0.00, 'R', 'F', '1994-02-02', '1994-01-04', '1994-02-23', 'NONE', 'AIR', 'ongside of the furiously brave acco'),
 (3, 19035429, 6535433, 2, 49.00, 66810.03, 0.10, 0.00, 'R', 'F', '1993-11-09', '1993-12-20', '1993-11-24', 'TAKE BACK RETURN', 'RAIL', ' unusual accounts. eve'),
 (3, 128448229, 3448254, 3, 27.00, 31611.60, 0.06, 0.07, 'A', 'F', '1994-01-16', '1993-11-22', '1994-01-23', 'DELIVER IN PERSON', 'SHIP', 'nal foxes wake. '),
 (3, 29379610, 1879613, 4, 2.00, 3376.30, 0.01, 0.06, 'A', 'F', '1993-12-04', '1994-01-07', '1994-01-01', 'NONE', 'TRUCK', 'y. fluffily pending d'),
 (3, 183094077, 594132, 5, 28.00, 29733.76, 0.04, 0.00, 'R', 'F', '1993-12-14', '1994-01-10', '1994-01-01', 'TAKE BACK RETURN', 'FOB', 'ages nag slyly pending'),
 (3, 62142591, 9642610, 6, 26.00, 42392.74, 0.10, 0.02, 'A', 'F', '1993-10-29', '1993-12-18', '1993-11-04', 'TAKE BACK RETURN', 'RAIL', 'ges sleep after the caref'),
 (4, 88034684, 5534709, 1, 30.00, 48428.40, 0.03, 0.08, 'N', 'O', '1996-01-10', '1995-12-14', '1996-01-18', 'DELIVER IN PERSON', 'REG AIR', '- quickly regular packages sleep. idly'),
 (5, 108569283, 8569284, 1, 15.00, 20202.90, 0.02, 0.04, 'R', 'F', '1994-10-31', '1994-08-31', '1994-11-20', 'NONE', 'AIR', 'ts wake furiously '),
 (5, 123926789, 3926790, 2, 26.00, 47049.34, 0.07, 0.08, 'R', 'F', '1994-10-16', '1994-09-25', '1994-10-19', 'NONE', 'FOB', 'sts use slyly quickly special instruc'),
 (5, 37530180, 30184, 3, 50.00, 60415.50, 0.08, 0.03, 'A', 'F', '1994-08-08', '1994-10-13', '1994-08-26', 'DELIVER IN PERSON', 'AIR', 'eodolites. fluffily unusual'),
 (6, 139635455, 2135469, 1, 37.00, 51188.39, 0.08, 0.03, 'A', 'F', '1992-04-27', '1992-05-15', '1992-05-02', 'TAKE BACK RETURN', 'TRUCK', 'p furiously special foxes'),
 (7, 182051839, 9551894, 1, 12.00, 21380.76, 0.07, 0.03, 'N', 'O', '1996-05-07', '1996-03-13', '1996-06-03', 'TAKE BACK RETURN', 'FOB', 'ss pinto beans wake against th'),
 (7, 145242743, 7742758, 2, 9.00, 15106.32, 0.08, 0.08, 'N', 'O', '1996-02-01', '1996-03-02', '1996-02-19', 'TAKE BACK RETURN', 'SHIP', 'es. instructions'),
 (7, 94779739, 9779758, 3, 46.00, 83444.00, 0.10, 0.07, 'N', 'O', '1996-01-15', '1996-03-27', '1996-02-03', 'COLLECT COD', 'MAIL', ' unusual reques'),
 (7, 163072047, 3072048, 4, 28.00, 28304.92, 0.03, 0.04, 'N', 'O', '1996-03-21', '1996-04-08', '1996-04-20', 'NONE', 'FOB', '. slyly special requests haggl'),
 (7, 151893810, 9393856, 5, 38.00, 68256.36, 0.08, 0.01, 'N', 'O', '1996-02-11', '1996-02-24', '1996-02-18', 'DELIVER IN PERSON', 'TRUCK', 'ns haggle carefully ironic deposits. bl'),
 (7, 79250148, 1750156, 6, 35.00, 38296.30, 0.06, 0.03, 'N', 'O', '1996-01-16', '1996-02-23', '1996-01-22', 'TAKE BACK RETURN', 'FOB', 'jole. excuses wake carefully alongside of '),
 (7, 157237027, 2237058, 7, 5.00, 4780.80, 0.04, 0.02, 'N', 'O', '1996-02-10', '1996-03-26', '1996-02-13', 'NONE', 'FOB', 'ithely regula'),
 (32, 82703512, 7703529, 1, 28.00, 42318.64, 0.05, 0.08, 'N', 'O', '1995-10-23', '1995-08-27', '1995-10-26', 'TAKE BACK RETURN', 'TRUCK', 'sleep quickly. req'),
 (32, 197920162, 420182, 2, 32.00, 37512.64, 0.02, 0.00, 'N', 'O', '1995-08-14', '1995-10-07', '1995-08-27', 'COLLECT COD', 'AIR', 'lithely regular deposits. fluffily '),
 (32, 44160335, 6660340, 3, 2.00, 2786.26, 0.09, 0.02, 'N', 'O', '1995-08-07', '1995-10-07', '1995-08-23', 'DELIVER IN PERSON', 'AIR', ' express accounts wake according to the'),
 (32, 2742061, 7742062, 4, 4.00, 4411.72, 0.09, 0.03, 'N', 'O', '1995-08-04', '1995-10-01', '1995-09-03', 'NONE', 'REG AIR', 'e slyly final pac'),
 (32, 85810176, 8310185, 5, 44.00, 47602.72, 0.05, 0.06, 'N', 'O', '1995-08-28', '1995-08-20', '1995-09-14', 'DELIVER IN PERSON', 'AIR', 'symptotes nag according to the ironic depo'),
 (32, 11614679, 4114681, 6, 6.00, 9558.54, 0.04, 0.03, 'N', 'O', '1995-07-21', '1995-09-23', '1995-07-25', 'COLLECT COD', 'RAIL', ' gifts cajole carefully.'),
 (33, 61335189, 8835208, 1, 31.00, 37854.72, 0.09, 0.04, 'A', 'F', '1993-10-29', '1993-12-19', '1993-11-08', 'COLLECT COD', 'TRUCK', 'ng to the furiously ironic package'),
 (33, 60518681, 5518694, 2, 32.00, 54293.12, 0.02, 0.05, 'A', 'F', '1993-12-09', '1994-01-04', '1993-12-28', 'COLLECT COD', 'MAIL', 'gular theodolites'),
 (33, 137468550, 9968564, 3, 5.00, 7558.40, 0.05, 0.03, 'A', 'F', '1993-12-09', '1993-12-25', '1993-12-23', 'TAKE BACK RETURN', 'AIR', '. stealthily bold exc'),
 (33, 33917488, 3917489, 4, 41.00, 61655.39, 0.09, 0.00, 'R', 'F', '1993-11-09', '1994-01-24', '1993-11-11', 'TAKE BACK RETURN', 'MAIL', 'unusual packages doubt caref'),
 (34, 88361363, 861372, 1, 13.00, 18459.35, 0.00, 0.07, 'N', 'O', '1998-10-23', '1998-09-14', '1998-11-06', 'NONE', 'REG AIR', 'nic accounts. deposits are alon'),
 (34, 89413313, 1913322, 2, 22.00, 26880.48, 0.08, 0.06, 'N', 'O', '1998-10-09', '1998-10-16', '1998-10-12', 'NONE', 'FOB', 'thely slyly p'),
 (34, 169543048, 4543081, 3, 6.00, 6495.42, 0.02, 0.06, 'N', 'O', '1998-10-30', '1998-09-20', '1998-11-05', 'NONE', 'FOB', 'ar foxes sleep '),
 (35, 449928, 2949929, 1, 24.00, 45069.60, 0.02, 0.00, 'N', 'O', '1996-02-21', '1996-01-03', '1996-03-18', 'TAKE BACK RETURN', 'FOB', ', regular tithe'),
 (35, 161939722, 4439739, 2, 34.00, 59623.42, 0.06, 0.08, 'N', 'O', '1996-01-22', '1996-01-06', '1996-01-27', 'DELIVER IN PERSON', 'RAIL', 's are carefully against the f'),
 (35, 120895174, 8395211, 3, 7.00, 8141.91, 0.06, 0.04, 'N', 'O', '1996-01-19', '1995-12-22', '1996-01-29', 'NONE', 'MAIL', ' the carefully regular '),
 (35, 85174030, 7674039, 4, 25.00, 27494.50, 0.06, 0.05, 'N', 'O', '1995-11-26', '1995-12-25', '1995-12-21', 'DELIVER IN PERSON', 'SHIP', ' quickly unti'),
 (35, 119916152, 4916175, 5, 34.00, 39513.44, 0.08, 0.06, 'N', 'O', '1995-11-08', '1996-01-15', '1995-11-26', 'COLLECT COD', 'MAIL', '. silent, unusual deposits boost'),
 (35, 30761725, 3261729, 6, 28.00, 49985.32, 0.03, 0.02, 'N', 'O', '1996-02-01', '1995-12-24', '1996-02-28', 'COLLECT COD', 'RAIL', 'ly alongside of '),
 (36, 119766448, 9766449, 1, 42.00, 63355.32, 0.09, 0.00, 'N', 'O', '1996-02-03', '1996-01-21', '1996-02-23', 'COLLECT COD', 'SHIP', ' careful courts. special '),
 (37, 22629071, 5129074, 1, 40.00, 39957.60, 0.09, 0.03, 'A', 'F', '1992-07-21', '1992-08-01', '1992-08-15', 'NONE', 'REG AIR', 'luffily regular requests. slyly final acco'),
 (37, 126781276, 1781301, 2, 39.00, 52686.66, 0.05, 0.02, 'A', 'F', '1992-07-02', '1992-08-18', '1992-07-28', 'TAKE BACK RETURN', 'RAIL', 'the final requests. ca'),
 (37, 12902948, 5402950, 3, 43.00, 83862.90, 0.05, 0.08, 'A', 'F', '1992-07-10', '1992-07-06', '1992-08-02', 'DELIVER IN PERSON', 'TRUCK', 'iously ste'),
 (38, 175838801, 838836, 1, 44.00, 76164.44, 0.04, 0.02, 'N', 'O', '1996-09-29', '1996-11-17', '1996-09-30', 'COLLECT COD', 'MAIL', 's. blithely unusual theodolites am'),
 (39, 2319664, 9819665, 1, 44.00, 74076.20, 0.09, 0.06, 'N', 'O', '1996-11-14', '1996-12-15', '1996-12-12', 'COLLECT COD', 'RAIL', 'eodolites. careful'),
 (39, 186581058, 4081113, 2, 26.00, 29372.98, 0.08, 0.04, 'N', 'O', '1996-11-04', '1996-10-20', '1996-11-20', 'NONE', 'FOB', 'ckages across the slyly silent'),
 (39, 67830106, 5330125, 3, 46.00, 47504.66, 0.06, 0.08, 'N', 'O', '1996-09-26', '1996-12-19', '1996-10-26', 'DELIVER IN PERSON', 'AIR', 'he carefully e'),
 (39, 20589905, 3089908, 4, 32.00, 63804.16, 0.07, 0.05, 'N', 'O', '1996-10-02', '1996-12-19', '1996-10-14', 'COLLECT COD', 'MAIL', 'heodolites sleep silently pending foxes. ac'),
 (39, 54518616, 9518627, 5, 43.00, 70171.27, 0.01, 0.01, 'N', 'O', '1996-10-17', '1996-11-14', '1996-10-26', 'COLLECT COD', 'MAIL', 'yly regular i'),
 (39, 94367239, 6867249, 6, 40.00, 52060.80, 0.06, 0.05, 'N', 'O', '1996-12-08', '1996-10-22', '1997-01-01', 'COLLECT COD', 'AIR', 'quickly ironic fox'),
 (64, 85950874, 5950875, 1, 21.00, 40332.18, 0.05, 0.02, 'R', 'F', '1994-09-30', '1994-09-18', '1994-10-26', 'DELIVER IN PERSON', 'REG AIR', 'ch slyly final, thin platelets.'),
 (65, 59693808, 4693819, 1, 26.00, 46769.32, 0.03, 0.03, 'A', 'F', '1995-04-20', '1995-04-25', '1995-05-13', 'NONE', 'TRUCK', 'pending deposits nag even packages. ca'),
 (65, 73814565, 8814580, 2, 22.00, 32469.14, 0.00, 0.05, 'N', 'O', '1995-07-17', '1995-06-04', '1995-07-19', 'COLLECT COD', 'FOB', ' ideas. special, r'),
 (65, 1387319, 3887320, 3, 21.00, 29531.25, 0.09, 0.07, 'N', 'O', '1995-07-06', '1995-05-14', '1995-07-31', 'DELIVER IN PERSON', 'RAIL', 'bove the even packages. accounts nag carefu'),
 (66, 115117124, 7617136, 1, 31.00, 35196.47, 0.00, 0.08, 'R', 'F', '1994-02-19', '1994-03-11', '1994-02-20', 'TAKE BACK RETURN', 'RAIL', 'ut the unusual accounts sleep at the bo'),
 (66, 173488357, 3488358, 2, 41.00, 54803.88, 0.04, 0.07, 'A', 'F', '1994-02-21', '1994-03-01', '1994-03-18', 'COLLECT COD', 'AIR', ' regular de'),
 (67, 21635045, 9135052, 1, 4.00, 3915.84, 0.09, 0.04, 'N', 'O', '1997-04-17', '1997-01-31', '1997-04-20', 'NONE', 'SHIP', ' cajole thinly expres'),
 (67, 20192396, 5192401, 2, 12.00, 17848.68, 0.09, 0.05, 'N', 'O', '1997-01-27', '1997-02-21', '1997-02-22', 'NONE', 'REG AIR', ' even packages cajole'),
 (67, 173599543, 6099561, 3, 5.00, 8169.35, 0.03, 0.07, 'N', 'O', '1997-02-20', '1997-02-12', '1997-02-21', 'DELIVER IN PERSON', 'TRUCK', 'y unusual packages thrash pinto '),
 (67, 87513573, 7513574, 4, 44.00, 69616.80, 0.08, 0.06, 'N', 'O', '1997-03-18', '1997-01-29', '1997-04-13', 'DELIVER IN PERSON', 'RAIL', 'se quickly above the even, express reques'),
 (67, 40612740, 8112753, 5, 23.00, 37966.33, 0.05, 0.07, 'N', 'O', '1997-04-19', '1997-02-14', '1997-05-06', 'DELIVER IN PERSON', 'REG AIR', 'ly regular deposit'),
 (67, 178305451, 805469, 6, 29.00, 41978.66, 0.02, 0.05, 'N', 'O', '1997-01-25', '1997-01-27', '1997-01-27', 'DELIVER IN PERSON', 'FOB', 'ultipliers '),
 (68, 7067007, 9567008, 1, 3.00, 2920.95, 0.05, 0.02, 'N', 'O', '1998-07-04', '1998-06-05', '1998-07-21', 'NONE', 'RAIL', 'fully special instructions cajole. furious'),
 (68, 175179091, 2679143, 2, 46.00, 53421.64, 0.02, 0.05, 'N', 'O', '1998-06-26', '1998-06-07', '1998-07-05', 'NONE', 'MAIL', ' requests are unusual, regular pinto '),
 (68, 34979160, 7479164, 3, 46.00, 56921.32, 0.04, 0.05, 'N', 'O', '1998-08-13', '1998-07-08', '1998-08-29', 'NONE', 'RAIL', 'egular dependencies affix ironically along '),
 (68, 94727362, 2227390, 4, 20.00, 27692.60, 0.07, 0.01, 'N', 'O', '1998-06-27', '1998-05-23', '1998-07-02', 'NONE', 'REG AIR', ' excuses integrate fluffily '),
 (68, 82757337, 5257346, 5, 27.00, 37535.40, 0.03, 0.06, 'N', 'O', '1998-06-19', '1998-06-25', '1998-06-29', 'DELIVER IN PERSON', 'SHIP', 'ccounts. deposits use. furiously'),
 (68, 102560793, 5060804, 6, 30.00, 55460.10, 0.05, 0.06, 'N', 'O', '1998-08-11', '1998-07-11', '1998-08-14', 'NONE', 'RAIL', 'oxes are slyly blithely fin'),
 (68, 139246458, 1746472, 7, 41.00, 57297.09, 0.09, 0.08, 'N', 'O', '1998-06-24', '1998-06-27', '1998-07-06', 'NONE', 'SHIP', 'eposits nag special ideas. furiousl'),
 (69, 115208198, 7708210, 1, 48.00, 52820.64, 0.01, 0.07, 'A', 'F', '1994-08-17', '1994-08-11', '1994-09-08', 'NONE', 'TRUCK', 'regular epitaphs. carefully even ideas hag'),
 (69, 104179049, 9179070, 2, 32.00, 35930.88, 0.08, 0.06, 'A', 'F', '1994-08-24', '1994-08-17', '1994-08-31', 'NONE', 'REG AIR', 's sleep carefully bold, '),
 (69, 137266467, 4766507, 3, 17.00, 24252.20, 0.09, 0.00, 'A', 'F', '1994-07-02', '1994-07-07', '1994-07-03', 'TAKE BACK RETURN', 'AIR', 'final, pending instr'),
 (69, 37501760, 2501767, 4, 3.00, 5279.67, 0.09, 0.04, 'R', 'F', '1994-06-06', '1994-07-27', '1994-06-15', 'NONE', 'MAIL', ' blithely final d'),
 (69, 92069882, 7069901, 5, 42.00, 77585.76, 0.07, 0.04, 'R', 'F', '1994-07-31', '1994-07-26', '1994-08-28', 'DELIVER IN PERSON', 'REG AIR', 'tect regular, speci'),
 (69, 18503830, 1003832, 6, 23.00, 42156.93, 0.05, 0.00, 'A', 'F', '1994-10-03', '1994-08-06', '1994-10-24', 'NONE', 'SHIP', 'nding accounts ca'),
 (70, 64127814, 9127827, 1, 8.00, 14708.88, 0.03, 0.08, 'R', 'F', '1994-01-12', '1994-02-27', '1994-01-14', 'TAKE BACK RETURN', 'FOB', 'ggle. carefully pending dependenc'),
 (70, 196155163, 1155202, 2, 13.00, 15708.68, 0.06, 0.06, 'A', 'F', '1994-03-03', '1994-02-13', '1994-03-26', 'COLLECT COD', 'AIR', 'lyly special packag'),
 (70, 179808755, 7308807, 3, 1.00, 1854.77, 0.03, 0.05, 'R', 'F', '1994-01-26', '1994-03-05', '1994-01-28', 'TAKE BACK RETURN', 'RAIL', 'quickly. fluffily unusual theodolites c'),
 (70, 45733155, 733164, 4, 11.00, 13044.57, 0.01, 0.05, 'A', 'F', '1994-03-17', '1994-03-17', '1994-03-27', 'NONE', 'MAIL', 'alongside of the deposits. fur'),
 (70, 37130699, 2130706, 5, 37.00, 63930.08, 0.09, 0.04, 'R', 'F', '1994-02-13', '1994-03-16', '1994-02-21', 'COLLECT COD', 'MAIL', 'n accounts are. q'),
 (70, 55654148, 3154164, 6, 19.00, 20887.84, 0.06, 0.03, 'A', 'F', '1994-01-26', '1994-02-17', '1994-02-06', 'TAKE BACK RETURN', 'SHIP', ' packages wake pending accounts.'),
 (71, 61930501, 1930502, 1, 25.00, 38210.25, 0.09, 0.07, 'N', 'O', '1998-04-10', '1998-04-22', '1998-04-11', 'COLLECT COD', 'FOB', 'ckly. slyly'),
 (71, 65915062, 3415081, 2, 3.00, 3221.31, 0.09, 0.07, 'N', 'O', '1998-05-23', '1998-04-03', '1998-06-02', 'COLLECT COD', 'SHIP', 'y. pinto beans haggle after the'),
 (71, 34431883, 1931893, 3, 45.00, 81592.20, 0.00, 0.07, 'N', 'O', '1998-02-23', '1998-03-20', '1998-03-24', 'DELIVER IN PERSON', 'SHIP', ' ironic packages believe blithely a'),
 (71, 96644449, 9144459, 4, 33.00, 45824.13, 0.00, 0.01, 'N', 'O', '1998-04-12', '1998-03-20', '1998-04-15', 'NONE', 'FOB', ' serve quickly fluffily bold deposi'),
 (71, 103254337, 5754348, 5, 39.00, 50160.63, 0.08, 0.06, 'N', 'O', '1998-01-29', '1998-04-07', '1998-02-18', 'DELIVER IN PERSON', 'RAIL', 'l accounts sleep across the pack'),
 (71, 195634217, 634256, 6, 34.00, 38808.62, 0.04, 0.01, 'N', 'O', '1998-03-05', '1998-04-22', '1998-03-30', 'DELIVER IN PERSON', 'TRUCK', 's cajole. '),
 (96, 123075825, 575862, 1, 23.00, 41277.41, 0.10, 0.06, 'A', 'F', '1994-07-19', '1994-06-29', '1994-07-25', 'DELIVER IN PERSON', 'TRUCK', 'ep-- carefully reg'),
 (96, 135389770, 5389771, 2, 30.00, 55590.30, 0.01, 0.06, 'R', 'F', '1994-06-03', '1994-05-29', '1994-06-22', 'DELIVER IN PERSON', 'TRUCK', 'e quickly even ideas. furiou'),
 (97, 119476978, 1976990, 1, 13.00, 25337.00, 0.00, 0.02, 'R', 'F', '1993-04-01', '1993-04-04', '1993-04-08', 'NONE', 'TRUCK', 'ayers cajole against the furiously'),
 (97, 49567306, 2067311, 2, 37.00, 50720.71, 0.02, 0.06, 'A', 'F', '1993-04-13', '1993-03-30', '1993-04-14', 'DELIVER IN PERSON', 'SHIP', 'ic requests boost carefully quic'),
 (97, 77698944, 5198966, 3, 19.00, 36842.14, 0.06, 0.08, 'R', 'F', '1993-05-14', '1993-03-05', '1993-05-25', 'TAKE BACK RETURN', 'RAIL', 'gifts. furiously ironic packages cajole. '),
 (98, 40215967, 215968, 1, 28.00, 52666.60, 0.06, 0.07, 'A', 'F', '1994-12-24', '1994-10-25', '1995-01-16', 'COLLECT COD', 'REG AIR', ' pending, regular accounts s'),
 (98, 109742650, 7242681, 2, 1.00, 1687.17, 0.00, 0.00, 'A', 'F', '1994-12-01', '1994-12-12', '1994-12-15', 'DELIVER IN PERSON', 'TRUCK', '. unusual instructions against'),
 (98, 44705610, 4705611, 3, 14.00, 22587.32, 0.05, 0.02, 'A', 'F', '1994-12-30', '1994-11-22', '1995-01-27', 'COLLECT COD', 'AIR', ' cajole furiously. blithely ironic ideas '),
 (98, 167179412, 7179413, 4, 10.00, 14830.60, 0.03, 0.03, 'A', 'F', '1994-10-23', '1994-11-08', '1994-11-09', 'COLLECT COD', 'RAIL', ' carefully. quickly ironic ideas'),
 (99, 87113927, 4613952, 1, 10.00, 19365.70, 0.02, 0.01, 'A', 'F', '1994-05-18', '1994-06-03', '1994-05-23', 'COLLECT COD', 'RAIL', 'kages. requ'),
 (99, 123765936, 3765937, 2, 5.00, 9978.75, 0.02, 0.07, 'R', 'F', '1994-05-06', '1994-05-28', '1994-05-20', 'TAKE BACK RETURN', 'RAIL', 'ests cajole fluffily waters. blithe'),
 (99, 134081534, 1581574, 3, 42.00, 63370.86, 0.02, 0.02, 'A', 'F', '1994-04-19', '1994-05-18', '1994-04-20', 'NONE', 'RAIL', 'kages are fluffily furiously ir'),
 (99, 108337010, 837021, 4, 36.00, 37497.60, 0.09, 0.02, 'A', 'F', '1994-07-04', '1994-04-17', '1994-07-30', 'DELIVER IN PERSON', 'AIR', 'slyly. slyly e'),
 (100, 62028678, 2028679, 1, 28.00, 44899.96, 0.04, 0.05, 'N', 'O', '1998-05-08', '1998-05-13', '1998-06-07', 'COLLECT COD', 'TRUCK', 'sts haggle. slowl'),
 (100, 115978233, 8478245, 2, 22.00, 28719.68, 0.00, 0.07, 'N', 'O', '1998-06-24', '1998-04-12', '1998-06-29', 'DELIVER IN PERSON', 'SHIP', 'nto beans alongside of the fi'),
 (100, 46149701, 8649706, 3, 46.00, 80426.40, 0.03, 0.04, 'N', 'O', '1998-05-02', '1998-04-10', '1998-05-22', 'TAKE BACK RETURN', 'SHIP', 'ular accounts. even'),
 (100, 38023053, 3023060, 4, 14.00, 13638.10, 0.06, 0.03, 'N', 'O', '1998-05-22', '1998-05-01', '1998-06-03', 'COLLECT COD', 'MAIL', 'y. furiously ironic ideas gr'),
 (100, 53438259, 938275, 5, 37.00, 44199.46, 0.05, 0.00, 'N', 'O', '1998-03-06', '1998-04-16', '1998-03-31', 'TAKE BACK RETURN', 'TRUCK', 'nd the quickly s'),
 (101, 118281867, 5781901, 1, 49.00, 90304.55, 0.10, 0.00, 'N', 'O', '1996-06-21', '1996-05-27', '1996-06-29', 'DELIVER IN PERSON', 'REG AIR', 'ts-- final packages sleep furiousl'),
 (101, 163333041, 833090, 2, 36.00, 38371.68, 0.00, 0.01, 'N', 'O', '1996-05-19', '1996-05-01', '1996-06-04', 'DELIVER IN PERSON', 'AIR', 'tes. blithely pending dolphins x-ray f'),
 (101, 138417252, 5917292, 3, 12.00, 13947.96, 0.06, 0.02, 'N', 'O', '1996-03-29', '1996-04-20', '1996-04-12', 'COLLECT COD', 'MAIL', '. quickly regular'),
 (102, 88913503, 3913520, 1, 37.00, 55946.22, 0.06, 0.00, 'N', 'O', '1997-07-24', '1997-08-02', '1997-08-07', 'TAKE BACK RETURN', 'SHIP', 'ully across the ideas. final deposit'),
 (102, 169237956, 6738005, 2, 34.00, 64106.66, 0.03, 0.08, 'N', 'O', '1997-08-09', '1997-07-28', '1997-08-26', 'TAKE BACK RETURN', 'SHIP', 'eposits cajole across'),
 (102, 182320531, 4820550, 3, 25.00, 38560.50, 0.01, 0.01, 'N', 'O', '1997-07-31', '1997-07-24', '1997-08-17', 'NONE', 'RAIL', 'bits. ironic accoun'),
 (102, 61157984, 8658003, 4, 15.00, 30583.95, 0.07, 0.07, 'N', 'O', '1997-06-02', '1997-07-13', '1997-06-04', 'DELIVER IN PERSON', 'SHIP', 'final packages. carefully even excu'),
 (103, 194657609, 2157667, 1, 6.00, 9341.22, 0.03, 0.05, 'N', 'O', '1996-10-11', '1996-07-25', '1996-10-28', 'NONE', 'FOB', 'cajole. carefully ex'),
 (103, 10425920, 2925922, 2, 37.00, 68279.80, 0.02, 0.07, 'N', 'O', '1996-09-17', '1996-07-27', '1996-09-20', 'TAKE BACK RETURN', 'MAIL', 'ies. quickly ironic requests use blithely'),
 (103, 28430358, 8430359, 3, 23.00, 29599.39, 0.01, 0.04, 'N', 'O', '1996-09-11', '1996-09-18', '1996-09-26', 'NONE', 'FOB', 'ironic accou'),
 (103, 29021558, 4021563, 4, 32.00, 47299.20, 0.01, 0.07, 'N', 'O', '1996-07-30', '1996-08-06', '1996-08-04', 'NONE', 'RAIL', 'kages doze. special, regular deposit'),
 (128, 106827451, 9327462, 1, 38.00, 52178.18, 0.06, 0.01, 'A', 'F', '1992-09-01', '1992-08-27', '1992-10-01', 'TAKE BACK RETURN', 'FOB', ' cajole careful'),
 (129, 2866970, 5366971, 1, 46.00, 89094.18, 0.08, 0.02, 'R', 'F', '1993-02-15', '1993-01-24', '1993-03-05', 'COLLECT COD', 'TRUCK', 'uietly bold theodolites. fluffil'),
 (129, 185163292, 5163293, 2, 36.00, 48457.44, 0.01, 0.02, 'A', 'F', '1992-11-25', '1992-12-25', '1992-12-09', 'TAKE BACK RETURN', 'REG AIR', 'packages are care'),
 (129, 39443990, 1943994, 3, 33.00, 63756.66, 0.04, 0.06, 'A', 'F', '1993-01-08', '1993-02-14', '1993-01-29', 'COLLECT COD', 'SHIP', 'sts nag bravely. fluffily'),
 (129, 135136037, 136064, 4, 34.00, 36253.52, 0.00, 0.01, 'R', 'F', '1993-01-29', '1993-02-14', '1993-02-10', 'COLLECT COD', 'MAIL', 'quests. express ideas'),
 (129, 31372467, 8872477, 5, 24.00, 36909.60, 0.06, 0.00, 'A', 'F', '1992-12-07', '1993-01-02', '1992-12-11', 'TAKE BACK RETURN', 'FOB', 'uests. foxes cajole slyly after the ca'),
 (129, 77049359, 4549381, 6, 22.00, 28699.00, 0.06, 0.01, 'R', 'F', '1993-02-15', '1993-01-31', '1993-02-24', 'COLLECT COD', 'SHIP', 'e. fluffily regular '),
 (129, 168568384, 3568417, 7, 1.00, 1443.96, 0.05, 0.04, 'R', 'F', '1993-01-26', '1993-01-08', '1993-02-24', 'DELIVER IN PERSON', 'FOB', 'e carefully blithely bold dolp'),
 (130, 128815478, 8815479, 1, 14.00, 19418.42, 0.08, 0.05, 'A', 'F', '1992-08-15', '1992-07-25', '1992-09-13', 'COLLECT COD', 'RAIL', ' requests. final instruction'),
 (130, 1738077, 4238078, 2, 48.00, 53519.52, 0.03, 0.02, 'R', 'F', '1992-07-01', '1992-07-12', '1992-07-24', 'NONE', 'AIR', 'lithely alongside of the regu'),
 (130, 11859085, 1859086, 3, 18.00, 18782.82, 0.04, 0.08, 'A', 'F', '1992-07-04', '1992-06-14', '1992-07-29', 'DELIVER IN PERSON', 'MAIL', ' slyly ironic decoys abou'),
 (130, 115634506, 3134540, 4, 13.00, 18651.36, 0.09, 0.02, 'R', 'F', '1992-06-26', '1992-07-29', '1992-07-05', 'NONE', 'FOB', ' pending dolphins sleep furious'),
 (130, 69129320, 4129333, 5, 31.00, 41721.97, 0.06, 0.05, 'R', 'F', '1992-09-01', '1992-07-18', '1992-09-02', 'TAKE BACK RETURN', 'RAIL', 'thily about the ruth'),
 (131, 167504270, 4287, 1, 45.00, 56965.50, 0.10, 0.02, 'R', 'F', '1994-09-14', '1994-09-02', '1994-10-04', 'NONE', 'FOB', 'ironic, bold accounts. careful'),
 (131, 44254717, 9254726, 2, 50.00, 83475.00, 0.02, 0.04, 'A', 'F', '1994-09-17', '1994-08-10', '1994-09-21', 'NONE', 'SHIP', 'ending requests. final, ironic pearls slee'),
 (131, 189020323, 1520342, 3, 4.00, 4935.48, 0.04, 0.03, 'A', 'F', '1994-09-20', '1994-08-30', '1994-09-23', 'COLLECT COD', 'REG AIR', ' are carefully slyly i'),
 (132, 140448567, 2948582, 1, 18.00, 27153.72, 0.00, 0.08, 'R', 'F', '1993-07-10', '1993-08-05', '1993-07-13', 'NONE', 'TRUCK', 'ges. platelets wake furio'),
 (132, 119052444, 9052445, 2, 43.00, 59791.07, 0.01, 0.08, 'R', 'F', '1993-09-01', '1993-08-16', '1993-09-22', 'NONE', 'TRUCK', 'y pending theodolites'),
 (132, 114418283, 4418284, 3, 32.00, 38257.92, 0.04, 0.04, 'A', 'F', '1993-07-12', '1993-08-05', '1993-08-05', 'COLLECT COD', 'TRUCK', 'd instructions hagg'),
 (132, 28081909, 5581916, 4, 23.00, 43458.50, 0.10, 0.00, 'A', 'F', '1993-06-16', '1993-08-27', '1993-06-23', 'DELIVER IN PERSON', 'AIR', 'refully blithely bold acco'),
 (133, 103431682, 5931693, 1, 27.00, 43429.77, 0.00, 0.02, 'N', 'O', '1997-12-21', '1998-02-23', '1997-12-27', 'TAKE BACK RETURN', 'MAIL', 'yly even gifts after the sl'),
 (133, 176278774, 3778826, 2, 12.00, 20927.52, 0.02, 0.06, 'N', 'O', '1997-12-02', '1998-01-15', '1997-12-29', 'DELIVER IN PERSON', 'REG AIR', 'ts cajole fluffily quickly i'),
 (133, 117349311, 4849345, 3, 29.00, 39279.05, 0.09, 0.08, 'N', 'O', '1998-02-28', '1998-01-30', '1998-03-09', 'DELIVER IN PERSON', 'RAIL', ' the carefully regular theodoli'),
 (133, 89854644, 7354669, 4, 11.00, 17535.65, 0.06, 0.01, 'N', 'O', '1998-03-21', '1998-01-15', '1998-04-04', 'DELIVER IN PERSON', 'REG AIR', 'e quickly across the dolphins'),
 (134, 640486, 640487, 1, 21.00, 29955.45, 0.00, 0.03, 'A', 'F', '1992-07-17', '1992-07-08', '1992-07-26', 'COLLECT COD', 'SHIP', 's. quickly regular'),
 (134, 164644985, 9645018, 2, 35.00, 67261.25, 0.06, 0.07, 'A', 'F', '1992-08-23', '1992-06-01', '1992-08-24', 'NONE', 'MAIL', 'ajole furiously. instructio'),
 (134, 188251562, 3251599, 3, 26.00, 39107.90, 0.09, 0.06, 'A', 'F', '1992-06-20', '1992-07-12', '1992-07-16', 'NONE', 'RAIL', ' among the pending depos'),
 (134, 144001617, 4001618, 4, 47.00, 80436.74, 0.05, 0.00, 'A', 'F', '1992-08-16', '1992-07-06', '1992-08-28', 'NONE', 'REG AIR', 's! carefully unusual requests boost careful'),
 (134, 35171840, 5171841, 5, 12.00, 22921.08, 0.05, 0.02, 'A', 'F', '1992-07-03', '1992-06-01', '1992-07-11', 'COLLECT COD', 'TRUCK', 'nts are quic');
