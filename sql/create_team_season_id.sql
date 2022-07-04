--  from https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TB-ATL

CREATE TABLE IF NOT EXISTS team_metadata (
    id int PRIMARY KEY,
    team_id int NOT NULL,
    season_id int NOT NULL,
    division_id int NOT NULL, 
    city string NOT NULL,
    abbrev string NOT NULL,
    ulti_analytics_ext_id string,
    final_standing string,
    name string NOT NULL,
    ext_team_id string NOT NULL, 
    ls_team_id string NOT NULL, 
);
