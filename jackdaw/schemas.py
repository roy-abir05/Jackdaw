# jackdaw/schemas.py

BUNDLED_SCHEMAS = {
    "github": {
        "commits": "Columns: sha, commit__author__name, commit__author__date, commit__message. RULE: MUST include WHERE owner = '{gh_owner}' AND repo = '{gh_repo}'",
        "issues": "Columns: number, title, state, user__login, repository__full_name. RULE: MUST include WHERE owner = '{gh_owner}' AND repo = '{gh_repo}'",
        "repo_action_runs": "Columns: workflow_id, status, conclusion, run_started_at. RULE: MUST include WHERE owner = '{gh_owner}' AND repo = '{gh_repo}'",
        "search_issues": "Function: github.search_issues(q => 'repo:{gh_owner}/{gh_repo} bug'). Use named parameter 'q =>' for cross-repo search."
    },
    "stripe": {
        "charges": "Columns: id, amount, customer, created. Note: amount is in cents, divide by 100.0 for USD.",
        "customers": "Columns: id, name, email, created. Note: Join with stripe.charges ON stripe.charges.customer = stripe.customers.id"
    }
}