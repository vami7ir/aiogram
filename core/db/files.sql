create table if exists files
(
    id        serial
        primary key,
    user_id   integer   not null,
    path      text      not null,
    type      text      not null,
    create_at timestamp not null
);


