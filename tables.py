from datetime import datetime
current_timestamp = datetime.now()
items = 'CREATE TABLE items (id serial primary key, body text, created timestamp)'
item1 = 'INSERT INTO items VALUES (1, "body_1", current_timestamp)'