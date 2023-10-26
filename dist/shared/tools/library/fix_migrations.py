from core.library import regex, listdir, rename
from web.settings import BASE_DIR, PROJECT_NAME


def apply_fixtures():
  migrations_fix = '_' + regex.to_alphanumeric(PROJECT_NAME).lower() + '.py'
  migrations_path = f'{BASE_DIR}/api/migrations'
  for _f in listdir(migrations_path):
    if not _f.startswith('__') and not _f.endswith(migrations_fix):
      rename(f'{migrations_path}/{_f}', f"{migrations_path}/{_f.replace('.py', migrations_fix)}")
