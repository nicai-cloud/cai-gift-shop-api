SELECT * FROM customer;
SELECT * FROM public.order;
SELECT * FROM order_item;

DELETE FROM customer;
DELETE FROM public.order;

SELECT * FROM bag;
SELECT * FROM item;
SELECT * FROM preselection;

INSERT INTO bag (id, image_url, name, description, size, price) VALUES (1, '/bag1', 'bag1', 'bag1 description', 'small', 10);
INSERT INTO bag (id, image_url, name, description, size, price) VALUES (2, '/bag2', 'bag2', 'bag2 description', 'medium', 15);

INSERT INTO item (id, image_url, name, description, price) VALUES (1, '/item1', 'item1', 'item1 description', 2);
INSERT INTO item (id, image_url, name, description, price) VALUES (2, '/item2', 'item2', 'item2 description', 1);
INSERT INTO item (id, image_url, name, description, price) VALUES (3, '/item3', 'item3', 'item3 description', 3);
INSERT INTO item (id, image_url, name, description, price) VALUES (4, '/item4', 'item4', 'item4 description', 1);
INSERT INTO item (id, image_url, name, description, price) VALUES (5, '/item5', 'item5', 'item5 description', 2);

INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (1, '/images/preselections/preselection1.webp', 'preselection1', 'Celebration Gift Pack (Person-alised)', 59, 1, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (2, '/images/preselections/preselection2.webp', 'preselection2', 'LOL OMG Gift Pack', 109, 1, '{3, 4, 5}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (3, '/images/preselections/preselection3.webp', 'preselection3', 'Fun Surprises Gift Pack', 109, 2, '{1, 2, 3}');
INSERT INTO preselection (id, image_url, name, description, price, bag_id, item_ids) VALUES (4, '/images/preselections/preselection4.png', 'preselection4', 'Squishmallow Surprise Gift Pack', 89, 2, '{1, 3, 5}');