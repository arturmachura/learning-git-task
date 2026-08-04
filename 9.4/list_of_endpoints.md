Metoda	URL	                         Opis
GET	    /api/movies	                 lista filmów (alfa)
GET	    /api/movies/<id>	         jeden film
POST	/api/movies	                 dodaj film {title, year, genre}
DELETE	/api/movies/<id>	         usuń film
GET	    /api/series	                 lista odcinków (alfa + sezon + ep)
GET	    /api/series/<id>	         jeden odcinek
POST	/api/series	                 dodaj odcinek {title, year, genre, season, episode}
POST	/api/series/season	         dodaj cały sezon {..., episodes_count}
DELETE	/api/series/<id>	         usuń odcinek
POST	/api/play/<id>	             +1 odtworzenie
GET	    /api/top?count=5&type=movie	 top tytuły
GET	    /api/search?q=kiler	         szukaj po tytule