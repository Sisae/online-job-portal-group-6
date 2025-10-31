from django.db import migrations


def add_missing_columns(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()

    # Inspect existing columns in jobs_job
    existing_cols = {c.name for c in connection.introspection.get_table_description(cursor, 'jobs_job')}

    # Add created_by_id if missing
    if 'created_by_id' not in existing_cols:
        cursor.execute(
            "ALTER TABLE jobs_job ADD COLUMN created_by_id integer REFERENCES auth_user(id)"
        )
        # Create an index for faster lookups (if supported)
        try:
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS jobs_job_created_by_id_idx ON jobs_job(created_by_id)"
            )
        except Exception:
            # SQLite versions prior to 3.8.0 might not support IF NOT EXISTS; ignore if index exists
            pass

        # Backfill created_by_id to the first available user (prefer superuser), if any
        cursor.execute(
            """
            UPDATE jobs_job
               SET created_by_id = (
                   SELECT id FROM auth_user
                    ORDER BY is_superuser DESC, id ASC
                    LIMIT 1
               )
             WHERE created_by_id IS NULL
            """
        )

    # Add created_at if missing
    if 'created_at' not in existing_cols:
        cursor.execute("ALTER TABLE jobs_job ADD COLUMN created_at datetime")
        # Initialize created_at from posted_date when available
        cursor.execute("UPDATE jobs_job SET created_at = posted_date WHERE created_at IS NULL")

    # Add updated_at if missing
    if 'updated_at' not in existing_cols:
        cursor.execute("ALTER TABLE jobs_job ADD COLUMN updated_at datetime")
        cursor.execute("UPDATE jobs_job SET updated_at = posted_date WHERE updated_at IS NULL")


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_missing_columns, migrations.RunPython.noop),
    ]
