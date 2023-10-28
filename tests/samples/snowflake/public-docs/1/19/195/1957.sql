show channels;
select SYSTEM$SNOWPIPE_STREAMING_UPDATE_CHANNEL_OFFSET_TOKEN('mydb.myschema.mytable', 'mychannel', '<new_offset_token>');
show channels;