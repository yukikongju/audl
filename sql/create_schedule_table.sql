--  from https://audl-stat-server.herokuapp.com/web-api/games?limit=10
CREATE TABLE IF NOT EXISTS schedule (
    gameID string PRIMARY KEY,
    awayTeamCity string NOT NULL,
    awayTeamID string NOT NULL,
    awayTeamName string NOT NULL,
    awayTeamNameRaw string NOT NULL,
    homeTeamCity string NOT NULL,
    homeTeamID string NOT NULL,
    homeTeamName string NOT NULL,
    homeTeamNameRaw string NOT NULL,
    status string NOT NULL, 
    ticketURL string NOT NULL, 
    streamURL string NOT NULL
    hasRosterReport bool,
    locationName string NOT NULL, 
    locationURL string NOT NULL, 
    startTimestamp string NOT NULL, 
    startTIMEzone string NOT NULL,
    startTimeTBD string,
);
