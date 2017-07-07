### Step 1: crawl season-by-season statistics for all skaters who played games in NHL between season 1998-1999 to season 2016-2017. 
+ Data is crawled from NHL.com, under "STATS" --> "PLAYERS". i.e. link here: http://www.nhl.com/stats/player?aggregate=0&gameType=2&report=skatersummary&pos=S&reportType=season&seasonFrom=20162017&seasonTo=20162017&filter=gamesPlayed,gte,1&sort=points,goals,assists
+ Python scripts and sample data fies can be found here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_NHL_season_stats
+ The data is written to database as table "chao_draft.NHL_season_stats_1998_2016_original" (referred as table_1 in this context for convenience).
+ Note: this dataset also includes skaters who got drafted before 1998 and after 2008 which is outside of the range of our intest.
   
### Step 2: screen players in table_1; crawl the player statistics for skaters who got drafted between year 1998-2008.
+ With player id (e.g. PlayerId = 8473593) obtained from table_1, crawl player stats for skaters for got drafted between 1998-2008 from NHL.com using url = "http://www.nhl.com/player/" + player_id
+ Python scripts and sample data fies can be found here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_NHL_player_stats
+ Record each players demographic info, draft info as well as his season stats for the last season he played before he got drafted into NHL.
+ The data is written to database as table "chao_draft.NHL_skaters_stats_1998_2008_original" (referred as table_2).
+ Total number of distinct skaters in talbe_2 is 1106.
+ Note that skaters in table_1 and table_2 have played greater than zero game in NHL. NHL.com does not have statistics for players who got drafted into NHL but didn't play any games in NHL, which is available in Step 3.
+ Based on PlayerId, eliminate season stats for skaters who got drafted outside the draft year range of 1998-2008 in table_1, save the season stats of our interest as table "chao_draft.NHL_season_stats_for_skaters_drafted_1998_2008" (referred as table_3).
+ Note: table_3 contains skaters who got drafted in the draft year range of our interest BUT DID NOT PLAY games in their first 7 seasons in NHL. To be accurate, there are 28 of them didn't play games in NHL until their 8th season or later on.
 
### Step 3: get player stats for skaters who got drafted into NHL but never played games in NHL.
+ Crawl player stats for all skaters who got drafted between 1998-2008 from eliteprospects.com whether these skaters ended up playing gmaes in NHL or not.
+ Data is crawled from eliteprospects.com, under "DRAFTS" --> select draft year between 1998-2008.
+ Python scripts and sample data fies can be find here: https://github.com/chaostewart/summer_research_2017/tree/master/crawl_elite_prospects
+ Only skaters' stats are recorded. Goalies are ommitted.
+ The data is written to database as table "chao_draft.elite_prospects_skaters_stats_1998_2008_original" (referred as table_4).
+ Total number of distinct skaters in talbe_4 is 2480.
+ Find all 1106 players from table_2 in table_4, saved as "chao_draft.elite_nhl_duplicated_skaters_view" (referred as view_1).
      
      create view chao_draft.elite_nhl_duplicated_skaters_view as
      select distinct eliteId, t1.PlayerName as elite_name, t2.PlayerName as nhl_name, PlayerId, t2.DraftYear, t2.Overall
      from chao_draft.elite_prospects_skaters_stats_1998_2008_original as t1,
      chao_draft.NHL_skaters_stats_1998_2008_original as t2
      where t1.DraftYear = t2.DraftYear and t1.Overall = t2.Overall
      order by t2.DraftYear, t2.Overall;
         
+ Excluding players appeared in table_2 from table_4, are the skaters who got drafted but never played in NHL. SAved as table "chao_draft.elite_zerogames_skaters_find_CSSrank" (referred as table_5)
      
      create table chao_draft.elite_zerogames_skaters_find_CSSrank as
      select distinct eliteId, PlayerName, BirthDate, Birthplace, DraftYear, Overall
      from chao_draft.elite_prospects_skaters_stats_1998_2008_original
      where eliteId not in
      (select eliteId from chao_draft.elite_nhl_duplicated_skaters_view);
+ Total number of distinct skaters in talbe_5 is 2480 - 1106 = 1374.
 
### Step 4: obtain final Cental Scouting Services(CSS) rank for all skaters.
+ The final CSS rank is available only on draftanalyst.com --> under "Rankings" --> "Year-to-Year Central Scouting Final Rankings".
+ Scrape the rankings for skaters only from both North America or Europe between 1998-2008.
+ The data is written to database as table "chao_draft.draft_analyst_CSS_rank" (referred as table_6)
+ Note: Draft year 2003 has the least number of CSS ranks available. There are only 55 ranks available skaters from north America and Europe in total. 
DraftYear | count(*) |
1998 | 146 |
1999 | 296 |
2000 | 309 |
2001 | 309 |
2002 | 220 |
2003 | 55 |
2004 | 390 |
2005 | 280 | 
2006 | 379 |
2007 | 385 |
2008 | 385 |


### Step 5: find corresponding CSS rankings in table_6 for skaters in talbe_2 and table_5
+ Firstly, many skaters rankings can be found by simply joining table_2 (or table_5) with table_6 on same draft year and same player name.
+ However, due to misspelling or the use of nicknames, many skaters' ranking need to be found painfully in a manual way.
+ Update players in table_6 with corresponding PlayerId from table_2 and eliteId from table_5.
+ Note: many names in table_6 have been modified according to table_2 and table_5 due to typos or spelling variations.

### Step 6: create seven-season stats tables that are equivalent to Wilson's table
+ Depending on including playoffs in NHL or not, two views are created as 
"chao_draft.season_sums_with_playoffs_1998_2008_view" (referred as view_7) and "chao_draft.season_sums_regular_season_only_1998_2008_view" (referred as view_8)
+ Based on view_7 and view_8, repectively, two tables that contain skaters first seven-season stats in NHL are created as
"chao_draft.seven_season_sums_with_playoffs_1998_2008" (referred as table_7) and "chao_draft.seven_season_sums_regular_season_only_1998_2008" (referred as table_8)
