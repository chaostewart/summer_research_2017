SELECT * FROM chao_draft.prediction_2nd_cohort
where (class_0_prob >= 0.5 AND GP_greater_than_0 = 'yes')
or (class_0_prob < 0.5 AND GP_greater_than_0 = 'no');