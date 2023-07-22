SELECT *
FROM (
  SELECT
    commit,subject,message,repos,difference,license
  FROM
    `commits_table_dedup` AS commits_table_dedup
JOIN (
  SELECT
    commit AS commit_base,difference
  FROM
    `bigquery-public-data.github_repos.commits` AS commits_table_base
  ) commits_table_base
ON
  commits_table_base.commit_base = commits_table_dedup.commit
)
