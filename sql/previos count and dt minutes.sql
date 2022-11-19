SELECT *, DATEDIFF(minute, t.prev_time,  t.timestamp) dt_minutes FROM 
(
SELECT count, timestamp,
LAG(count) OVER(ORDER BY timestamp) as prev_count,
LAG(timestamp) OVER(ORDER BY timestamp) as prev_time
FROM post 
WHERE mechanism_id in(SELECT id from mechanism WHERE type = 'kran' and number=60) 
) t
WHERE t.count = 0
ORDER BY timestamp DESC
