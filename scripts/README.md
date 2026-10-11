# Maintenance scripts

`validate_resources.py` is the maintained script in this folder. It checks the
package CSV against the local reference resources.

The remaining scripts in `scripts/archive/` are preserved exploratory or
one-off parsing tools from the original data-collection work. They are kept
for provenance and may contain older hard-coded paths; use the maintained
root-level `generate_csv.py` and `build_package_data.py` workflow for normal
updates.
