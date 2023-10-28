SELECT uniform(0::float, 1::float, random()) FROM table(generator(rowCount => 5));
