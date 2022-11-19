/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (10) [id]
      ,[mechanism_id]
      ,[latitude]
      ,[longitude]
      ,[value]
      ,[value2]
      ,[value3]
      ,[count]
      ,[timestamp]
      ,[date_shift]
      ,[shift]
      ,[terminal]
  FROM [nmtport].[dbo].[post]
  where mechanism_id in(SELECT id from mechanism WHERE type = 'kran' and number=31)
  ORDER BY timestamp DESC