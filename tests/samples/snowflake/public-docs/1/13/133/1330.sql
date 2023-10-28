SELECT * 
    FROM sounding_board AS board, sounding_bored AS bored 
    WHERE SOUNDEX(bored.v) = SOUNDEX(board.v);