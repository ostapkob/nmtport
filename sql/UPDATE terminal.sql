/****** Script for SelectTopNRows command from SSMS  ******/
UPDATE post
SET terminal= 9
  WHERE 
  date_shift='2022-08-03' and
  shift=2 and 
  mechanism_id = 34214