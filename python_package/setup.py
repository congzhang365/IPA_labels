from setuptools import setup, find_packages

setup(
    name="ipa_labels",
    version="0.2.0",
    packages=find_packages(),
    package_data={"ipa_labels": ["data/*.json.gz", "data/*.json"]},
    include_package_data=True,
    install_requires=[],
    author="Cong",
    license="MIT",
    description="A comprehensive IPA dictionary package with dynamic lookup functions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
