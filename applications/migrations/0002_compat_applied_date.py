from django.db import migrations


def ensure_applied_date(apps, schema_editor):
    connection = schema_editor.connection
    cursor = connection.cursor()

    # Get current columns
    existing_cols = {c.name for c in connection.introspection.get_table_description(cursor, 'applications_application')}

    # If applied_date is missing but applied_at exists, rename the column for consistency
    if 'applied_date' not in existing_cols and 'applied_at' in existing_cols:
        # SQLite supports simple rename from SQLite 3.25+, but to stay compatible we try a direct RENAME first
        try:
            cursor.execute("ALTER TABLE applications_application RENAME COLUMN applied_at TO applied_date")
        except Exception:
            # Fallback: create new column and copy data
            cursor.execute("ALTER TABLE applications_application ADD COLUMN applied_date datetime")
            cursor.execute("UPDATE applications_application SET applied_date = applied_at WHERE applied_date IS NULL")


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(ensure_applied_date, migrations.RunPython.noop),
    ]
