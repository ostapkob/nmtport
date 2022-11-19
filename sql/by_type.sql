/****** Script for SelectTopNRows command from SSMS ******/
SELECT TOP (1000) 
      [mechanism_id]
	  ,count (value) Count
  FROM [nmtport].[dbo].[post]
  where mechanism_id in(SELECT id from mechanism WHERE type = 'usm')
  and shift=1 
  and date_shift='2022-07-12'
  GROUP BY [mechanism_id] 
