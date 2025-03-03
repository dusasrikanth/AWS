# Attach IAM Boundary - Lambda Function

This project contains an AWS Lambda function that automatically attaches a specified IAM permissions boundary to all IAM users **except** the admin user.

## Features

- Lists all IAM users in the account.
- Skips a predefined IAM user (`admin` in this case).
- Checks if a permissions boundary is already attached before applying it.
- Automatically attaches the specified permissions boundary.


## Setup & Deployment

### 1️⃣ Create the Lambda Function

1. Go to **AWS Lambda Console**.
2. Click **Create Function** → Select **Author from Scratch**.
3. Set a name (e.g., `AttachIamBoundary`).
4. Choose **Runtime**: `Python 3.x`.
5. Assign an **IAM Role** with required permissions(IAMFullAccess)
6. Click **Create Function**.

### 2️⃣ Upload the Code

1. Copy and paste the script from `attach_iam_boundary.py` into the Lambda function editor.
2. Click **Deploy**.

### 3️⃣ Set Environment Variables

1. In the Lambda function, go to the **Configuration** tab.
2. Click **Environment Variables** → Add Variable:
   - **Key:** `PERMISSIONS_BOUNDARY_ARN`
   - **Value:** `arn:aws:iam::ACCOUNT_ID:policy/YourBoundaryPolicy`

### 4️⃣ (Optional) Trigger Lambda with EventBridge

To automatically run the function when a new IAM user is created:

1. Go to **AWS EventBridge Console**.
2. Create a new rule:
   - **Event Pattern:**
     ```json
     {
       "source": ["aws.iam"],
       "detail-type": ["AWS API Call via CloudTrail"],
       "detail": {
         "eventSource": ["iam.amazonaws.com"],
         "eventName": ["CreateUser"]
       }
     }
     ```
3. Set the **Target** to the Lambda function.
4. Click **Create Rule**.

## Testing

- Manually **trigger the Lambda function** in AWS Lambda console.
- **Check CloudWatch Logs** for success/failure messages.
- Try creating an IAM user and confirm the boundary gets attached.

## Notes

- The script **skips users who already have the boundary** to avoid redundant API calls.
- The **admin user is excluded** from having a permissions boundary applied.
- Ensure that **CloudTrail is enabled** so that EventBridge can capture IAM user creation events.

## Cleanup

If you no longer need the Lambda function:

- Delete the function from AWS Lambda.
- Remove the EventBridge rule if created.
---

✅ *Happy learning..* 🚀

