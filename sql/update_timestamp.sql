	--SELECT TOP (1000) [id],[timestamp], [date_shift], [shift], [value], [value3]	FROM [nmtport].[dbo].[post]
	--SELECT COUNT (*) FROM [nmtport].[dbo].[post]
	UPDATE post SET value=0.95, value3=25

   WHERE 
	--date_shift='2022-08-10' 
	mechanism_id=33287 and
	timestamp>CONVERT(datetime, '2022-08-12 17:07:00', 120) and 
	timestamp<CONVERT(datetime, '2022-08-12 17:14:00', 120)
