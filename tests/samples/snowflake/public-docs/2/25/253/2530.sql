CREATE TABLE vartab (a ARRAY, o OBJECT, v VARIANT);
INSERT INTO vartab (a, o, v) 
  SELECT
    ARRAY_CONSTRUCT(2.71, 3.14),
    OBJECT_CONSTRUCT('Ukraine', 'Kyiv'::VARIANT, 
                     'France',  'Paris'::VARIANT),
    TO_VARIANT(OBJECT_CONSTRUCT('weatherStationID', 42::VARIANT,
                     'timestamp', '2022-03-07 14:00'::TIMESTAMP_LTZ::VARIANT,
                     'temperature', 31.5::VARIANT,
                     'sensorType', 'indoor'::VARIANT))
    ;