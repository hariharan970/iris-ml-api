# Task 20 Notes

Task 20 finalizes the Iris ML API with documentation, deployment configuration, automated testing, and an independent extension.

## Independent Extension

I chose **GitHub Actions automated testing**. The workflow in `.github/workflows/tests.yml` runs the existing pytest suite on pushes to `main` and pull requests targeting `main`.

This keeps the project's regression tests running automatically instead of relying only on local test execution.
