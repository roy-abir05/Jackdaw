-- queries/code_to_cash.sql
-- Uses Window Functions to "zip" the streams of commits and revenue together chronologically.

WITH ranked_commits AS (
    SELECT 
        sha, 
        commit__author__name, 
        ROW_NUMBER() OVER(ORDER BY commit__author__date DESC) as rn
    FROM github.commits 
    WHERE owner = '{github_owner}' AND repo = '{github_repo}'
),
ranked_charges AS (
    SELECT 
        s.amount, 
        c.name, 
        ROW_NUMBER() OVER(ORDER BY s.created DESC) as rn
    FROM stripe.charges s
    JOIN stripe.customers c ON s.customer = c.id
)
SELECT 
    g.sha AS commit_hash,
    g.commit__author__name AS developer,
    (s.amount / 100.0) AS revenue_usd,
    s.name AS customer_name
FROM ranked_commits g
JOIN ranked_charges s ON g.rn = s.rn
ORDER BY g.rn
LIMIT 5;