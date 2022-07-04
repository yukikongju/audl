--  from https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TB-ATL

CREATE TABLE IF NOT EXISTS game_metadata (
    id int PRIMARY KEY,
    team_season_id_home int NOT NULL,
    team_season_id_away int NOT NULL,
    status_id int NOT NULL,
    score_home int NOT NULl, 
    score_away int NOT NULL,
    live bool,
    reg_season bool, 
    ignore_game bool, 
    start_timestamp string NOT NULL, 
    start_timezone string NOT NULL,
    start_time_tbd string,
    aw_section string NOT NULL,
    ext_game_id string SECONDARY KEY,
    update_timestamp string NOT NULL, 
    location_id int NOT NULL, 
    ls_game_id string NOT NULL, 
    ticket_url string NOT NULL
);

