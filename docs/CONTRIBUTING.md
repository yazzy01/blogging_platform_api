# Contributing Guide

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/blogging_platform_api.git
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

## Project Structure

```
blogging_platform_api/
├── apps/
│   ├── categories/
│   ├── comments/
│   ├── posts/
│   └── users/
│       ├── models/
│       │   ├── __init__.py
│       │   ├── activity.py
│       │   └── base.py
│       ├── serializers/
│       │   ├── __init__.py
│       │   ├── activity.py
│       │   └── base.py
│       ├── views/
│       │   ├── __init__.py
│       │   ├── activity.py
│       │   ├── auth.py
│       │   └── base.py
│       ├── tests/
│       │   ├── __init__.py
│       │   ├── test_models.py
│       │   ├── test_views.py
│       │   └── test_auth.py
│       ├── admin.py
│       ├── apps.py
│       ├── urls.py
│       └── middleware.py
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
├── static/
├── media/
├── manage.py
└── requirements.txt
```

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all classes and methods
- Keep functions small and focused
- Use type hints where possible

### Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run tests before submitting PR:
  ```bash
  python manage.py test
  ```

### Git Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: your descriptive commit message"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request

### Commit Message Format

Follow the Conventional Commits specification:

- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting, etc)
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

Example:
```
feat: add social authentication with GitHub

- Add GitHub OAuth integration
- Create social auth pipeline
- Update user profile with GitHub data
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test apps.users.tests.test_models

# Run with coverage
coverage run manage.py test
coverage report
```

## Documentation

- Update API.md for new endpoints
- Add docstrings to all new code
- Update README.md if needed

## Code Review Guidelines

- Check code style
- Verify test coverage
- Review documentation updates
- Test functionality locally
- Check for security issues
- Verify error handling

## Release Process

1. Update version in setup.py
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Deploy to staging
7. Deploy to production

## Getting Help

- Create an issue for bugs
- Join our Discord channel
- Check the documentation
- Contact maintainers
