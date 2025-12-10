# Cloudinary Setup Guide

## Why Cloudinary?
Cloudinary is a cloud-based image hosting service that stores your car images. Without it, uploaded images won't display.

## Step 1: Get Cloudinary Credentials

1. Go to https://cloudinary.com and sign up for a free account (if you don't have one)
2. After logging in, go to your Dashboard: https://cloudinary.com/console
3. You'll see three important values:
   - **Cloud Name** (e.g., `dxxxxx`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)

## Step 2: Configure on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your **CarBazaar** web service
3. Click on the **Environment** tab in the left sidebar
4. Click **Add Environment Variable** and add these three variables:

   | Key | Value |
   |-----|-------|
   | `CLOUDINARY_CLOUD_NAME` | Your cloud name from Cloudinary |
   | `CLOUDINARY_API_KEY` | Your API key from Cloudinary |
   | `CLOUDINARY_API_SECRET` | Your API secret from Cloudinary |

5. Click **Save Changes**
6. Render will automatically redeploy your application (this takes 2-3 minutes)

## Step 3: Verify It Works

1. Wait for the deployment to complete (check the "Events" tab)
2. Visit your deployed CarBazaar site
3. Log in to your account
4. Click "Add Car" and fill out the form
5. **Upload an image** when adding the car
6. Submit the form
7. The car should appear immediately with the uploaded image!

## Optional: Local Development Setup

If you want to test image uploads locally:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace the placeholder values with your actual Cloudinary credentials

3. Run the app locally:
   ```bash
   python src/app.py
   ```

4. Test adding a car with an image at http://localhost:5000

## Troubleshooting

### Images still not showing?
- Check Render logs for error messages (click "Logs" tab)
- Look for `[DEBUG] CLOUDINARY_ENABLED: True` in the logs
- Verify all three environment variables are set correctly (no typos!)

### Getting "Image upload failed" error?
- Double-check your API credentials are correct
- Make sure you copied the full API Secret (it's long!)
- Try regenerating your API credentials in Cloudinary dashboard

### Need help?
Check the Cloudinary documentation: https://cloudinary.com/documentation
