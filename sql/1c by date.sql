/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [id]
      ,[inv_num]
      ,[greifer_num]
      ,[greifer_vol]
      ,[fio]
      ,[data_nach]
      ,[data_kon]
      ,[port]
      ,[data_smen]
      ,[smena]
      ,[ID_DOK_1C]
  FROM [nmtport].[dbo].[Work_1C_1]
  
  where 
  data_smen=CONVERT(datetime, '2022-07-05 00:00:00', 120) 
  and smena=1
  --inv_num=6574
  order by data_kon desc
  