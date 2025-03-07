import json
import pymysql
import os

# Database configuration (use environment variables for security)
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

def lambda_handler(event, context):
    try:
        # Connect to MySQL database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # ✅ Correctly joining `votes` and `candidates` tables
            sql = """
            SELECT v.candidate_id, c.name AS candidate_name, COUNT(v.vote_id) AS vote_count
            FROM votes v
            JOIN candidates c ON v.candidate_id = c.candidate_id
            GROUP BY v.candidate_id, c.name
            ORDER BY vote_count DESC;
            """
            cursor.execute(sql)
            results = cursor.fetchall()

        connection.close()

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Authorization, Content-Type"
            },
            "body": json.dumps(results)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Authorization, Content-Type"
            },
            "body": json.dumps({"error": str(e)})
        }
