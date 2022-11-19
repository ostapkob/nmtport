SELECT 
  f.number
  ,fio
  ,cnt

FROM

(
  SELECT 
    number
    ,fio
    ,data_smen
  FROM Work_1C_1 JOIN mechanism ON Work_1C_1.inv_num=mechanism.id
  where 
  inv_num in(SELECT id FROM mechanism WHERE type='kran') 
  AND data_smen=DATEADD(day, -1, CAST(GETDATE() AS date)) 
  AND smena=2
) f 

LEFT OUTER JOIN

(
  SELECT 
    number,
    COUNT(*) as cnt 
  FROM post JOIN mechanism ON post.mechanism_id=mechanism.id 
  WHERE mechanism_id IN(SELECT id FROM mechanism WHERE type='kran')
  AND shift=2 
  AND date_shift=DATEADD(day, -1, CAST(GETDATE() AS date)) 
  AND value>0
  GROUP BY number 
  HAVING COUNT(*) > 10
) v

ON v.number = f.number
