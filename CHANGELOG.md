# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-06-28

### Added

#### Core Features
- Initial public release of **autooutlier**.
- Automatic outlier detection with intelligent method selection.
- Automatic outlier handling based on dataset characteristics.
- Manual selection of detection and handling methods.
- Support for custom replacement values.

#### Statistics Module
- Descriptive statistics:
  - Mean
  - Median
  - Mode
  - Standard Deviation
  - Variance
  - Data Range
- Quartile calculations (Q1, Q3, IQR)
- Skewness analysis
- Kurtosis analysis
- Distribution classification

#### Detection Module
Implemented the following outlier detection methods:

- IQR Method
- Z-Score Method
- Modified Z-Score Method
- Percentile Method
- Automatic Detection Method Selection
- Boolean Outlier Mask Generation

#### Handling Module
Implemented multiple outlier handling strategies:

- Winsorization
- Mean Replacement
- Median Replacement
- Mode Replacement
- Interpolation
- Forward Fill
- Backward Fill
- Custom Value Replacement
- Outlier Removal
- Automatic Handling Method Selection

#### Summary Module
Added comprehensive pre-cleaning analysis including:

- Recommended detection method
- Recommended handling method
- Number of outliers
- Percentage of outliers
- Distribution type
- Skewness report
- Statistical summary

#### Visualization Module
- Box Plot visualization using Seaborn.

#### Utility Module
Added helper functions for:

- Numeric column validation
- Continuous data validation
- Time-series detection
- Outlier counting
- Outlier percentage calculation

#### Documentation
Added professional project documentation including:

- README
- Installation Guide
- User Guide
- API Reference
- Detection Methods Guide
- Handling Methods Guide
- Examples
- FAQ
- Changelog

#### Examples
Added practical usage examples demonstrating:

- Automatic detection
- Automatic handling
- Manual detection
- Manual handling
- Summary generation

#### Testing
Added unit tests for:

- Detection module
- Handling module
- Statistics module
- Summary module

#### Packaging
Configured the project for distribution using:

- pyproject.toml
- setuptools
- MANIFEST.in
- Editable installation support
- Source distribution (sdist)
- Wheel distribution

#### Project Structure
Added:

- MIT License
- Version management
- Documentation folder
- Examples folder
- Tests folder
- Professional package layout

---

## License

This project is licensed under the MIT License.