# Contributing to Ather Energy Home Assistant Integration

Thank you for considering contributing to this project! Here's how you can help.

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- Check the [issue tracker](https://github.com/NoobPratik/ather-home-assistant/issues) first
- Use the bug report template
- Include your Home Assistant version and logs

### Suggesting Features

- Use the feature request template
- Explain why the feature would be useful
- Consider how it integrates with the existing sensor model

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.12+
- Home Assistant development environment

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ather-home-assistant.git
cd ather-home-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Coding Standards

- Follow PEP 8
- Use type hints
- Line length: 88 characters (Black default)

## Architecture

```
custom_components/ather/
├── __init__.py        # Integration setup, WebSocket loop, coordinator
├── config_flow.py     # Phone + OTP authentication flow
├── const.py           # Constants, sensor/binary sensor definitions
├── sensor.py          # Sensor platform (battery, range, tyre pressure, etc.)
├── binary_sensor.py   # Binary sensor platform (incognito, charger, alerts)
├── device_tracker.py  # GPS device tracker entity
└── manifest.json      # HA integration manifest
```

## Submitting Changes

1. Write clear commit messages
2. Update documentation if needed
3. Reference any related issues

Thank you for contributing!
