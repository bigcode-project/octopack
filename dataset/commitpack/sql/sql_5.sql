SELECT commit,repos,licenses
FROM (
(
  SELECT commit AS commit_base
  FROM `commits_table_dedup_files`
  GROUP BY commit
  HAVING COUNT(*) = 1
)
JOIN (
  SELECT
    commit,subject,message,repos,old_file,new_file
  FROM
    `commits_table_dedup_files` AS commits_table_base
  ) commits_table_base
ON commits_table_base.commit = commit_base
)
