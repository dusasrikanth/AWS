import boto3
import os

def attach_permissions_boundary(permissions_boundary_arn):
    iam_client = boto3.client('iam')
    excluded_user_arn = "arn:aws:iam::12345678910:user/admin"
    
    try:
        # List all IAM users
        users = iam_client.list_users()
        
        for user in users['Users']:
            user_name = user['UserName']
            user_arn = user['Arn']
            
            # Skip the excluded user
            if user_arn == excluded_user_arn:
                print(f"Skipping excluded user: {user_name}")
                continue
            
            # Check if the user already has the boundary set
            try:
                user_details = iam_client.get_user(UserName=user_name)
                if 'PermissionsBoundary' in user_details['User'] and \
                   user_details['User']['PermissionsBoundary']['PermissionsBoundaryArn'] == permissions_boundary_arn:
                    print(f"Skipping user {user_name}, boundary already set.")
                    continue
            except Exception as e:
                print(f"Error checking user {user_name}: {e}")
                continue

            # Attach permissions boundary to each user
            iam_client.put_user_permissions_boundary(
                UserName=user_name,
                PermissionsBoundary=permissions_boundary_arn
            )
            print(f"Successfully attached permissions boundary to user: {user_name}")
    except Exception as e:
        print(f"Error attaching permissions boundary: {e}")

def lambda_handler(event, context):
    permissions_boundary_arn = os.getenv("PERMISSIONS_BOUNDARY_ARN")
    if not permissions_boundary_arn:
        print("Error: PERMISSIONS_BOUNDARY_ARN environment variable is not set")
        return

    attach_permissions_boundary(permissions_boundary_arn)
