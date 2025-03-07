# 3-Tier Serverless Voting App

## Screenshots

![Screenshot (502)](https://github.com/user-attachments/assets/6efba770-6469-4d0c-b8ad-6dfdc2f17315)
                                **User create an account**

![Screenshot (504)](https://github.com/user-attachments/assets/7f406b3f-6d3c-48f9-8795-4f2b14a7c9ff)
                                    **User login**

![Screenshot (505)](https://github.com/user-attachments/assets/ea6b152b-b9e5-4873-ad2a-c6b4bca9121c)
                                  **User submit vote**

![Screenshot (507)](https://github.com/user-attachments/assets/08c8be3e-4165-41cd-a146-b978262943f8)
                           **User get error if try to vote again**

![Screenshot (508)](https://github.com/user-attachments/assets/f276a9e8-51a7-430f-b9ac-dceaf9f8f0df)
                                   **Vote result**

## Project Overview

- **Project Name:** Cloud-based Serverless Voting App
- **Description:** A serverless voting application hosted on the AWS cloud platform.
- **Features:**
  - User authentication via AWS Cognito
  - Secure voting system using AWS Lambda, API Gateway, and RDS
  - Cost-effective cloud-based infrastructure
- **Objective:** Reduce infrastructure costs by leveraging serverless architecture, as voting is not a frequent activity.

## Architecture Diagram


![Project diagram](https://github.com/user-attachments/assets/8a0827c1-5d8f-413b-972a-133f8141befe)

## Prerequisites

- **Frontend:** React
- **Backend:** AWS Lambda
- **API:** AWS API Gateway
- **User Authentication:** AWS Cognito
- **Database:** AWS RDS (MySQL)
- **Hosting:** AWS S3 Static Website Hosting
- **Domain Registration:** AWS Route 53
- **SSL Certificate:** AWS Certificate Manager
- **CDN:** AWS CloudFront

---

## Steps to Set Up the Application

### 1. User Authentication (AWS Cognito)

#### Create an AWS Cognito User Pool
1. Sign in to AWS Cognito Console and create a new **User Pool**.
2. Configure settings:
   - **User Pool Name:** `votingauth`
   - **Sign-in options:** Email, Phone Number, or Username
   - **Security settings:** Password policies and account recovery options
   - **User registration:** Self Sign-Up enabled, email/SMS verification
3. Create an **App Client** (e.g., `VotingSystemClient`)
   - Disable **Generate Client Secret** for frontend authentication
4. Configure **OAuth settings**
5. (Optional) Configure **Cognito Hosted UI** for authentication
6. Save and create the User Pool.

#### Store User Data in MySQL via Lambda Trigger
1. In Cognito, navigate to **Triggers** → **Post Confirmation Lambda Trigger**
2. Select a Lambda function that stores user ID and email in RDS.

![Screenshot (516)](https://github.com/user-attachments/assets/d2042d9d-3768-49b4-8013-9941c541fea9)

![image](https://github.com/user-attachments/assets/1bb4e92f-3ee1-4e17-bcb3-e4cd849e4a94)

![Screenshot (509)](https://github.com/user-attachments/assets/421347ad-0da2-43a6-ade3-4156bd4b14f0)

---

### 2. Database Setup (AWS RDS - MySQL)

#### Create a MySQL RDS Instance
1. Sign in to AWS Console → Navigate to **RDS** → Create Database.
2. Select **MySQL**, configure database settings:
   - **Database Name:** `voting-db`
   - **Master Username & Password**
   - **Instance Type:** `db.t3.micro` (for free-tier usage)
   - **Public Access:** Yes/No (based on access needs)
3. Allow **Inbound Rule** for MySQL (Port 3306) in Security Group.
4. Click **Create Database** and wait for it to be available.

#### Connect to the RDS Instance
- Use **MySQL Workbench** or CLI with the database **endpoint**.
- Create necessary tables:

```sql
CREATE DATABASE voting_system;
USE voting_system;

CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hasVoted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE votes (
    vote_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    candidate_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
);
```
![Screenshot (518)](https://github.com/user-attachments/assets/c64a5407-bcf3-4543-92e2-0101354765ec)

---

### 3. Backend (AWS Lambda Functions)

#### Create a MySQL-Python Layer for AWS Lambda

```sh
mkdir -p python
cd python
pip install pymysql -t .
zip -r mysql-layer.zip .
aws lambda publish-layer-version --layer-name pymysql-layer \  
  --zip-file fileb://mysql-layer.zip --compatible-runtimes python3.8 python3.9
```

#### Create Lambda Functions
1. Sign in to **AWS Lambda** → **Create Function** → Author from Scratch.
2. Set **Function Name** (e.g., `candidates`, `submitVote`, `getResult`).
3. Choose **Runtime**: Python 3.x.
4. Attach **pymysql-layer** to each function.
5. Implement logic for:
   - Fetching candidates
   - Submitting votes
   - Retrieving results

![Screenshot (513)](https://github.com/user-attachments/assets/7be2a6cf-9032-4456-87ae-a98818a8d2bc)

---

### 4. API Gateway Setup (For Frontend Integration)

#### Create API Gateway
1. Sign in to **API Gateway Console** → Create **REST API**.
2. Create **Resources**:
   - `/candidates` (GET)
   - `/votes` (POST)
   - `/getResult` (GET)
3. Integrate with **Lambda Functions**.
4. Enable **CORS**.
5. Deploy API to `dev` stage.
6. Copy **Invoke URL** for frontend.

![Screenshot (515)](https://github.com/user-attachments/assets/13af5f5f-6656-442d-9694-f8f8f24303b6)

![Screenshot (526)](https://github.com/user-attachments/assets/006900cd-9cb9-4fff-800f-a01f91b0e563)

---

### 5. Frontend (React App)

#### Setup React App
1. Install React and dependencies:

```sh
npx create-react-app voting-app
cd voting-app
npm install axios aws-amplify
```

2. Configure AWS Amplify for Cognito authentication.

3. Fetch candidates, submit votes, and display results using API Gateway endpoints.

#### Deploy React App to AWS S3
1. Build the project:

```sh
npm run build
```

2. Upload the `/build` folder to an **S3 bucket**.
3. Enable **Static Website Hosting**.
4. Link the S3 bucket with **CloudFront** for global distribution.

#### Domain Setup (AWS Route 53)
- Register a custom domain.
- Configure **CloudFront** to use **Route 53 domain**.
- Attach an **SSL Certificate** via **AWS Certificate Manager**.

![Screenshot (519)](https://github.com/user-attachments/assets/c93ed922-0b6f-4acf-925b-cbcd3a245fa0)

![image](https://github.com/user-attachments/assets/534015cc-a133-4fae-bc21-27c2470bc0b4)

![image](https://github.com/user-attachments/assets/60fbbc15-271f-4454-9185-d49414ba2afe)

![image](https://github.com/user-attachments/assets/f80fc026-babb-4341-84e7-41415839a504)


---

---

## Conclusion
This project demonstrates a cost-effective, fully serverless voting system using AWS services. By leveraging Cognito for authentication, Lambda for backend processing, API Gateway for API management, and RDS for persistent storage, we ensure a scalable and highly available architecture for voting operations.

---

## Author
**Your Name**  
sidhartha kumar rout  
Email: sidharthachintu1997@gmail.com  

---

## License
This project is licensed under the MIT License.
