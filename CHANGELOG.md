
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [PEP440](https://peps.python.org/pep-0440/).

## [Unreleased]


## [0.2.0] - 2025-05-11

### Added
 - Sphinx Documentation

### Removed
 - `Signal.set`: this was just a hack


## [0.1.0] - 2025-05-06

### Added
 - `Signal`: a container that tracks changes
 - `effect`: effects run whenever the signals they use have changed
 - `derived`: define a new signal that is computed from other signals
