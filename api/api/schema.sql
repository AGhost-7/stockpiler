
drop table if exists `user`;
create table `user` (
	id char(36) primary key,
	email varchar(256),
	password blob(60),
	active boolean not null default false
);

drop table if exists `email_confirmation`;
create table `email_confirmation` (
	id char(36) primary key,
	user_id char(36) not null references `user`(id)
);

drop table if exists `location`;
create table `location` (
	id char(36) primary key,
	name text not null,
	owner_id char(36) not null references `user`(id)
);

drop table if exists `item`;
create table `item` (
	id char(36) primary key,
	name text not null,
	location_id char(36) not null references `location`(id),
	created_by_id char(36) not null references `user`(id),
	created_at timestamp not null,
	updated_by_id char(36) not null references `user`(id),
	updated_at timestamp not null,
	quantity integer unsigned not null
);

drop table if exists `item_log`;
create table item_log (
	item_id char(36) not null references `item`(id),
	name text not null,
	location_id char(36) not null references `location`(id),
	quantity integer unsigned not null,
	edited_by_id char(36) not null references `user`(id),
	edited_at timestamp not null,
	primary key(item_id, edited_at)
);

drop table if exists `device`;
create table device (
	id char(36) not null,
	mac_address char(36) not null,
	hardware_id blob(64) not null,
	location_id char(36) not null references `location`(id),
	created_at timestamp not null,
	created_by_id char(36) not null references `user`(id),
	name text
);

