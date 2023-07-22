SELECT
    commit,subject,message,repos,license,d.old_path as old_file,d.new_path as new_file
FROM
    `commits_table_dedup_difference` AS commits_table,
    UNNEST(difference) AS d
WHERE (d.old_path = d.new_path) AND (d.old_path IS NOT NULL) AND (d.new_path IS NOT NULL)
