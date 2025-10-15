# Contributing to Customer API

Thank you for your interest in contributing to Customer API!

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in GitHub Issues
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Actual behavior
   - Environment details (Frappe/ERPNext version)

### Submitting Changes

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

### Code Standards

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions
- Include type hints where appropriate
- Update documentation for new features
- Maintain backward compatibility

### Testing

- Test all endpoints thoroughly
- Verify Swagger UI documentation updates
- Check for security vulnerabilities
- Ensure no breaking changes

## Development Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/customer_api.git

# Install in development mode
cd ~/frappe-bench
bench get-app customer_api --skip-assets
bench --site your-site.com install-app customer_api

# Make changes and test
bench restart
```

## Questions?

Feel free to open an issue for any questions or clarifications.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

