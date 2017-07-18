create table chao_draft.prediction_2008_view as

SELECT id, PlayerName, CSS_rank, sum_7yr_GP,class_0_prob,
  @prev := @curr,
  @curr := class_0_prob,
  @rank := IF(@prev = @curr, @rank, @rank + @i) AS rank,
  IF(@prev <> class_0_prob, @i:=1, @i:=@i+1) AS counter
FROM chao_draft.prediction_2nd_cohort,
  (SELECT @curr := null, @prev := null, @rank := 0, @i := 0) tmp_tbl
where DraftYear = 2008
ORDER BY class_0_prob DESC

/*
Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '/*12:37:42 SELECT id, PlayerName, CSS_rank   @prev := @curr,   @curr := class_0_' at line 13
*/