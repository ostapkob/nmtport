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
  FROM [nmtport].[dbo].[Work_1C_1]
    where inv_num=33297
	  order by data_smen desc
