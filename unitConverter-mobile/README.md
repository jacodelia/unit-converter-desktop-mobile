# Unit Converter - Mobile

A mobile unit converter application built with Python and PySide6 (Qt), following the MVVM architecture pattern with a glassmorphism dark gradient UI optimized for phone-sized viewports (390x844).

## Features

- **6 Conversion Categories**: Length, Temperature, Area, Volume, Weight, Time
- **57 Units** across all categories with precise conversion factors
- **Natural Language Search**: Type queries like "from kilometers to meters" to navigate directly
- **8 Languages**: English, Spanish, French, Italian, German, Russian, Japanese, Chinese
- **Conversion History**: Tracks recent conversions
- **Bottom Navigation Bar**: Home, History, Settings
- **Horizontal Category Pills**: Scrollable category selection
- **Swap Button**: Instantly reverse source and target units

## Project Structure

```
unitConverter-mobile/
├── main.py                          # Application entry point
├── pyproject.toml                   # Project config & dependencies (uv)
├── README.md                        # This file
├── docs/
│   └── architecture.md              # Mermaid diagrams & build docs
├── src/
│   ├── __init__.py
│   ├── models/                      # Data models (MVVM - Model)
│   │   ├── __init__.py
│   │   ├── unit.py                  # Unit dataclass
│   │   ├── category.py              # Category dataclass
│   │   └── conversion_result.py     # ConversionResult dataclass
│   ├── operations/                  # Conversion logic (one file per category)
│   │   ├── __init__.py
│   │   ├── length_operations.py     # Length conversions (11 units)
│   │   ├── temperature_operations.py # Temperature conversions (3 units)
│   │   ├── area_operations.py       # Area conversions (11 units)
│   │   ├── volume_operations.py     # Volume conversions (11 units)
│   │   ├── weight_operations.py     # Weight conversions (10 units)
│   │   └── time_operations.py       # Time conversions (11 units)
│   ├── services/                    # Business logic services
│   │   ├── __init__.py
│   │   ├── converter_service.py     # Central conversion dispatcher
│   │   └── search_service.py        # Natural language search parser
│   ├── i18n/                        # Internationalization
│   │   ├── __init__.py
│   │   └── translations.py          # 8-language translation dictionary
│   ├── viewmodels/                  # ViewModels (MVVM - ViewModel)
│   │   ├── __init__.py
│   │   ├── converter_viewmodel.py   # Main conversion state & logic
│   │   ├── search_viewmodel.py      # Search state & navigation
│   │   └── preferences_viewmodel.py # Language preferences
│   ├── views/                       # UI layer (MVVM - View)
│   │   ├── __init__.py
│   │   ├── mobile_view.py           # Main mobile window (QMainWindow)
│   │   └── styles.py                # Qt stylesheet constants (glassmorphism)
│   └── assets/                      # Icons, images
│       └── (empty)
└── tests/
    ├── __init__.py
    ├── unit/                        # Unit tests
    │   ├── __init__.py
    │   ├── test_models.py           # Model tests
    │   ├── test_operations.py       # Conversion operation tests
    │   ├── test_services.py         # Service layer tests
    │   ├── test_i18n.py             # Translation tests
    │   └── test_viewmodels.py       # ViewModel tests
    ├── integration/                 # Integration tests
    │   ├── __init__.py
    │   └── test_integration.py      # Cross-layer workflow tests
    └── e2e/                         # End-to-end tests
        ├── __init__.py
        └── test_e2e_mobile.py       # Full application E2E tests
```

## Architecture

This project follows the **MVVM (Model-View-ViewModel)** pattern:

- **Model**: Pure data classes (`Unit`, `Category`, `ConversionResult`) with no dependencies on Qt
- **ViewModel**: Qt `QObject` subclasses with `Signal`/`Slot` for reactive data binding
- **View**: PySide6 widgets with glassmorphism styling, bound to ViewModels via signals

See [docs/architecture.md](docs/architecture.md) for Mermaid diagrams and detailed architecture documentation.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
# Clone the repository
git clone <repo-url> unitConverter-mobile
cd unitConverter-mobile

# Install dependencies with uv
uv sync --dev
```

## Running the Application

```bash
uv run python main.py
```

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run only unit tests
uv run pytest tests/unit/ -v

# Run integration tests
uv run pytest tests/integration/ -v

# Run E2E tests
uv run pytest tests/e2e/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

## Building Binary

```bash
# Build standalone executable
uv run pyinstaller --onefile --windowed --name "UnitConverter-Mobile" --add-data "src:src" main.py

# Output: dist/UnitConverter-Mobile
```

See [docs/architecture.md](docs/architecture.md) for cross-platform build instructions.

## Supported Conversions

| Category | Units |
|----------|-------|
| Length | Meter, Kilometer, Centimeter, Millimeter, Micrometer, Nanometer, Mile, Yard, Foot, Inch, Light Year |
| Temperature | Celsius, Kelvin, Fahrenheit |
| Area | Square Meter, Square Kilometer, Square Centimeter, Square Millimeter, Square Micrometer, Hectare, Square Mile, Square Yard, Square Foot, Square Inch, Acre |
| Volume | Cubic Meter, Cubic Kilometer, Cubic Centimeter, Cubic Millimeter, Liter, Milliliter, US Gallon, US Quart, US Pint, US Cup, US Fluid Ounce |
| Weight | Kilogram, Gram, Milligram, Metric Ton, Long Ton, Short Ton, Pound, Ounce, Carat, Atomic Mass Unit |
| Time | Second, Millisecond, Microsecond, Nanosecond, Picosecond, Minute, Hour, Day, Week, Month, Year |

## Design

The mobile UI follows a glassmorphism design with:
- Dark gradient background (#0F0C29 → #302B63 → #24243e)
- Translucent frosted-glass cards with blur effect
- Accent violet (#7F5AF0) and blue (#6C63FF) highlights
- Touch-friendly controls (min 48px tap targets)
- Fixed 390x844 viewport matching iPhone 14 Pro dimensions

## License

MIT
