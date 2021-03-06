create table japan_service.japan_user(
id int primary key auto_increment,
email varchar(100) not null,
password varchar(100) not null,
username varchar(100) not null,
level varchar(10) not null,
is_staff int default 0,
regist_date datetime default now()
);

create table japan_service.japan_hanja(
id int primary key auto_increment,
seq int,
main varchar(100) not null,
mean varchar(100),
um varchar(100),
hun varchar(100),
level varchar(100),
use_yn varchar(10) default 'y',
regist_date datetime default now()
);

create table japan_service.japan_um_word(
id int primary key auto_increment,
hanja_id int not null,
word varchar(500),
hira varchar(500),
hangul varchar(500)
);

create table japan_service.japan_hun_word(
id int primary key auto_increment,
hanja_id int not null,
word varchar(500),
hira varchar(500),
hangul varchar(500)
);

create table japan_service.japan_exam(
id int primary key auto_increment,
hanja_id int not null,
exam varchar(500),
hira varchar(500),
hangul varchar(500)
);

ALTER TABLE japan_user convert to charset utf8;
ALTER TABLE japan_hanja convert to charset utf8;
ALTER TABLE japan_um_word convert to charset utf8;
ALTER TABLE japan_hun_word convert to charset utf8;
ALTER TABLE japan_exam convert to charset utf8;

create table picture(
id int auto_increment primary key,
file_name varchar(100),
file_dir varchar(100),
regist_date DATETIME,
delete_yn varchar(10) default 'N',
normal varchar(100),
soft varchar(100),
adult varchar(100)
);

ALTER TABLE picture convert to charset utf8;

create table dc_japanese(
    id int primary key AUTO_INCREMENT,
    data_num varchar(500),
    data_subject varchar(500),
    data_content varchar(500),
    data_writer varchar(500),
    data_ip varchar(500),
    regist_date datetime default now()
);

ALTER TABLE dc_japanese convert to charset utf8;
