import sys
sys.path.append("/opt/python")  # Ensure Lambda Layer is found

import json
import pymysql
import os

# Database credentials (Use Secrets Manager in production!)
DB_HOST = os.getenv("DB_HOST", "your-mysql-host")
DB_USER = os.getenv("DB_USER", "your-db-username")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your-db-password")
DB_NAME = os.getenv("DB_NAME", "your-database-name")

# Connect to MySQL
def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def lambda_handler(event, context):
    print("Received Cognito Event:", json.dumps(event, indent=2))

    # Extract user attributes from Cognito event
    user_attributes = event.get("request", {}).get("userAttributes", {})
    user_id = user_attributes.get("sub")  # Unique Cognito User ID
    username = event.get("userName")  # Cognito username
    email = user_attributes.get("email")  # User email

    # Validate data
    if not user_id or not username or not email:
        print("Error: Missing required user attributes")
        return {"statusCode": 400, "body": json.dumps({"message": "Missing user_id, username, or email"})}

    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            # Insert user data into MySQL
            sql = "INSERT INTO users (user_id, username, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, username, email))
            connection.commit()
        print(f"User {username} ({email}) inserted successfully.")
    except Exception as e:
        print("Database error:", str(e))
        return {"statusCode": 500, "body": json.dumps({"message": "Database error", "error": str(e)})}
    finally:
        connection.close()

    # Return event for Cognito Post Confirmation trigger
    return event
