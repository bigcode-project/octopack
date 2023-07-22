SELECT commit, subject, message, STRING_AGG(unnested_repo_name), license AS repos
FROM `commits_table_base`
GROUP BY commit, subject, message, license
