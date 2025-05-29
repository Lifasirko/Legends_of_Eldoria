from setuptools import setup, find_packages

setup(
    name="legends_of_eldoria",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "aiogram>=3.0.0",
        "SQLAlchemy>=1.4",
        "alembic>=1.9",
        "psycopg2-binary",
        "redis",
        "celery",
        "python-dotenv",
    ],
) 