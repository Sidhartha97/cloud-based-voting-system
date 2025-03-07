import json
import pymysql
import os

# Load database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL Database
def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Check if the user has already voted
def has_user_voted(user_id, connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT hasVoted FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        return result and result["hasVoted"]

# Store vote and mark user as voted
def submit_vote(user_id, candidate_id, connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                return {"status": "error", "message": "User not found"}

            if has_user_voted(user_id, connection):
                return {"status": "error", "message": "You have already voted."}

            cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (%s, %s)", (user_id, candidate_id))
            cursor.execute("UPDATE users SET hasVoted = TRUE WHERE user_id = %s", (user_id,))

            connection.commit()
            return {"status": "success", "message": "Vote submitted successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Lambda handler function
def lambda_handler(event, context):
    print("🚀 Received event:", json.dumps(event))  # Debugging log

    # ✅ Extract HTTP method safely
    http_method = event.get("httpMethod")  # Standard API Gateway event

    # Fallback for cases where httpMethod is missing
    if not http_method and "requestContext" in event:
        if "http" in event["requestContext"]:  # Newer API Gateway format
            http_method = event["requestContext"]["http"].get("method")
        elif "httpMethod" in event["requestContext"]:  # Older format
            http_method = event["requestContext"]["httpMethod"]

    print(f"🔹 HTTP Method Detected: {http_method}")  # Debugging log

    # ✅ Handle OPTIONS request for CORS
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "CORS preflight successful"})
        }

    connection = None
    try:
        connection = connect_db()

        # ✅ Handle GET request (Return a simple message)
        if http_method == "GET":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": "GET method is active but not used for voting."})
            }

        # ✅ Handle POST request (Vote submission)
        elif http_method == "POST":
            try:
                body = json.loads(event.get("body", "{}"))
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                    },
                    "body": json.dumps({"message": "Invalid JSON format"})
                }

            user_id = body.get("user_id")
            candidate_id = body.get("candidate_id")

            if not user_id or not candidate_id:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({"message": "Missing user_id or candidate_id"})
                }

            response = submit_vote(user_id, candidate_id, connection)
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(response)
            }

        # ✅ Handle any other methods with a friendly response
        else:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"message": f"Received {http_method} request. No operation performed."})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }

    finally:
        if connection:
            connection.close()
            print("🔹 Database connection closed")
