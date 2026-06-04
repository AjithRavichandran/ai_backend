# generate/services.py

from django.core.exceptions import ValidationError
from .models import ProjectVersion

def rename_live_tables_and_fields(project, table_renames, field_renames):
    try:
        live_version = ProjectVersion.objects.get(
            project=project, version_type="live"
        )
    except ProjectVersion.DoesNotExist:
        raise ValidationError("Live version not found")

    old_live_appdata = live_version.app_data or {}
    new_live_appdata = {}

    for old_table_name, rows in old_live_appdata.items():
        new_table_name = table_renames.get(old_table_name, old_table_name)
        new_live_appdata[new_table_name] = []

        rename_map = field_renames.get(new_table_name, {})

        for row in rows:
            new_row = {}
            for old_field, value in row.items():
                new_field = rename_map.get(old_field, old_field)
                new_row[new_field] = value
            new_live_appdata[new_table_name].append(new_row)

    live_version.app_data = new_live_appdata
    live_version.save()

    return live_version
