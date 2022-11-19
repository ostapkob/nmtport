SELECT TOP (10)
       [number]
      ,[greifer_num]
      ,[greifer_vol]
      ,[fio]
      ,[data_nach]
      ,[data_kon]
      ,[port]

  FROM Work_1C_1 JOIN mechanism ON Work_1C_1.inv_num=mechanism.id
  where 
  inv_num in(SELECT id from mechanism WHERE type = 'kran' and number=23) 
  ORDER BY data_smen DESC
