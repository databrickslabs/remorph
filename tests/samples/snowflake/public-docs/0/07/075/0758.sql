SELECT randstr(abs(random()) % 10, random()) FROM table(generator(rowCount => 5));
