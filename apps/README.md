# Inactive app copies

This directory contains older/duplicate app modules (`accounts/`, `companies/`, `jobs/`, `applications/`, `core/`) that are not used by the current project configuration.

- Active apps are the top-level packages in the repository root (e.g., `accounts/`, `jobs/`, etc.).
- `INSTALLED_APPS` in `jobportal_project/settings.py` references only the top-level apps.
- You can safely ignore this folder for development and deployment.

If you want to remove it entirely:

- Confirm no imports reference `apps.*` (current settings don’t).
- Remove the `apps/` directory in a separate commit/PR to keep history clean.
