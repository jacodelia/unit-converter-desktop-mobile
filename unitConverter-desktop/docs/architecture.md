# Architecture Documentation

## MVVM Architecture Diagram

```mermaid
graph TB
    subgraph View Layer
        DV[DesktopWindow<br/>PySide6 QMainWindow]
        PD[PreferencesDialog<br/>QDialog]
    end

    subgraph ViewModel Layer
        CVM[ConverterViewModel<br/>QObject + Signals]
        SVM[SearchViewModel<br/>QObject + Signals]
        PVM[PreferencesViewModel<br/>QObject + Signals]
    end

    subgraph Service Layer
        CS[ConverterService]
        SS[SearchService]
        TS[TranslationService]
    end

    subgraph Model Layer
        U[Unit<br/>dataclass]
        C[Category<br/>dataclass]
        CR[ConversionResult<br/>dataclass]
    end

    subgraph Operations Layer
        LO[length_operations.py]
        TO[temperature_operations.py]
        AO[area_operations.py]
        VO[volume_operations.py]
        WO[weight_operations.py]
        TiO[time_operations.py]
    end

    DV -->|binds to| CVM
    DV -->|binds to| SVM
    DV -->|binds to| PVM
    PD -->|binds to| PVM

    CVM -->|uses| CS
    SVM -->|uses| SS
    SVM -->|updates| CVM
    PVM -->|uses| TS

    CS -->|creates| CR
    CS -->|dispatches to| LO
    CS -->|dispatches to| TO
    CS -->|dispatches to| AO
    CS -->|dispatches to| VO
    CS -->|dispatches to| WO
    CS -->|dispatches to| TiO

    SS -->|queries| CS
    CS -->|reads| C
    C -->|contains| U

    LO -->|uses| U
    TO -->|uses| U
    AO -->|uses| U
    VO -->|uses| U
    WO -->|uses| U
    TiO -->|uses| U
```

## Conversion Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant View as DesktopWindow
    participant CVM as ConverterViewModel
    participant CS as ConverterService
    participant Op as CategoryOperation
    participant Model as ConversionResult

    User->>View: Types value in "From" input
    View->>CVM: set_from_value("100")
    CVM->>CS: convert(100, "length", "km", "m")
    CS->>Op: convert_length(100, "km", "m")
    Op-->>CS: 100000.0
    CS->>Model: Create ConversionResult
    Model-->>CS: result
    CS-->>CVM: ConversionResult
    CVM-->>View: result_changed signal("100000")
    View-->>User: Displays "100000" in "To" input
    CVM->>CVM: Add to history
    CVM-->>View: history_changed signal
```

## Search Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant View as DesktopWindow
    participant SVM as SearchViewModel
    participant SS as SearchService
    participant CVM as ConverterViewModel

    User->>View: Types "from kilometers to meters"
    View->>SVM: search("from kilometers to meters")
    SVM->>SS: search("from kilometers to meters")
    SS->>SS: Parse regex "from X to Y"
    SS->>SS: Match "kilometers" → length/kilometer
    SS->>SS: Match "meters" → length/meter
    SS-->>SVM: SearchResult(category=length, from=km, to=m)
    SVM->>CVM: set_units_from_search("length", "kilometer", "meter")
    CVM-->>View: category_changed + unit signals
    View-->>User: Navigates to Length with km→m
```

## Language Change Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant View as PreferencesDialog
    participant PVM as PreferencesViewModel
    participant TS as TranslationService
    participant Main as DesktopWindow

    User->>View: Selects "Español" from dropdown
    View->>PVM: set_language("es")
    PVM->>TS: language = "es"
    PVM-->>Main: language_changed signal("es")
    Main->>PVM: get_text(APP_TITLE)
    PVM->>TS: get("app_title")
    TS-->>PVM: "Conversor de Unidades"
    PVM-->>Main: "Conversor de Unidades"
    Main-->>User: UI updates to Spanish
```

## Building Binary Files

### Desktop Application (PyInstaller)

```bash
# Install dependencies
uv sync --dev

# Build single-file executable
uv run pyinstaller --onefile --windowed \
    --name "UnitConverter-Desktop" \
    --add-data "src:src" \
    main.py

# Output: dist/UnitConverter-Desktop
```

### Cross-Platform Build Matrix

| Platform | Command | Output |
|----------|---------|--------|
| Linux | `uv run pyinstaller --onefile main.py` | `dist/UnitConverter-Desktop` |
| macOS | `uv run pyinstaller --onefile --windowed main.py` | `dist/UnitConverter-Desktop.app` |
| Windows | `uv run pyinstaller --onefile --windowed main.py` | `dist/UnitConverter-Desktop.exe` |

### Build Notes

1. PyInstaller bundles Python + PySide6 + all dependencies into a single executable
2. Use `--windowed` flag on macOS/Windows to suppress the console window
3. The `--add-data` flag ensures the `src` package is included in the bundle
4. For smaller builds, use `--exclude-module` to remove unused Qt modules
5. Test the built binary on a clean machine without Python installed
