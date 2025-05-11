# Visual Regression Test Screenshots

This directory contains screenshots used for visual regression testing.

## Directory Structure

- `baseline/`: Contains the baseline screenshots that serve as reference
- `actual/`: Contains the screenshots taken during test execution
- `diff/`: Contains difference images when visual regressions are detected

## Usage

Visual regression tests compare screenshots taken during test execution against
baseline screenshots to detect unintended visual changes in the application.

When running the tests for the first time, baseline screenshots will be automatically
created. Subsequent test runs will compare new screenshots against these baselines.

## Updating Baselines

If intended visual changes are made to the application, the baseline screenshots
should be updated. This can be done by:

1. Deleting the existing baseline screenshots that need to be updated
2. Running the tests again, which will generate new baseline screenshots

Alternatively, you can manually copy screenshots from `actual/` to `baseline/`.

## Notes

- Visual regression tests are marked with the `visual` marker and can be run with:
  `pytest -m visual`
- The threshold for visual differences can be adjusted in `test_visual.py`
- Screenshot comparison uses PIL (Pillow) for image processing
