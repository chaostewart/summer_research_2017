### Step 1: crawling season by season data for all skaters who played games in NHL between season 1998-1999 to season 2016-2017. 
+ Data is crawled from NHL.com, under "STATS" --> "PLAYERS" : http://www.nhl.com/stats/player?aggregate=0&gameType=2&report=skatersummary&pos=S&reportType=season&seasonFrom=20162017&seasonTo=20162017&filter=gamesPlayed,gte,1&sort=points,goals,assists
+ Python scripts and sample data fies can be find here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_NHL_season_stats
+ The data is written to database as table "" (referred as table_1 in this context for convenience).
   
### Step 2: screen players in table_1, only crawl the player statistics for the skaters who got drafted between year 1998-2008.
+ With player id obtained from table_1, crawl player stats from NHL.com, using url: "http://www.nhl.com/player/" + player_id
+ Python scripts and sample data fies can be find here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_NHL_player_stats
+ Record each players demographic info, draft info as well as his season stats for the last season he played before he got drafted into NHL.
+ Only record player stats for those who got drafted in 1998-2008.
+ The data is written to database as table "" (referred as table_2).
+ Note that players in table_1 and table_2 have played greater than zero game in NHL.
+ To get player stats for the skater who got drafted into NHL but played 0 game in NHL, move to Step 3.
 
### Step 3: get player stats for the skater who got drafted into NHL but played 0 game in NHL
+ Crawl player stats for all skater who got drafted between 1998-2008 whether they ended up playing gmaes in NHL or not.
+ Data is crawled form eliteprospects.com, under "DRAFTS", select draft year between 1998-2008.
+ Only skaters' stats are recorded. Goalies are ommitted.
+ Python scripts and sample data fies can be find here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_elite_prospect
+ The data is written to database as table "" (referred as table_3).
+ Exclude players appeared in table_2 from table_3, the rest of the player are the skaters who got drafted but never played in NHL.
+ To identify the same player who appear in both table_2 and table_3, use the join condition on same birthday,same draft year and same overall.
+ At the end, player stats for skaters who played 0 games is saved in table "" (referred as table_4).
 
### Step 4: obtain final CSS rank for all skaters from north America or Europe between 1998-2008
+ The final CSS rank is only available on draftanalyst.com, under "Rankings" --> "Year-to-Year Central Scouting Final Rankings"
+ Scrape the rankings for skaters only.
+ The data is written to database as table "chao_draft.draft_analyst_CSS_ranking" (referred as table_5)

### Step 5: find corresponding CSS rankings in table_5 for skaters in talbe_2 and table_4
+ Firstly, many skaters rankings can be found by simply joining table_2 (or table_4) with table_5 on same draft year and same player name.
+ However, due to misspelling or the use of nicknames, many skaters' ranking need to be found painfully in a manual way.
+ Update players in table_5 with corresponding PlayerId from table_2 and eliteId from table_4.
+ Note: many names in table_5 have been modified according to table_4 and table_2 due to typos or spelling variations.

