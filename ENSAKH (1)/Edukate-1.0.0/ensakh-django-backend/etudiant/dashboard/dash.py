# backend ENSAKH version Django
# Une seule vue pour exposer les mêmes données que le backend Node.js

from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
import json
from django.contrib.auth.hashers import check_password
import jwt
import datetime

# Clé secrète pour JWT (mettre dans .env ou settings)
JWT_SECRET = 'ensakh_secret_key_2024'
JWT_ALGO = 'HS256'

# Utilitaire : Exécuter requête SQL + retourner le résultat

def dictfetchall(cursor):
    """Retourne tous les résultats de curseur comme liste de dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Authentification avec email / password
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        body = json.loads(request.body)
        email = body['email']
        password = body['password']

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password_hash FROM students WHERE email = %s", [email])
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"error": "Email incorrect"}, status=401)

            student = dict(zip([col[0] for col in cursor.description], row))

            if not check_password(password, student['password_hash']):
                return JsonResponse({"error": "Mot de passe incorrect"}, status=401)

            payload = {
                "id": student['id'],
                "email": student['email'],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

            return JsonResponse({
                "token": token,
                "student": {
                    "id": student['id'],
                    "name": student['name'],
                    "email": student['email']
                }
            })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Exemple de route : Données du tableau de bord (modules, moyenne, projets)
@require_http_methods(["GET"])
def student_dashboard(request, student_id):
    token = request.headers.get("Authorization")
    if not token:
        return JsonResponse({"error": "Token manquant"}, status=401)

    try:
        jwt.decode(token.split(" ")[1], JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Token expiré"}, status=403)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Token invalide"}, status=403)

    try:
        with connection.cursor() as cursor:
            # Modules inscrits
            cursor.execute("""
                SELECT m.name, m.code, m.semester
                FROM modules m
                JOIN enrollments e ON m.id = e.module_id
                WHERE e.student_id = %s
            """, [student_id])
            modules = dictfetchall(cursor)

            # Moyenne
            cursor.execute("SELECT ROUND(AVG(grade), 2) AS moyenne FROM grades WHERE student_id = %s", [student_id])
            moyenne = cursor.fetchone()[0] or 0

            return JsonResponse({
                "modules": modules,
                "moyenne": moyenne
            })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Page 404 personnalisée
def not_found(request, exception):
    return HttpResponseNotFound(json.dumps({"error": "Route non trouvée"}), content_type="application/json")
