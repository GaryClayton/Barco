from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reports.models import ClubMember, Attendance, Guests


class Command(BaseCommand):
    help = 'Checks for orphaned records that point to non-existent Users'

    def handle(self, *args, **options):
        User = get_user_model()

        # Configuration: (Model, Field Name, Description)
        checks = [
            (ClubMember, 'user_id', 'Club Members'),
            (Attendance, 'member', 'Attendance Records'),
            (Guests, 'sponsor', 'Guest Sponsors'),
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("--- Reports Data Integrity Audit ---"))

        for model, field, label in checks:
            # Efficiently find records where the ID is NOT in the User table
            orphans = model.objects.exclude(**{f"{field}__in": User.objects.all()})

            if orphans.exists():
                count = orphans.count()
                orphan_ids = list(orphans.values_list(field, flat=True).distinct())
                self.stdout.write(
                    self.style.ERROR(f"❌ {label}: Found {count} orphans! IDs: {orphan_ids}")
                )
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ {label}: All records valid."))