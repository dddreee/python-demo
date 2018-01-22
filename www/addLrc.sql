use awesome;

create table `net_ease_lrc` (
    `id` VARCHAR(50) NOT NULL,
    `song_id` VARCHAR(50) NOT NULL,
    `song_name` VARCHAR(50) DEFAULT NULL,
    `singer_name` VARCHAR(50) DEFAULT NULL,
    `lrc` VARCHAR(3000) DEFAULT NULL,
    `user_img` VARCHAR(500) DEFAULT NULL,
    `cover_img` VARCHAR(100) DEFAULT NULL,
    PRIMARY key (`id`)
) engine = innodb DEFAULT charset = utf8;