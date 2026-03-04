# Unit Converter - Mobile

A cross-platform unit converter application built with Python, following the MVVM architecture pattern. The app runs on **desktop** (PySide6/Qt with a glassmorphism dark gradient UI) and **Android/iOS** (Toga native widgets via Briefcase). ViewModels use a pure-Python `EventMixin` (emit/on/off) so the entire business-logic layer is framework-agnostic.

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
├── main.py                          # Platform-aware entry point (PySide6 or Toga)
├── pyproject.toml                   # Project config, optional deps, Briefcase config
├── README.md                        # This file
├── architecture.md                  # Mermaid diagrams & build documentation
├── unitconverter/
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
│   ├── viewmodels/                  # ViewModels (MVVM - ViewModel, pure Python)
│   │   ├── __init__.py
│   │   ├── event_mixin.py           # Pure-Python emit/on/off event system
│   │   ├── converter_viewmodel.py   # Main conversion state & logic
│   │   ├── search_viewmodel.py      # Search state & navigation
│   │   └── preferences_viewmodel.py # Language preferences
│   ├── views/                       # UI layer (MVVM - View)
│   │   ├── __init__.py
│   │   ├── mobile_view.py           # Desktop view (PySide6 QMainWindow)
│   │   ├── toga_view.py             # Mobile view (Toga for Android/iOS)
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

This project follows the **MVVM (Model-View-ViewModel)** pattern with a **dual-UI** design:

- **Model**: Pure data classes (`Unit`, `Category`, `ConversionResult`) with no framework dependencies
- **ViewModel**: Pure-Python classes using `EventMixin` (emit/on/off) — no PySide6 or Toga dependency
- **View (desktop)**: `mobile_view.py` — PySide6 widgets with glassmorphism styling, listens to ViewModel events via `.on()`
- **View (mobile)**: `toga_view.py` — Toga native widgets for Android/iOS, also using `.on()`

The `EventMixin` in `viewmodels/event_mixin.py` replaces PySide6's `QObject`/`Signal`/`Slot`, making the ViewModel layer completely framework-agnostic. The `main.py` entry point detects the platform at startup and launches the appropriate UI.

See [architecture.md](architecture.md) for Mermaid diagrams and detailed architecture documentation.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- **Desktop**: PySide6 (installed automatically via dev dependencies)
- **Android**: Java JDK 17+, Android SDK (API 34) — see [Building](#building) below
- **iOS**: macOS with Xcode 15+ — see [Building](#building) below

## Installation

```bash
# Clone the repository
git clone <repo-url> unitConverter-mobile
cd unitConverter-mobile

# Install dev dependencies (includes PySide6 for desktop)
uv sync --dev

# Or install only core dependencies (no PySide6, no Toga — for CI/testing)
uv sync
```

**Dependency layout** (see `pyproject.toml`):

| Group | Packages | When used |
|-------|----------|-----------|
| `[project] dependencies` | *(none)* | Core — models, operations, services, ViewModels are pure Python |
| `[project.optional-dependencies] desktop` | PySide6 | Desktop UI only |
| `[dependency-groups] dev` | PySide6, pytest, briefcase, etc. | Local development |
| `[tool.briefcase...android] requires` | toga-android | Injected by Briefcase at APK build time |
| `[tool.briefcase...iOS] requires` | toga-iOS | Injected by Briefcase at IPA build time |

## Running the Application

```bash
# Desktop (auto-detects phone/tablet layout from screen size)
uv run python main.py

# Force phone layout
uv run python main.py --phone

# Force tablet layout
uv run python main.py --tablet
```

On Android/iOS, Briefcase launches `main.py` which detects the platform and uses the Toga UI automatically.

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
uv run pytest tests/ --cov=unitconverter --cov-report=html
```

## Building

### Desktop Binary (PyInstaller)

```bash
# Build standalone executable for the current OS
uv run pyinstaller --onefile --windowed --name "UnitConverter-Mobile" --add-data "unitconverter:unitconverter" main.py

# Output: dist/UnitConverter-Mobile (Linux), .app (macOS), .exe (Windows)
```

### Android APK (Briefcase)

Build a universal APK that runs on both **phone** and **tablet** devices. The app detects the form factor at runtime and adapts accordingly.

**Prerequisites**:
- Java JDK 17+
- Android SDK (API 34) with build-tools 34.0.0
- Briefcase: `uv add --dev briefcase`

```bash
# 1. Create the Android project scaffold
uv run briefcase create android

# 2. Build a debug APK
uv run briefcase build android

# 3. Run on a connected device or emulator
uv run briefcase run android

# 4. Package a signed AAB for Google Play Store
uv run briefcase package android
```

**Output files**:
| Build Type | Output Path |
|------------|-------------|
| Debug APK | `android/gradle/app/build/outputs/apk/debug/app-debug.apk` |
| AAB (Play Store) | `android/gradle/app/build/outputs/bundle/release/app-release.aab` |

**Device support**:
| Device | Screen Size | Layout | Orientation |
|--------|-------------|--------|-------------|
| Phone | < 7" | 390x844 compact | Portrait preferred |
| Tablet | >= 7" | 1024x768 expanded | Any orientation |

### iOS Build (Briefcase)

Build a universal iOS app for both **iPhone** and **iPad**. Requires macOS with Xcode installed.

**Prerequisites**:
- macOS with Xcode 15+ and Command Line Tools
- Apple Developer account (for device deployment)
- Briefcase: `uv add --dev briefcase`

```bash
# 1. Create the iOS project scaffold (Xcode project)
uv run briefcase create iOS

# 2. Build a debug build
uv run briefcase build iOS

# 3. Run on the iOS Simulator
uv run briefcase run iOS

# 4. Run on a physical device (requires signing)
uv run briefcase run iOS -d <device-udid>

# 5. Package a signed IPA for App Store
uv run briefcase package iOS
```

**Output files**:
| Build Type | Output Path |
|------------|-------------|
| Debug build | `iOS/Xcode/build/Debug-iphonesimulator/Unit Converter.app` |
| IPA (App Store) | `iOS/Xcode/build/Unit Converter.ipa` |

**Device support**:
| Device | Minimum OS | Device Family | Orientation |
|--------|-----------|---------------|-------------|
| iPhone | iOS 15.0 | 1 | Portrait preferred |
| iPad | iOS 15.0 | 2 | Any orientation, multitasking supported |

See [architecture.md](architecture.md) for architecture diagrams and additional build details.

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
