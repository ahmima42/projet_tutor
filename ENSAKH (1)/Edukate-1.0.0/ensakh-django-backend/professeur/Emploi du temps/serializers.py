
from rest_framework import serializers
from .models import Session, TimeSlot, Attendance
from academic.models import Module, Group, Room
from accounts.models import Professor

class TimeSlotSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.name', read_only=True)
    professor_name = serializers.CharField(source='professor.user.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    time_slot_details = TimeSlotSerializer(source='time_slot', read_only=True)
    
    class Meta:
        model = Session
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'