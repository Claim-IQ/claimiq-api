from django.db import connection
from rest_framework import permissions, viewsets
from rest_framework.response import Response


def dictfetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def run_query(sql, single=False, column=None):
    """Run SQL and return results as dicts or simple values"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = dictfetchall(cursor)
        if single:
            return rows[0] if rows else None
        if column:
            return [row[column] for row in rows]
        return rows


class StatisticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # --- Basic complaint statistics ---
        metrics = run_query("""
            SELECT
                COUNT(*) AS complaints_overall,
                SUM(CASE WHEN cs.label = 'W trakcie' THEN 1 ELSE 0 END) AS complaints_in_progress,
                COUNT(CASE WHEN c.exit_date IS NOT NULL THEN 1 END) AS complaints_exited,
                CAST(AVG(c.exit_date - c.submit_date) AS INTEGER) AS average_consideration_days,
                SUM(CASE
                    WHEN cs.label NOT IN ('Nie rozpoczęto', 'W trakcie')
                         AND CURRENT_DATE > c.deadline
                    THEN 1 ELSE 0
                END) AS complaints_after_deadline
            FROM api_complaint c
            INNER JOIN api_complaintstatus cs
                ON cs.id = c.status_id
        """, single=True)

        # --- Other stats ---
        most_frequent_decisions = run_query("""
            SELECT cd.label
            FROM (
                SELECT decision_id, DENSE_RANK() OVER (ORDER BY cnt DESC) AS rank
                FROM (
                    SELECT decision_id, COUNT(*) AS cnt
                    FROM api_complaint
                    WHERE decision_id IS NOT NULL
                    GROUP BY decision_id
                )
            ) ranked
            INNER JOIN api_complaintdecision cd
            ON cd.id = ranked.decision_id
            WHERE rank = 1
                AND cd.label IS NOT NULL
        """, column="label")

        most_common_producers = run_query("""
            SELECT p.name
            FROM (
                SELECT producer_id, DENSE_RANK() OVER (ORDER BY cnt DESC) AS rank
                FROM (
                    SELECT producer_id, COUNT(*) AS cnt
                    FROM api_complaint
                    WHERE producer_id IS NOT NULL
                    GROUP BY producer_id
                ) sub
            ) ranked
            INNER JOIN api_producer p
            ON p.id = ranked.producer_id
            WHERE rank = 1
                AND ranked.producer_id IS NOT NULL
        """, column="name")

        most_common_products = run_query("""
            SELECT commodity_name
            FROM (
                SELECT commodity_name, DENSE_RANK() OVER (ORDER BY cnt DESC) AS rank
                FROM (
                    SELECT commodity_name, COUNT(*) AS cnt
                    FROM api_complaint
                    WHERE commodity_name IS NOT NULL
                    GROUP BY commodity_name
                ) sub
            ) ranked
            WHERE rank = 1
                AND commodity_name IS NOT NULL
        """, column="commodity_name")

        most_burdened_employees = run_query("""
            SELECT user_id
            FROM (
                SELECT user_id, DENSE_RANK() OVER (ORDER BY cnt DESC) AS rank
                FROM (
                    SELECT user_id, COUNT(*) AS cnt
                    FROM api_complaint c
                    INNER JOIN api_complaintstatus cs
                    ON cs.id = c.status_id
                    WHERE cs.label = 'W trakcie'
                    GROUP BY user_id
                ) sub
            ) ranked
            WHERE rank = 1
                AND user_id IS NOT NULL
        """, column="user_id")

        # --- Combine results ---
        stats = {
            **metrics,
            "most_frequent_decisions": most_frequent_decisions,
            "most_common_producers": most_common_producers,
            "most_common_products": most_common_products,
            "most_burdened_employees": most_burdened_employees,
        }

        return Response(stats)
