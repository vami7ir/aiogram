create table if exists users
(
    id          serial
        primary key,
    telegram_id integer   not null
        constraint users_user_id_key
            unique,
    name        text      not null,
    create_at   timestamp not null
);


