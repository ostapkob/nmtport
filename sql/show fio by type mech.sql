/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000)
       [number]
      ,[greifer_num]
      ,[greifer_vol]
      ,[fio]
      ,[data_nach]
      ,[data_kon]
      ,[port]

  FROM Work_1C_1 JOIN mechanism ON Work_1C_1.inv_num=mechanism.id
  where 
  inv_num in(SELECT id from mechanism WHERE type = 'kran') 
  and
  data_smen=CONVERT(datetime, '2022-08-26 00:00:00', 120) 
  and
  smena = 1