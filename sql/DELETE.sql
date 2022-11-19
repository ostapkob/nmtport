DELETE
--SELECT TOP (1000) [id],  [timestamp]
  FROM [nmtport].[dbo].[post]
  where mechanism_id in(SELECT id from mechanism WHERE type = 'usm' and number=7)
  and  date_shift='2022-08-25' 
  and shift=1
