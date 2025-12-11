# Deploying to Render with ImgBB

Great! The ImgBB integration code is pushed. Now you need to update your Render configuration.

## Step-by-Step Instructions

1.  **Open Render Dashboard**: Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2.  **Select Your Service**: Click on your `CarBazaar` web service.
3.  **Go to Environment**: Click the **"Environment"** tab on the left sidebar.
4.  **Add the Key**:
    -   Click **"Add Environment Variable"**.
    -   **Key**: `IMGBB_API_KEY`
    -   **Value**: `764458b9b68f03c204df6b653cec2790`
5.  **Clean Up (Optional)**:
    -   You can remove `UNSPLASH_ACCESS_KEY` and any `CLOUDINARY_*` keys as they are no longer used.
6.  **Save Changes**: Click **"Save Changes"**.

## Deployment

Render typically restarts your service automatically when you save environment variables. If not, you can manually trigger a deploy from the dashboard.
