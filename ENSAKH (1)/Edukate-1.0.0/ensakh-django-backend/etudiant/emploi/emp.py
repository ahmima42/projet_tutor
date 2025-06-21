from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime, timedelta

# Utilitaire pour exécuter des requêtes SQL
def fetchall_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@login_required
def schedule_view(request):
    user = request.user
    student_id = user.username  # ou un autre champ selon ton système d'authentification

    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    time_slots = [
        {"id": 1, "time_range": "08:00-10:00"},
        {"id": 2, "time_range": "10:15-12:15"},
        {"id": 3, "time_range": "13:30-15:30"},
        {"id": 4, "time_range": "15:45-17:45"},
    ]

    # Simuler un emploi du temps depuis la base de données
    schedule_data = {slot["id"]: {day: [] for day in days} for slot in time_slots}

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.name, 'Salle B203' AS room, 'Pr. Yassine' AS professor,
                   'bg-info' AS color_class, 'Lundi' AS day, '08:00-10:00' AS time_range
            FROM enrollments e
            JOIN modules m ON m.id = e.module_id
            WHERE e.student_id = %s
            LIMIT 5
        """, [student_id])
        results = fetchall_dict(cursor)

    for row in results:
        for slot in time_slots:
            if slot["time_range"] == row["time_range"]:
                schedule_data[slot["id"]][row["day"]].append({
                    "name": row["name"],
                    "room": row["room"],
                    "professor": row["professor"],
                    "color_class": row["color_class"],
                    "id": f"{row['name']}_{row['day']}_{slot['id']}"
                })

    # Statistiques
    stats = {
        "total_courses": len(results),
        "total_hours": len(results) * 2,
        "unique_subjects": len(set([row["name"] for row in results]))
    }

    # Types de cours
    course_types = [
        {"name": "Cours", "badge_class": "badge-primary"},
        {"name": "TP", "badge_class": "badge-success"},
        {"name": "TD", "badge_class": "badge-warning"},
        {"name": "Projet", "badge_class": "badge-danger"},
    ]

    context = {
        "user": user,
        "days": days,
        "time_slots": time_slots,
        "schedule_data": schedule_data,
        "stats": stats,
        "current_week": f"Semaine {datetime.now().isocalendar()[1]}",
        "course_types": course_types
    }

    return render(request, 'schedule.html', context)
