**(a) Blind Spot Exploited**

The blind spot our bypass exploits is over-privileged table access. The user should only be able to access the non-sensitive information needed for their task, but our bypass lets them access the protected **api_keys** table. We do this by writing the table name in a different, but still completely valid, SQLite format that isn't caught by the server's regex check. Since the server is checking the exact text of the query instead of what table SQLite actually ends up accessing, the query is able to get through.

**(b) Improved Defense**

Instead of adding every possible table-name format to a blacklist, I would change the server to use an allowlist. Before running a query, it should normalize any table names by removing quotes, brackets, backticks, or any other valid SQLite formatting, then compare the resulting names against a list of tables the user is actually allowed to access. If the query references any table that isn't on that list, it should be rejected. This is a better approach because it checks what table the query is really trying to access instead of trying to block every possible way someone could write the table name.

**(c) New Bypass This Defense Would Invite**

This defense would stop the quoted table-name trick, but it would probably push an attacker to look for weaknesses somewhere else. Instead of changing how the table name is written, they might try using more complicated SQL queries, like subqueries or views, if the server doesn't correctly identify every table being accessed. They could also look for another tool on the server that exposes the same information without going through the SQL check. A stronger long-term solution would be to avoid letting users run arbitrary SQL at all and instead provide a small set of predefined, parameterized database queries that only return the information users are supposed to see.
