drop table if exists chao_draft.rank_m5p_prob_2001;
create table chao_draft.rank_m5p_prob_2001 as
SELECT id, PlayerName, DraftYear, Predicted_GP,
  @prev := @curr,
  @curr := Predicted_GP,
  @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank_m5p,
  IF(@prev <> Predicted_GP, @i:=1, @i:=@i+1) AS counter
FROM chao_draft.m5p_prediction_1st_cohort,
  (SELECT @curr := null, @prev := null, @rank:= 1, @i := 0) tmp_tbl
where DraftYear = 2001
order by Predicted_GP DESC;

drop table if exists chao_draft.rank_m5p_prob_2002;
create table chao_draft.rank_m5p_prob_2002 as
SELECT id, PlayerName, DraftYear, Predicted_GP,
  @prev := @curr,
  @curr := Predicted_GP,
  @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank_m5p,
  IF(@prev <> Predicted_GP, @i:=1, @i:=@i+1) AS counter
FROM chao_draft.m5p_prediction_1st_cohort,
  (SELECT @curr := null, @prev := null, @rank:= 1, @i := 0) tmp_tbl
where DraftYear = 2002
order by Predicted_GP DESC;

drop table if exists chao_draft.rank_m5p_prob_2007;
create table chao_draft.rank_m5p_prob_2007 as
SELECT id, PlayerName, DraftYear, Predicted_GP,
  @prev := @curr,
  @curr := Predicted_GP,
  @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank_m5p,
  IF(@prev <> Predicted_GP, @i:=1, @i:=@i+1) AS counter
FROM chao_draft.m5p_prediction_2nd_cohort,
  (SELECT @curr := null, @prev := null, @rank:= 1, @i := 0) tmp_tbl
where DraftYear = 2007
order by Predicted_GP DESC;

drop table if exists chao_draft.rank_m5p_prob_2008;
create table chao_draft.rank_m5p_prob_2008 as
SELECT id, PlayerName, DraftYear, Predicted_GP,
  @prev := @curr,
  @curr := Predicted_GP,
  @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank_m5p,
  IF(@prev <> Predicted_GP, @i:=1, @i:=@i+1) AS counter
FROM chao_draft.m5p_prediction_2nd_cohort,
  (SELECT @curr := null, @prev := null, @rank:= 1, @i := 0) tmp_tbl
where DraftYear = 2008
order by Predicted_GP DESC;