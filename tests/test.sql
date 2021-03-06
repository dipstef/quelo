create table test (
    value       integer primary key not null
);

create table full_name (
    id          integer not null primary key autoincrement,
    name        text not null,
    surname     text not null,
    unique(name, surname)
);

create table person (
    id                    integer not null primary key autoincrement,
    full_name_id          integer not null references full_name(id) on delete cascade,
    social_number         text not null,
    unique(social_number)
);


create table timestamp_value (
    id                    integer not null primary key autoincrement,
    value                 timestamp not null,
    unique(value)
);

create table url (
    id                    integer not null primary key autoincrement,
    value                 text not null,
    unique(value)
);