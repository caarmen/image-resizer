rm -rf reports
SUPPORTED_IMAGE_URL_SCHEMAS='["https","file"]' python -m pytest --cov=imageresizer --cov-report=xml --cov-report=html --junitxml="reports/junit.xml" tests
mkdir -p reports
mv coverage.xml htmlcov reports/.
