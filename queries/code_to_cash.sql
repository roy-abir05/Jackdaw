-- queries/code_to_cash.sql
-- Joins GitHub commits and Stripe charges to correlate deployments with revenue.
-- Converts Stripe cents to USD and joins the customers table to get real names.
SELECT 
    g.sha AS commit_hash,
    g.commit__author__name AS developer,
    (s.amount / 100.0) AS revenue_usd,
    c.name AS customer_name,
    c.email AS customer_email
FROM github.commits g
CROSS JOIN stripe.charges s
JOIN stripe.customers c ON s.customer = c.id
WHERE g.owner = '{github_owner}' AND g.repo = '{github_repo}'
-- Order by the most recent payments
ORDER BY s.created DESC, g.commit__author__date DESC
LIMIT 5;