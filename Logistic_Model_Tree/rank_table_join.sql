create view chao_draft.join_all_rank_table_view as
SELECT 
    distinct t1.id, t2.PlayerName, t1.DraftYear, t3.Overall, t1.CSS_rank, t2.rank + 1 as LMT_rank,t1.sum_7yr_GP,t1.sum_7yr_TOI
FROM
    chao_draft.join_skater_and_season_stats_10_years AS t1,
	chao_draft.prediction_1278_view as t2,
    chao_draft.all_skaters_stats_10_years_view AS t3
    where t1.id = t2.id and t1.id = t3.id AND (t1. DraftYear = 2001 or t1. DraftYear = 2002 or t1. DraftYear = 2007 or t1. DraftYear = 2008);