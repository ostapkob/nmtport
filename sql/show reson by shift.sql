/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000)
      [inv_num]
      ,[data_smen]
      ,[smena]
      ,[data_nach]
      ,[data_kon]
      ,[id_downtime]
	  ,name
FROM [nmtport].[dbo].[mechanism_downtime_1C]
JOIN Downtime ON mechanism_downtime_1C.id_downtime=Downtime.id
WHERE
  inv_num in(SELECT id from mechanism WHERE type = 'usm' and number=13) 
  and
  data_smen=CONVERT(datetime, '2022-08-25 00:00:00', 120) 
  and
  smena = 2