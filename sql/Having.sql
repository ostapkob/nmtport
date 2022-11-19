/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (100) 
	  --mechanism.type
	  mechanism.name AS name
	  --,date_shift
      ,Count(value) AS Count
  FROM [nmtport].[dbo].[post]
  JOIN  mechanism ON mechanism.id = post.mechanism_id
  GROUP BY   mechanism.type, name, date_shift
  HAVING mechanism.type='usm'
  AND date_shift='2021-12-07'
 
  ORDER BY Count DESC
