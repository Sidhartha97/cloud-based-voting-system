import json
import pymysql
import os

# MySQL Database Configuration (Replace with your actual values)
DB_HOST = os.getenv("DB_HOST", "voting-db.ctua2o6qmixp.us-east-1.rds.amazonaws.com")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sidhartha1997")
DB_NAME = os.getenv("DB_NAME", "voting_system")

def lambda_handler(event, context):
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Query to fetch candidates from the MySQL table
            sql = "SELECT candidate_id, name AS candidate_name, party FROM candidates"
            cursor.execute(sql)
            candidates = cursor.fetchall()  # Fetch all candidates

        # Close connection
        connection.close()

          # ✅ Fix CORS: Allow requests from React frontend
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps(candidates)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({"error": "Internal Server Error"})
        }

        # Return data as JSON response
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},  # Enable CORS for frontend
            "body": json.dumps(candidates)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
