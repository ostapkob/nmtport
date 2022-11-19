/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) 
	 post.mechanism_id,
	 count(*) as Count
	 
  FROM  [nmtport].[dbo].[post]
  where mechanism_id=34213 or mechanism_id=34214 or mechanism_id=32770
  GROUP BY post.mechanism_id
