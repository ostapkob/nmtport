/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (100) *
      ,[terminal]
  FROM [nmtport].[dbo].[post] 
  where mechanism_id=25390


  order by date_shift desc