import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentme.settings')


def management_command():
    """Entry-point for the command-line admin utility."""
    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
