/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [id]
      ,[inv_num]
      ,[data_smen]
      ,[smena]
      ,[data_nach]
      ,[data_kon]
      ,[id_downtime]
      ,[ID_DOK_1C]
  FROM [nmtport].[dbo].[mechanism_downtime_1C]
    where 
  inv_num=4513
  and data_smen=CONVERT(datetime, '2022-07-07 00:00:00', 120) 
  and smena=1
  order by data_nach