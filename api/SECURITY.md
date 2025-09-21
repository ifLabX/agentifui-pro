# Security Configuration Guide

## 🛡️ Security Features Implemented

### 1. Secure Configuration Management
- **Environment Variable Validation**: All sensitive data must be provided via environment variables
- **Secret Key Validation**: Prevents use of default/weak secret keys
- **CORS Restriction**: Blocks wildcard origins, only allows specific domains
- **Debug Mode Warnings**: Logs warnings when debug mode is enabled

### 2. Security Middleware

#### Security Headers Middleware
Automatically adds OWASP recommended security headers:
- `X-Content-Type-Options: nosniff` - Prevents MIME type sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking attacks
- `X-XSS-Protection: 1; mode=block` - Enables XSS filtering
- `Referrer-Policy: strict-origin-when-cross-origin` - Controls referrer information
- `Content-Security-Policy` - Basic CSP to prevent script injection

#### Trusted Host Middleware
- Validates Host headers against approved list
- Prevents Host header injection attacks
- Disabled in debug mode for development convenience
- Logs suspicious access attempts

### 3. CORS Security
- Restricted headers (no wildcard `*`)
- Specific allowed methods only
- Credential support with restricted origins
- Preflight request caching

## 🔧 Production Security Checklist

### Environment Configuration
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Required environment variables
SECRET_KEY=<32+ character secure string>
DEBUG=false
ENABLE_DOCS=false
ENABLE_REDOC=false
ENABLE_SECURITY_HEADERS=true
TRUSTED_HOSTS=["yourdomain.com", "api.yourdomain.com"]
CORS_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]
```

### Database Security
```bash
# Use strong database credentials
DATABASE_URL=postgresql+asyncpg://secure_user:strong_password@localhost:5432/agentifui_pro

# Connection pool settings (automatically configured)
# - pool_size: 20
# - max_overflow: 30
# - pool_timeout: 30
# - pool_recycle: 1800 (30 minutes)
# - pool_pre_ping: True
```

## ⚠️ Security Warnings Fixed

### High Risk Issues Resolved
1. **Weak Secret Keys**: Added validation to reject default/weak keys
2. **Debug Mode**: Added warnings and production-safe defaults
3. **CORS Wildcards**: Prevented wildcard origins
4. **Insecure Headers**: Restricted allowed headers to necessary ones only

### Medium Risk Issues Addressed
1. **Host Header Validation**: Added trusted host middleware
2. **Security Headers**: Comprehensive OWASP headers implementation
3. **Logging Security**: Replaced f-strings with parameterized logging

## 🚨 Runtime Security Validations

The application will **refuse to start** if:
- Secret key is the default value
- Secret key contains common weak patterns
- CORS origins include wildcards
- Database URL has invalid format

## 🔍 Security Monitoring

### Logged Security Events
- Untrusted host access attempts
- Configuration validation failures
- Debug mode enabled warnings
- Authentication failures (when implemented)

### Log Format
```
WARNING app.core.middleware.security:security.py:72 Untrusted host attempted access: suspicious.domain.com
WARNING app.main:main.py:45 ⚠️  DEBUG mode is enabled - do not use in production!
```

## 📚 Additional Security Recommendations

### For Production Deployment
1. **HTTPS Only**: Always use HTTPS in production
2. **Reverse Proxy**: Use nginx/Apache with security headers
3. **Rate Limiting**: Implement rate limiting (not included in base framework)
4. **Authentication**: Add JWT/OAuth2 authentication for protected endpoints
5. **Input Validation**: Always validate input data (Pydantic handles this)
6. **Database Security**: Use database connection encryption
7. **Monitoring**: Implement security monitoring and alerting

### Security Headers (Additional)
Consider adding these via reverse proxy:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Permitted-Cross-Domain-Policies: none
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## 🔄 Security Update Process

1. **Regular Dependencies**: Update dependencies monthly
2. **Security Patches**: Apply security patches immediately
3. **Secret Rotation**: Rotate secrets every 90 days
4. **Security Audits**: Conduct quarterly security reviews
5. **Penetration Testing**: Annual pen testing recommended

## 📞 Security Contact

For security issues, please follow responsible disclosure:
1. Do not create public GitHub issues for security vulnerabilities
2. Contact the development team privately
3. Allow reasonable time for patches before public disclosure

---

**Note**: This security configuration provides a solid foundation but should be reviewed and enhanced based on specific deployment requirements and threat models.