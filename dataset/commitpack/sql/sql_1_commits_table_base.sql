SELECT
  commit, difference, subject, message, unnested_repo_name, license
FROM (
  SELECT
    repo_name,
    lang.name AS language_name
  FROM
    `bigquery-public-data.github_repos.languages` AS lang_table,
    UNNEST(LANGUAGE) AS lang) lang_table
JOIN
  `bigquery-public-data.github_repos.licenses` AS license_table
ON
  license_table.repo_name = lang_table.repo_name
JOIN (
  SELECT
    *
  FROM
    `bigquery-public-data.github_repos.commits` AS commits_table,
    UNNEST(repo_name) AS unnested_repo_name) commits_table
ON
  commits_table.unnested_repo_name = lang_table.repo_name
WHERE
  ((license_table.license LIKE 'mit')
    OR (license_table.license LIKE 'artistic-2.0')
    OR (license_table.license LIKE 'isc')
    OR (license_table.license LIKE 'cc0-1.0')
    OR (license_table.license LIKE 'epl-1.0')
    OR (license_table.license LIKE 'mpl-2.0')
    OR (license_table.license LIKE 'unlicense')
    OR (license_table.license LIKE 'apache-2.0')
    OR (license_table.license LIKE 'bsd-3-clause')
    OR (license_table.license LIKE 'agpl-3.0')
    OR (license_table.license LIKE 'lgpl-2.1')
    OR (license_table.license LIKE 'bsd-2-clause'))
  AND ( (lang_table.language_name LIKE 'Python')
    OR (lang_table.language_name LIKE 'Java')
    OR (lang_table.language_name LIKE 'JavaScript')
    OR (lang_table.language_name LIKE 'HTML')
    OR (lang_table.language_name LIKE 'Common Lisp')
    OR (lang_table.language_name LIKE 'Shell')
    OR (lang_table.language_name LIKE 'R')
    OR (lang_table.language_name LIKE 'Perl%')
    OR (lang_table.language_name LIKE 'SQL')
    OR (lang_table.language_name LIKE 'C')
    OR (lang_table.language_name LIKE 'C#')
    OR (lang_table.language_name LIKE 'C++')
    OR (lang_table.language_name LIKE 'TypeScript')
    OR (lang_table.language_name LIKE 'Go')
    OR (lang_table.language_name LIKE 'Rust')
    OR (lang_table.language_name LIKE 'Swift')
    OR (lang_table.language_name LIKE 'PHP')
    OR (lang_table.language_name LIKE 'Dart')
    OR (lang_table.language_name LIKE 'Kotlin')
    OR (lang_table.language_name LIKE 'Matlab')
    OR (lang_table.language_name LIKE 'MATLAB')
    OR (lang_table.language_name LIKE 'Ruby') )
AND
  LENGTH(commits_table.message) > 5
AND 
  LENGTH(commits_table.message) < 10000
AND LOWER(commits_table.message) NOT LIKE 'update readme.md'
AND LOWER(commits_table.message) NOT LIKE 'initial commit'
AND LOWER(commits_table.message) NOT LIKE 'update'
AND LOWER(commits_table.message) NOT LIKE 'mirroring from micro.blog.'
AND LOWER(commits_table.message) NOT LIKE 'update data.json'
AND LOWER(commits_table.message) NOT LIKE 'update data.js'
AND LOWER(commits_table.message) NOT LIKE 'add files via upload'
AND LOWER(commits_table.message) NOT LIKE 'update readme'
AND LOWER(commits_table.message) NOT LIKE "can't you see i'm updating the time?"
AND LOWER(commits_table.message) NOT LIKE 'pi push'
AND LOWER(commits_table.message) NOT LIKE 'dummy'
AND LOWER(commits_table.message) NOT LIKE 'update index.html'
AND LOWER(commits_table.message) NOT LIKE 'first commit'
AND LOWER(commits_table.message) NOT LIKE 'create readme.md'
AND LOWER(commits_table.message) NOT LIKE 'heartbeat update'
AND LOWER(commits_table.message) NOT LIKE 'updated readme'
AND LOWER(commits_table.message) NOT LIKE 'update log'
AND LOWER(commits_table.message) NOT LIKE 'test'
AND LOWER(commits_table.message) NOT LIKE 'no message'
AND LOWER(commits_table.message) NOT LIKE 'readme'
AND LOWER(commits_table.message) NOT LIKE 'wip'
AND LOWER(commits_table.message) NOT LIKE 'updates'
AND LOWER(commits_table.message) NOT LIKE 'first commit'
AND LOWER(commits_table.message) NOT LIKE 'commit'
AND LOWER(commits_table.message) NOT LIKE 'update _config.yaml'
AND LOWER(commits_table.message) NOT LIKE 'update data.json'
AND LOWER(commits_table.message) NOT LIKE 'update data.js'
AND LOWER(commits_table.message) NOT LIKE 'merge%';
