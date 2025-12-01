# Google OAuth Login Setup Guide

## Overview

This guide will help you set up Google OAuth login for the Career Guidance System.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "Career Guidance System")
5. Click "Create"

### 2. Configure OAuth Consent Screen

1. In the Google Cloud Console, go to **APIs & Services** > **OAuth consent screen**
2. Select **External** (unless you have a Google Workspace)
3. Fill in the required information:
   - App name: "Career Guidance System"
   - User support email: Your email
   - Developer contact information: Your email
4. Click "Save and Continue"
5. On the Scopes page, click "Save and Continue" (no need to add scopes)
6. On the Test users page, click "Save and Continue"
7. Review and click "Back to Dashboard"

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** > **OAuth client ID**
3. Select **Web application** as the application type
4. Give it a name (e.g., "Career Guidance Web Client")
5. Under **Authorized JavaScript origins**, add:
   - `http://localhost:3001`
   - `http://localhost:3000` (if using port 3000)
6. Under **Authorized redirect URIs**, add:
   - `http://localhost:3001`
   - `http://localhost:3000` (if using port 3000)
7. Click **Create**
8. **Copy the Client ID** (you'll need this)

### 4. Configure Backend

1. Set the environment variable:

   ```bash
   export GOOGLE_CLIENT_ID='your-client-id-here'
   ```

   Or add it to your `.env` file:

   ```
   GOOGLE_CLIENT_ID=your-client-id-here
   ```

2. Install required packages (if not already installed):

   ```bash
   cd backend
   pip install google-auth google-auth-oauthlib google-auth-httplib2
   ```

3. Restart your backend server

### 5. Test Google Login

1. Start your frontend and backend servers
2. Go to the login page
3. You should see a "Sign in with Google" button
4. Click it and complete the Google sign-in flow
5. You should be automatically logged in and redirected to the dashboard

## Troubleshooting

### Button doesn't appear

- Check browser console for errors
- Verify `GOOGLE_CLIENT_ID` is set correctly
- Check that the Google Sign-In script loaded (check Network tab)

### "Invalid token" error

- Verify your Client ID is correct
- Check that authorized origins match your frontend URL exactly
- Make sure you're using the correct Client ID (not Client Secret)

### "OAuth not configured" error

- Verify `GOOGLE_CLIENT_ID` environment variable is set
- Restart the backend server after setting the variable
- Check backend logs for configuration errors

## Security Notes

- Never commit your Client ID or Client Secret to version control
- Use environment variables for sensitive configuration
- In production, use HTTPS and update authorized origins accordingly

## Production Setup

For production deployment:

1. Update authorized JavaScript origins to your production domain
2. Update authorized redirect URIs to your production domain
3. Ensure your production site uses HTTPS
4. Update the `FRONTEND_URL` environment variable in your backend
