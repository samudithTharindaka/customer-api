# Installation Guide

## Prerequisites

- Frappe Framework v13 or higher
- ERPNext v13 or higher
- Python 3.7+
- Git

## Quick Install

### Method 1: Using Bench (Recommended)

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app
bench get-app https://github.com/YOUR_USERNAME/customer_api.git

# Install on your site
bench --site your-site.com install-app customer_api

# Restart bench
bench restart
```

### Method 2: Manual Installation

```bash
# Clone the repository
cd ~/frappe-bench/apps
git clone https://github.com/YOUR_USERNAME/customer_api.git

# Install dependencies
cd ~/frappe-bench
bench --site your-site.com install-app customer_api

# Build assets
bench build

# Restart
bench restart
```

## Verify Installation

1. **Check if app is installed:**
   ```bash
   bench --site your-site.com list-apps
   ```
   You should see `customer_api` in the list.

2. **Access API Documentation:**
   ```
   https://your-site.com/api-docs
   ```

3. **Test the API:**
   ```bash
   curl -X GET "https://your-site.com/api/method/customer_api.api.check_customer_registered?customer_name=Test" \
     -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"
   ```

## Configuration

### 1. Generate API Keys

1. Login to your ERPNext site
2. Go to: **User → Your User**
3. Scroll to **"API Access"** section
4. Click **"Generate Keys"**
5. Save the API Key and API Secret securely

### 2. Set Permissions

Ensure users have appropriate permissions:

- **For checking customers:**
  - Read access to Customer doctype

- **For creating customers:**
  - Create and Write access to Customer doctype
  - Create and Write access to Contact doctype (for contact info)
  - Create and Write access to Address doctype (for addresses)

### 3. CSRF Configuration (Development Only)

For development/testing environments, you may need to disable CSRF protection:

```bash
# Edit configuration
nano ~/frappe-bench/sites/common_site_config.json

# Add this line:
{
  ...
  "ignore_csrf": 1
}

# Restart bench
bench restart
```

**⚠️ Important:** Remove `"ignore_csrf": 1` in production environments. Use API Key authentication instead.

## Uninstall

```bash
# Uninstall from site
bench --site your-site.com uninstall-app customer_api

# Remove from apps directory (optional)
rm -rf ~/frappe-bench/apps/customer_api
```

## Upgrading

```bash
# Navigate to app directory
cd ~/frappe-bench/apps/customer_api

# Pull latest changes
git pull

# Run migrate
cd ~/frappe-bench
bench --site your-site.com migrate

# Build assets
bench build

# Restart
bench restart
```

## Troubleshooting

### Issue: App not found

**Solution:**
```bash
cd ~/frappe-bench
bench get-app customer_api
bench --site your-site.com install-app customer_api
```

### Issue: Permission denied

**Solution:**
- Check user permissions in ERPNext
- Ensure API user has required roles
- Verify API key is correct

### Issue: CSRF token error

**Solution:**
- Use API Key authentication (recommended)
- Or add `"ignore_csrf": 1` for development only

### Issue: Import errors

**Solution:**
```bash
cd ~/frappe-bench
./env/bin/pip install -e apps/customer_api
bench restart
```

## Production Deployment

### Recommended Settings

1. **Use HTTPS** - Always use SSL/TLS in production
2. **Use API Keys** - Never use session cookies for integrations
3. **Enable CSRF** - Remove `ignore_csrf` configuration
4. **Rate Limiting** - Implement rate limiting at nginx/proxy level
5. **Monitoring** - Set up logging and monitoring
6. **Backup** - Regular backups of your database

### Nginx Configuration

Add rate limiting in your nginx configuration:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/method/customer_api {
    limit_req zone=api_limit burst=20;
    # ... rest of your configuration
}
```

## Support

For issues during installation:
- Check the [README](README.md)
- Review [API Documentation](API_DOCUMENTATION.md)
- Visit the Swagger UI at `/api-docs`

## Next Steps

After installation:
1. Generate API keys
2. Test the endpoints using Swagger UI
3. Integrate with your application
4. Review the [API Documentation](API_DOCUMENTATION.md)

