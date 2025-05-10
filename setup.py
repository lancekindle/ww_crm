from setuptools import setup, find_packages

setup(
    name="ww_crm",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask==3.1.0",
        "flask-sqlalchemy==3.1.1",
        "flask-migrate==4.1.0",
    ],
    python_requires=">=3.11",
)
