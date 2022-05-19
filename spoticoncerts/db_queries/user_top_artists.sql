SELECT 
	artist,
    count(*) as reproductions
FROM song
LEFT JOIN user
	ON song.user_id = user.id
WHERE user_id = :val
GROUP BY artist, username
ORDER BY reproductions DESC, artist 
LIMIT 25;