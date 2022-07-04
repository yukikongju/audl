--  from all season roster: https://audl-stat-server.herokuapp.com/stats-pages/game/2022-06-11-TB-ATL (rostersHome)

CREATE TABLE IF NOT EXISTS season_roster (
    id PRIMARY KEY, 
    team_season_id int NOT NULL,
    player_id int NOT NULL,
    jersey_number string NOT NULL, -- why
    first_name string NOT NULL,
    last_name string NOT NULL,
    ext_player_id string SECONDARY KEY
    ls_player_id string SECONDARY KEY
);

