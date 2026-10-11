"""Backward-compatible alias for build_package_data.py."""

from build_package_data import build_database


if __name__ == "__main__":
    print("copy_csv.py is deprecated; generating compressed package databases.")
    build_database()
