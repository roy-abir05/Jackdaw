-- queries/daily_snapshot.sql
-- Gets the latest deployments/commits to power the dashboard timeline
SELECT 
    sha AS commit_hash, 
    commit__author__name AS author, 
    commit__message AS message,
    commit__author__date AS timestamp
FROM github.commits
WHERE owner = '{github_owner}' AND repo = '{github_repo}'
ORDER BY commit__author__date DESC
LIMIT 10;