/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [id]
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
    WHERE 
 date_shift='2022-08-10' and
 mechanism_id =34213

