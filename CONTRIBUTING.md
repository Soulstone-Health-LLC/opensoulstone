# Contributing to Soulstone

Thank you for your interest in contributing to Soulstone! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style and Standards](#code-style-and-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful**: Treat all contributors with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be collaborative**: Work together to improve the project
- **Be professional**: Keep discussions focused and constructive

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Docker** and **Docker Compose** installed
- **Git** for version control
- **Make** for build commands (optional but recommended)
- A **text editor** or **IDE** of your choice

### First-time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/soulstone.git
   cd soulstone
   ```

3. **Add the upstream remote**:

   ```bash
   git remote add upstream https://github.com/rodneygauna/soulstone.git
   ```

4. **Set up your environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your development settings
   make validate
   ```

## Development Setup

### Quick Development Environment

```bash
# Start development environment (no SSL, simplified)
make dev-up

# Or start with sample data for testing
make test-env
```

### Development Workflow

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** using the development environment

3. **Test your changes**:

   ```bash
   # Run validation
   make validate

   # Run tests
   make shell
   pytest

   # Test in browser at http://localhost:8000
   ```

4. **Commit your changes**:

   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

### Useful Development Commands

```bash
# Validate setup
make validate

# View logs
make logs

# Access container shell for debugging
make shell

# Reset development environment
make clean
make dev-up

# Run with fresh test data
make test-env
```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix existing issues
- **Feature additions**: Add new functionality
- **Documentation**: Improve docs, comments, or examples
- **Testing**: Add or improve tests
- **UI/UX improvements**: Enhance user interface and experience
- **Performance optimizations**: Improve speed or efficiency
- **Security improvements**: Enhance security measures

### Areas That Need Help

- **Documentation**: Expand user guides and API documentation
- **Testing**: Increase test coverage
- **Accessibility**: Improve accessibility compliance
- **Internationalization**: Add support for multiple languages
- **Mobile responsiveness**: Improve mobile user experience
- **Performance**: Optimize database queries and UI responsiveness

## Code Style and Standards

### Python Code Style

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation
- Maximum line length: **79 characters**
- Use **meaningful variable names**
- Add **docstrings** for functions and classes

Example:

```python
def create_user(email, password, first_name, last_name):
    """
    Create a new user with the provided information.

    Args:
        email (str): User's email address
        password (str): User's password (will be hashed)
        first_name (str): User's first name
        last_name (str): User's last name

    Returns:
        User: The created user object
    """
    # Implementation here
```

### HTML/CSS Style

- Use **semantic HTML** elements
- Follow **accessibility best practices**
- Use **consistent indentation** (2 spaces)
- Add **meaningful CSS class names**
- Ensure **mobile responsiveness**

### JavaScript Style

- Use **modern ES6+** syntax
- Use **meaningful variable names**
- Add **comments** for complex logic
- Follow **consistent formatting**

### Database

- Use **descriptive table and column names**
- Add **proper indexing** for performance
- Include **foreign key constraints**
- Document **complex queries**

## Testing

### Running Tests

```bash
# Access the container
make shell

# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run with coverage
pytest --cov=web tests/

# Run tests with verbose output
pytest -v
```

### Writing Tests

- Write tests for **new features**
- Include **edge cases**
- Use **descriptive test names**
- Test both **positive and negative scenarios**

Example test:

```python
def test_user_creation_with_valid_data():
    """Test that a user can be created with valid data."""
    user = create_user(
        email="test@example.com",
        password="secure_password",
        first_name="Test",
        last_name="User"
    )
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
```

### Test Coverage

- Aim for **80%+ test coverage**
- Focus on **critical functionality**
- Test **error handling**
- Include **integration tests**

## Submitting Changes

### Pull Request Process

1. **Update your fork**:

   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

2. **Rebase your feature branch**:

   ```bash
   git checkout feature/your-feature-name
   git rebase main
   ```

3. **Push your changes**:

   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub with:
   - **Clear title** describing the change
   - **Detailed description** of what was changed and why
   - **Screenshots** for UI changes
   - **Testing instructions** for reviewers

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests have been added/updated
- [ ] Documentation has been updated
- [ ] All tests pass
- [ ] No new linting errors
- [ ] Change has been tested manually
- [ ] Screenshots included for UI changes

### Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good examples:
git commit -m "Add: user profile picture upload functionality"
git commit -m "Fix: email validation regex pattern"
git commit -m "Update: improve database query performance"
git commit -m "Remove: deprecated authentication method"

# Format: Type: brief description
# Types: Add, Fix, Update, Remove, Refactor, Test, Doc
```

## Reporting Issues

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Try the latest version** to see if the issue is fixed
3. **Run `make validate`** to check your setup

### Issue Report Template

When reporting bugs, please include:

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04, macOS 12.0, Windows 11]
- Docker version: [e.g., 20.10.0]
- Browser: [e.g., Chrome 95, Firefox 94]

## Additional Context
- Screenshots
- Error messages
- Relevant logs
```

### Security Issues

For security-related issues:

- **Do NOT** create a public issue
- Email security concerns to: [rodney@soulstonehealth.com]
- Include detailed reproduction steps
- Allow time for investigation before disclosure

## Feature Requests

### Before Requesting

1. **Check existing feature requests**
2. **Consider if it fits the project scope**
3. **Think about implementation complexity**

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? Who would use it?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other ways to achieve the same goal

## Additional Context
Screenshots, mockups, or examples
```

## Development Tips

### Database Changes

- Always create **migration scripts**
- Test migrations on **sample data**
- Consider **backwards compatibility**
- Document **schema changes**

### UI Changes

- Test on **multiple screen sizes**
- Ensure **keyboard accessibility**
- Check **color contrast** ratios
- Test with **screen readers**

### Performance

- **Profile** before optimizing
- Focus on **user-facing** improvements
- Test with **realistic data volumes**
- Monitor **database query performance**

## Getting Help

### Community

- **GitHub Discussions**: Ask questions and share ideas
- **GitHub Issues**: Report bugs and request features
- **Code Review**: Learn from pull request feedback

### Documentation

- **README.md**: Setup and basic usage
- **Code comments**: Implementation details
- **Inline documentation**: Function and class docs

### Mentorship

New contributors are welcome! If you're new to open source:

- Start with **"good first issue"** labels
- Ask questions in **discussions**
- Request **code review** feedback
- Pair with **experienced contributors**

## Recognition

Contributors will be:

- **Listed** in the project contributors
- **Credited** in release notes for significant contributions
- **Thanked** in community discussions

Thank you for contributing to Soulstone! 🎉
