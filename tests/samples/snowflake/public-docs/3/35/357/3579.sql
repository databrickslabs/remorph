UPDATE my_table SET my_object = { 'Alberta': 'Edmonton' , 'Manitoba': 'Winnipeg' };

UPDATE my_table SET my_object = OBJECT_CONSTRUCT('Alberta', 'Edmonton', 'Manitoba', 'Winnipeg');