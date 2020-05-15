use BasicPAS;

INSERT Users (users_name, users_login, users_password, status_to_system) 
VALUES ('User', 'user', 123, 'Пользователь');

INSERT Workers (users_name, users_login, users_password, status_to_system) 
VALUES ('Worker', 'worker', 123, 'Рабочий');

INSERT Admin (users_name, users_login, users_password, status_to_system) 
VALUES ('Admin', 'admin', 123, 'Админ');

INSERT Product (name_product, description_product, price_product, image_product) 
VALUES ("Пицца Барбекю", "Пицца с утончённым вкусом, которую должен попробовать каждый!", 350, Null);
INSERT Product (name_product, description_product, price_product, image_product) 
VALUES ("Пицца Грибная", "Настоящее грибное изобилие!", 350, Null);
INSERT Product (name_product, description_product, price_product, image_product) 
VALUES ("Пицца Аль-Копчоне", "Пицца, которой нельзя сопротивляться.", 350, Null);
INSERT Product (name_product, description_product, price_product, image_product) 
VALUES ("Кока-Кола", "Возьми в дорогу!", 100, Null);
INSERT Product (name_product, description_product, price_product, image_product) 
VALUES ("Латте и Круассан", "Начни своё утро с приятного кофе и нежного круассана!", 102, Null);

INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (1, "Пицца Барбекю", "Томатный соус, сыр, мясной топинг, сосиски баварские с зеленью, помидоры, перец болгарский, лук красный, соус барбекю.", 310);
INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (2,"Пицца Грибная", "Соус грибной, сыр, шампиньоны, опята маринованные, грибы шиитаке, микс салат.", 300);
INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (3, "Пицца Аль-копчоне", "Фирменный соус, сыр, охотничьи колбаски, колбаса п/к, салями, маринованные огурчики, помидоры.", 270);
INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (4, "Кока-Кола", "0.5л, 0.75л, 1л", 90);
INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (5, "Латте", "0.19л", 35);
INSERT To_products (id_product, name_product, description_product, consumption_product) 
VALUES (5, "Круассан", "Круассан с черникой", 67);

INSERT Orders (owner_orders, id_product_orders, comment_orders, quantuty_orders) 
VALUES (1, 3, "Нет комментариев", 1);
INSERT Orders (owner_orders, id_product_orders, comment_orders, quantuty_orders) 
VALUES (1, 4, "Нет комментариев", 1);
INSERT Orders (owner_orders, id_product_orders, comment_orders, quantuty_orders) 
VALUES (1, 1, "Нет комментариев", 1);

INSERT Status_order (id_order, worker, step_status) 
VALUES (1, Null, 'Новый');
INSERT Status_order (id_order, worker, step_status) 
VALUES (2, Null, 'Новый');
INSERT Status_order (id_order, worker, step_status) 
VALUES (3, Null, 'Новый');





