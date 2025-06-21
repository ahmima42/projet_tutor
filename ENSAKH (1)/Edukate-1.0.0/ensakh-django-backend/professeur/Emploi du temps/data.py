# management/commands/populate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Professor, Student
from academic.models import Module, Group, Room
from schedule.models import TimeSlot, Session
from datetime import time, date

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data'
    
    def handle(self, *args, **options):
        # Créer les créneaux horaires
        time_slots = [
            (1, time(8, 30), time(10, 30)),
            (1, time(10, 45), time(12, 45)),
            (1, time(14, 0), time(16, 0)),
            (1, time(16, 15), time(18, 15)),
            (2, time(8, 30), time(10, 30)),
            (2, time(10, 45), time(12, 45)),
            (3, time(10, 45), time(12, 45)),
            (4, time(16, 15), time(18, 15)),
        ]
        
        for day, start, end in time_slots:
            TimeSlot.objects.get_or_create(
                day_of_week=day,
                start_time=start,
                end_time=end
            )
        
        # Créer des salles
        rooms_data = [
            ('A24', 50, 'classroom'),
            ('B12', 30, 'lab'),
            ('C07', 40, 'classroom'),
        ]
        
        for name, capacity, room_type in rooms_data:
            Room.objects.get_or_create(
                name=name,
                defaults={'capacity': capacity, 'room_type': room_type}
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data')
        )