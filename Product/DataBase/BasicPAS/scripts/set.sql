use BasicPAS;

create table if not exists Users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	users_name char(40) not null,
	users_login char(30) not null,
    users_password varchar(20) not null,
    status_to_system char(20) not null
);

create table if not exists Workers (
	id INT AUTO_INCREMENT PRIMARY KEY,
    users_name char(40) not null,
    users_login char(30) not null,
    users_password varchar(20) not null,
    status_to_system char(20) not null
);

create table if not exists Admin (
	id INT AUTO_INCREMENT PRIMARY KEY,
    users_name char(40) not null,
    users_login char(30) not null,
    users_password varchar(20) not null,
    status_to_system char(20) not null
);

create table if not exists Orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
    owner_orders INT not null,
    id_product_orders INT not null,
	comment_orders TEXT not null,
    quantuty_orders INT not null
);

create table if not exists To_products (
	id INT AUTO_INCREMENT PRIMARY KEY,
	id_product INT not null,
    name_product char(30) not null,
    description_product TEXT,
	consumption_product INT not null
);

create table if not exists Product (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name_product char(30) not null,
    description_product TEXT not null,
	price_product INT not null,
    image_product text
);

create table if not exists Status_order (
	id_order INT not null PRIMARY KEY,
    worker INT,
    step_status char(20) not null
)