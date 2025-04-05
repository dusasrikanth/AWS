# 🌐 Static Website Hosting on AWS (S3 + CloudFront + Route53 + ACM)

This guide helps you set up a secure, fast, and scalable static website using:

- ✅ Amazon S3 (for storage)
- ✅ CloudFront (for CDN and caching)
- ✅ Route 53 (for domain routing)
- ✅ AWS Certificate Manager (for HTTPS)

---

## 🚀 Prerequisites

- A registered domain (e.g., from Route 53 or elsewhere) with ACM certificate created to it.

---

## 🪣 Step 1: Create a Private S3 Bucket

1. Go to AWS S3 Console.
2. Click **Create bucket**.
3. Choose a **unique name** (e.g., `my-website-bucket`).
4. Keep **Block all public access** ✅ enabled. This is important because we are not going to expose the bucket to public.
5. Click **Create bucket**.

### 🔼 Upload your website files

- Upload `index.html`, `404.html`, `style.css`, `script.js`, etc.

---

## 🌍 Step 2: Set Up CloudFront Distribution

1. Go to AWS CloudFront Console
2. Click **Create Distribution**.
3. Under **Origin** section:
   - Select the S3 bucket that you have created above as **Origin domain**.
   - Select **Origin access control (recommended)** as Origin access.
   - Click on **Create new OAC** button under **Origin access control**.
   - Select **Signing behavior** as **Sign requests (recommended)** and click on Create.
4. Set **Viewer Protocol Policy** to `Redirect HTTP to HTTPS`.
5. Select **Web Application Firewall (WAF)** as **Do not enable security protections**
6. Set **Default root object** to `index.html`.
7. Click **Create Distribution**.

---

## 🔒 Step 3: Attach OAC Permissions to S3 Bucket

1. Go to your **S3 bucket** → **Permissions** → **Bucket Policy**.
2. Add the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipal",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::<ACCOUNT_ID>:distribution/<DISTRIBUTION_ARN>"
        }
      }
    }
  ]
}
```

> Replace `<BUCKET_NAME>`, `<ACCOUNT_ID>`, and `<DISTRIBUTION_ARN>` accordingly.

---

## 🧭 Step 4: Point Domain via Route 53

1. Go to AWS Route 53
2. Find your hosted zone for the domain.
3. Create a **Record**:
   - **Type**: A (Alias)
   - **Alias target**: Select your CloudFront distribution from dropdown.
   - **Name**: `www` (as needed)

---

## 🔗 Step 6: Add Custom Domain to CloudFront

1. Go to CloudFront → Open your distribution.
2. Click on **Edit** under **Settings** section. 
3. Under **Alternate domain name (CNAME)**, add:
   ```
   www.example.com
   ```
3. Under **Custom SSL Certificate**, choose the ACM certificate you created.
4. Save changes.

---

## ✅ Done! Access your site at `https://www.example.com`

---
