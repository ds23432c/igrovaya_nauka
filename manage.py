#!/usr/bin/env python
import os
import sys


def maybe_repair_legacy_database():
    if len(sys.argv) < 2 or sys.argv[1] != 'migrate':
        return

    import django
    from django.core.management import call_command

    django.setup()
    call_command('repair_legacy_db')


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc

    maybe_repair_legacy_database()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
