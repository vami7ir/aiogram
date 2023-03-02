create table if exists expense
(
    id        serial
        primary key,
    summ      double precision                                                not null,
    create_at timestamp default date_trunc('second'::text, CURRENT_TIMESTAMP) not null,
    user_id   integer                                                         not null
);




