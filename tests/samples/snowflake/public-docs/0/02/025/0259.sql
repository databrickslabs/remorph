SELECT zipf(1, 10, random()) FROM table(generator(rowCount => 10));
