################## Using index to speed up query ##################

ALTER TABLE sportlogiq_new.team_HomeAway_Info ADD INDEX (gameId) USING BTREE;

ALTER TABLE sportlogiq_new.GDMDPevents ADD INDEX (gameId) USING BTREE;
ALTER TABLE sportlogiq_new.GDMDPevents ADD INDEX (id) USING BTREE;

################################################################## 
################ Create table of GDMDP events ####################
########## for 446 games only from all 1140 games ################
################################################################## 

DROP TABLE IF EXISTS sportlogiq_new.GDMDP1140events;
CREATE TABLE sportlogiq_new.GDMDP1140events AS 
SELECT t1.id, t1.gameId, t1.teamId, t1.P, t1.GD, t1.MD, t1.`name` 
FROM
    sportlogiq_new.GDMDPevents AS t1;

ALTER TABLE sportlogiq_new.GDMDP1140events ADD COLUMN venue varchar(15) after TeamId;

ALTER TABLE sportlogiq_new.GDMDP1140events ADD INDEX (id) USING BTREE;
ALTER TABLE sportlogiq_new.GDMDP1140events ADD INDEX (gameId) USING BTREE;

UPDATE sportlogiq_new.GDMDP1140events AS T1,
    sportlogiq_new.team_HomeAway_Info AS T2 
SET 
    T1.venue = CASE
        WHEN T1.TeamId = T2.AwayId THEN 'away'
        WHEN T1.TeamId = T2.HomeId THEN 'home'
    END
WHERE
    T1.gameId = T2.gameId;
    
############################## Modified Query Starts Here ##############################

/*Create home_goal & away_goal columns 
e.g. home_goal value is 1 only if it's a home goal event; 0, otherwise  */

UPDATE sportlogiq_new.GoalEvents1 AS T1,
    sportlogiq_new.team_HomeAway_Info AS T2 
SET 
    T1.venue = CASE
        WHEN T1.TeamId = T2.AwayId THEN 'away'
        WHEN T1.TeamId = T2.HomeId THEN 'home'
    END
WHERE
    T1.gameId = T2.gameId;


ALTER TABLE sportlogiq_new.GoalEvents1 ADD INDEX (id) USING BTREE;
ALTER TABLE sportlogiq_new.GoalEvents1 ADD INDEX (gameId) USING BTREE;

drop view if exists sportlogiq_new.GoalEvents2_view;
CREATE VIEW sportlogiq_new.GoalEvents2_view AS
    SELECT 
       id,gameId,TeamId,venue,IF(venue = 'home', 1, 0) AS home_goal,
        IF(venue = 'away', 1, 0) AS away_goal
    FROM sportlogiq_new.GoalEvents1;

DROP TABLE if exists sportlogiq_new.GoalEvents2;	   
DROP VIEW if exists sportlogiq_new.GoalEvents2;  
CREATE TABLE sportlogiq_new.GoalEvents2 AS SELECT * FROM
    sportlogiq_new.GoalEvents2_view;

ALTER TABLE sportlogiq_new.GoalEvents2 ADD INDEX (id) USING BTREE;
ALTER TABLE sportlogiq_new.GoalEvents2 ADD INDEX (gameId) USING BTREE;

/* Calculate home_future_goals & away_future_goals for each event 
by summing up the number of home/away_goal events after each event.
If it's a null value, which happens to all events 
starting from the last goal event to the last event in each game, 
set the sum value to be 0. */


drop view if exists sportlogiq_new.GDMDP1140events01_view;
CREATE VIEW sportlogiq_new.GDMDP1140events01_view AS
    SELECT 
        t1.id,
        t1.gameId,
        t1.TeamId,
        t1.venue,
        t1.P,
        t1.GD,
        t1.MD,
        t1.name,
        if (sum(t2.home_goal) is not null, sum(t2.home_goal), 0) as home_future_goals,
        if (sum(t2.away_goal) is not null, sum(t2.away_goal), 0) as away_future_goals
        from sportlogiq_new.GDMDP1140events as t1 
        left outer join sportlogiq_new.GoalEvents2 as t2
        on t1.gameId = t2.gameId AND t1.id < t2.id
        group by t1.id;
  
 DROP TABLE IF EXISTS  sportlogiq_new.GDMDP1140events01;
 CREATE TABLE sportlogiq_new.GDMDP1140events01 AS
 SELECT * FROM
 sportlogiq_new.GDMDP1140events01_view;
  
 /* Calculate the sum_future_goals for each event by simply add update
 home_future_goals & away_future_goals of each event*/
    
drop view if exists sportlogiq_new.GDMDP1140events02_view;
CREATE VIEW sportlogiq_new.GDMDP1140events02_view AS
    SELECT 
        id,
        gameId,
        TeamId,
        venue,
        P,
        GD,
        MD,name,
        home_future_goals,
        away_future_goals,
        (home_future_goals + away_future_goals) AS sum_future_goals
    FROM
        sportlogiq_new.GDMDP1140events01;
        
DROP TABLE IF EXISTS  sportlogiq_new.GDMDP1140events02;
 CREATE TABLE sportlogiq_new.GDMDP1140events02 AS
 SELECT * FROM
 sportlogiq_new.GDMDP1140events02_view;

############################## Modified Query Ends Here ##############################


################### Calculate AVG of sum & home & away future goals for ################### 
############## each (period, goaldifferential, manpower, venue) combination ###############
################################# in each single game #####################################

DROP VIEW IF EXISTS sportlogiq_new.GDMDP1140events_avg;	
CREATE VIEW sportlogiq_new.GDMDP1140events_avg AS
    SELECT 
        gameId,
        P,
        GD,
        MD,
        venue,
        AVG(home_future_goals) AS avg_home_future_goals,
        AVG(away_future_goals) AS avg_away_future_goals,
        AVG(sum_future_goals) AS avg_sum_future_goals,
        count(*) AS count
    FROM
        sportlogiq_new.GDMDP1140events02
    GROUP BY gameId , P , GD , MD , venue;

################### Calculate SUM of averaged sum & home & away future goals for ####################
################### each (period, goaldifferential, manpower, venue) combination  ###################
######################################### for all 446 games #########################################

DROP VIEW IF EXISTS sportlogiq_new.GDMDP1140events_sum;	
CREATE VIEW sportlogiq_new.GDMDP1140events_sum AS
    SELECT 
        P,
        GD,
        MD,
        venue,
       sum(avg_home_future_goals) AS sum_home_future_goals,
        sum(avg_away_future_goals) AS sum_away_future_goals,
         sum(avg_sum_future_goals) AS sum_sum_future_goals, 
         count(*) AS count
    FROM
        sportlogiq_new.GDMDP1140events_avg
    GROUP BY P , GD , MD , venue;



    
DROP VIEW IF EXISTS sportlogiq_new.GDMDPevents_compare_sum;
CREATE VIEW sportlogiq_new.GDMDPevents_compare_sum AS
    SELECT 
        t1.P,
        t1.GD,
        t1.MD,
        t1.venue,
        t1.count AS count1140,
        t2.count AS count446,
        t1.sum_home_future_goals AS sum_home_1140,
        t2.sum_home_future_goals AS sum_home_446,
        t1.sum_away_future_goals AS sum_away_1140,
        t2.sum_away_future_goals AS sum_away_446,
        t1.sum_sum_future_goals AS sum_sum_1140,
        t2.sum_sum_future_goals AS sum_sum_446
    FROM
        sportlogiq_new.GDMDP1140events_sum AS t1
            LEFT OUTER JOIN
        sportlogiq_new.GDMDP446events_sum AS t2 ON t1.P = t2.P AND t1.GD = t2.GD
            AND t1.MD = t2.MD
            AND t1.venue = t2.venue;
            
            
            
            
            
DROP VIEW IF EXISTS sportlogiq_new.GDMDPevents_compare_avg;
CREATE VIEW sportlogiq_new.GDMDPevents_compare_avg AS
    SELECT 
		t1.gameId,
        t1.P,
        t1.GD,
        t1.MD,
        t1.venue,
		t1.count AS count1140,
        t2.count AS count446,
        t1.avg_home_future_goals AS avg_home_1140,
        t2.avg_home_future_goals AS avg_home_446,
        t1.avg_away_future_goals AS avg_away_1140,
        t2.avg_away_future_goals AS avg_away_446,
        t1.avg_sum_future_goals AS avg_sum_1140,
        t2.avg_sum_future_goals AS avg_sum_446
    FROM
        sportlogiq_new.GDMDP1140events_avg AS t1
            LEFT OUTER JOIN
        sportlogiq_new.GDMDP446events_avg t2 ON t1.gameId = t2.gameId AND t1.P = t2.P AND t1.GD = t2.GD
            AND t1.MD = t2.MD
            AND t1.venue = t2.venue;
