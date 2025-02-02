## Problem Statement

#### Restrict access to the dev1-files folder (prefix) within the isrikanthd5364 S3 bucket only to the IAM user dev1, allowing the user to upload, download, delete, and list files within that specific folder, while denying access to any other part of the bucket.

## Solution and Explanation:

#### A two-layered approach using a bucket policy and an access point policy.  Here's how they work together:

1. Bucket Policy (The Gatekeeper):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::isrikanthd5364",
                "arn:aws:s3:::isrikanthd5364/*"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:DataAccessPointAccount": "084828562044"
                }
            }
        }
    ]
}
```

#### A two-layered approach using a bucket policy and an access point policy.  Here's how they work together:

#### This S3 bucket policy defines access permissions for the `isrikanthd5364` bucket.


####   **`Effect`:** `"Allow"` indicates that this statement grants permission.

*   **`Principal`:** `{ "AWS": "*" }`  specifies *who* is granted the permission.  `"*"` means *all* AWS principals. This includes all AWS accounts, users, roles, and even anonymous users.  It's important to note that this `Principal` alone *does not* grant access. The `Condition` element is what actually restricts who can use this permission.

*   **`Action`:** `"s3:*"` specifies the allowed actions. The `*` is a wildcard that means *all* S3 actions. This includes actions like `s3:GetObject` (reading objects), `s3:PutObject` (writing objects), `s3:ListBucket` (listing objects in the bucket), and many others.

*   **`Resource`:** This specifies *what* the actions apply to.
    *   `"arn:aws:s3:::isrikanthd5364"` refers to the bucket itself.
    *   `"arn:aws:s3:::isrikanthd5364/*"` refers to all objects *within* the `isrikanthd5364` bucket.

*   **`Condition`:** This is the part that restricts access.
    *   `"StringEquals": { "s3:DataAccessPointAccount": "084828562044" }` This condition states that the policy *only* applies if the request to access the S3 bucket is made through an access point that belongs to the AWS account `084828562044`.  This is the key to how access is controlled.  Even though the `Principal` is `*`, the condition restricts access to only requests coming through a specific access point.

In summary, this policy says:  *Anyone* is *potentially* allowed to perform *any* S3 action on the `isrikanthd5364` bucket and its objects, *but only if* the request originates from an access point that belongs to the AWS account `084828562044`.  This effectively means that access to the bucket is restricted to those using a specifically configured access point.


2. Access Point Policy (Fine-Grained Permissions):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowObjectAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::084828562044:user/dev1"
            },
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:PutObjectAcl",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:ap-south-1:084828562044:accesspoint/dev1-ap/object/dev1-files/*"
        },
        {
            "Sid": "AllowListBucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::084828562044:user/dev1"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:ap-south-1:084828562044:accesspoint/dev1-ap",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "dev1-files/*",
                        "dev1-files/"
                    ]
                }
            }
        }
    ]
}
```

*   **`Principal: { "AWS": "arn:aws:iam::084828562044:user/dev1" }`:** This grants permissions *only* to the `dev1` IAM user.

*   **`AllowObjectAccess` Statement:** This statement grants the `dev1` user permissions to perform object-level actions (upload, download, delete, manage ACLs) *specifically on objects within* the `dev1-files` prefix.

*   **`AllowListBucket` Statement:** This statement is *crucial* for listing objects.
    *   **`Action: "s3:ListBucket"`:**  Grants the permission to list objects.
    *   **`Resource: "arn:aws:s3:ap-south-1:084828562044:accesspoint/dev1-ap"`:**  Specifies that the listing permission applies to the `dev1-ap` access point.  Listing happens at the access point level.
    *   **`Condition: { "StringLike": { "s3:prefix": [...] } }`:**  This is *essential* for restricting the listing to the `dev1-files` folder.  It ensures that the `dev1` user can only list objects *within* that specific prefix.

**How They Work Together:**

1.  A request comes in to access the `isrikanthd5364` bucket.

2.  The bucket policy is evaluated.  It checks the `s3:DataAccessPointAccount` condition.  If the request *doesn't* come through an access point belonging to your account, the request is denied.

3.  If the request *does* come through a valid access point (like `dev1-ap`), the bucket policy allows the request to proceed.

4.  The *access point policy* is then evaluated.  It checks the `Principal` to ensure that the request is being made by the `dev1` user.

5.  The access point policy then checks the `Action` and `Resource` to determine what the user is allowed to do.  If the user is trying to list objects, the `AllowListBucket` statement is evaluated, and the `s3:prefix` condition ensures that only objects within the `dev1-files` folder are listed.  If the user is trying to upload or download, the `AllowObjectAccess` statement is evaluated.

**In Summary:**

The bucket policy acts as a gatekeeper, ensuring that all access goes through an access point.  The access point policy then defines the specific permissions for each access point, allowing fine-grained control over what each user can do and which parts of the bucket they can access.  This combination provides a secure and flexible way to manage access to your S3 data.  By using specific actions and restricting access to the necessary prefixes, you follow the principle of least privilege and improve the security of your S3 bucket.

