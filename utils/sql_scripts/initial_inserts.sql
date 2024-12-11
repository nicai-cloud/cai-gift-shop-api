SELECT * FROM customer;
SELECT * FROM order_item;
SELECT * FROM public.order;

DELETE FROM customer;
DELETE FROM order_item;
DELETE FROM public.order;

SELECT * FROM bag;
SELECT * FROM item;
SELECT * FROM preselection;

INSERT INTO bag (id, image_src, name, color, size, price) VALUES (1, '/bag1', 'bag1', 'blue', 'small', 10);
INSERT INTO bag (id, image_src, name, color, size, price) VALUES (2, '/bag2', 'bag2', 'yellow', 'medium', 10);

INSERT INTO item (id, image_src, name, price) VALUES (1, '/item1', 'car', 1);
INSERT INTO item (id, image_src, name, price) VALUES (2, '/item2', 'book', 1);
INSERT INTO item (id, image_src, name, price) VALUES (3, '/item3', 'candy', 1);
INSERT INTO item (id, image_src, name, price) VALUES (4, '/item4', 'sticker', 1);
INSERT INTO item (id, image_src, name, price) VALUES (5, '/item5', 'stationary', 1);

INSERT INTO preselection (id, image_src, name, description, price, bag_id, item_ids) VALUES (1, '/images/preselections/preselection1.webp', 'preselection1', 'Celebration Gift Pack (Person-alised)', 59, 1, '{1, 2, 3}');
INSERT INTO preselection (id, image_src, name, description, price, bag_id, item_ids) VALUES (2, '/images/preselections/preselection2.webp', 'preselection2', 'LOL OMG Gift Pack', 109, 1, '{3, 4, 5}');
INSERT INTO preselection (id, image_src, name, description, price, bag_id, item_ids) VALUES (3, '/images/preselections/preselection3.webp', 'preselection3', 'Fun Surprises Gift Pack', 109, 2, '{1, 2, 3}');
INSERT INTO preselection (id, image_src, name, description, price, bag_id, item_ids) VALUES (4, '/images/preselections/preselection4.png', 'preselection4', 'preseleSquishmallow Surprise Gift Packction4', 89, 2, '{1, 3, 5}');