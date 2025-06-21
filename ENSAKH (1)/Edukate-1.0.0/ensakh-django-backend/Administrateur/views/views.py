from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from .models import Filiere, Module, Enseignant, Etudiant
import re

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_response(request):
    """API pour le chatbot IA"""
    message = request.data.get('message', '').lower().strip()
    
    if not message:
        return Response({'error': 'Message vide'}, status=400)
    
    # Contexte ENSAKH
    context = {
        'total_etudiants': Etudiant.objects.count(),
        'total_enseignants': Enseignant.objects.count(),
        'total_modules': Module.objects.count(),
        'total_filieres': Filiere.objects.count(),
    }
    
    # Statistiques par filière
    filieres_stats = Filiere.objects.annotate(
        nb_etudiants=Count('etudiants')
    ).values('code', 'nom', 'nb_etudiants')
    
    # Analyse du message et génération de réponse
    response_text = generate_chatbot_response(message, context, list(filieres_stats))
    
    return Response({'response': response_text})

def generate_chatbot_response(message, context, filieres_stats):
    """Génère une réponse contextuelle pour le chatbot"""
    
    # Salutations
    if any(word in message for word in ['bonjour', 'salut', 'hello', 'bonsoir']):
        return f"""Bonjour ! Je suis ravi de vous aider. En tant qu'assistant IA de l'ENSAKH, je peux vous fournir des informations détaillées sur :

• 📊 Statistiques ({context['total_etudiants']} étudiants, {context['total_enseignants']} enseignants)
• 🎓 Les {context['total_filieres']} filières disponibles
• 📚 Les {context['total_modules']} modules d'enseignement
• 🔍 Recherches spécifiques sur les données

Que souhaitez-vous savoir ?"""
    
    # Questions sur les étudiants
    elif any(word in message for word in ['étudiant', 'étudiants', 'élève']):
        filiere_breakdown = '\n'.join([
            f"• {f['code']}: {f['nb_etudiants']} étudiants"
            for f in filieres_stats
        ])
        
        return f"""📊 **Informations sur les étudiants ENSAKH:**

**Total:** {context['total_etudiants']} étudiants inscrits

**Répartition par filière:**
{filiere_breakdown}

La filière avec le plus d'étudiants est {max(filieres_stats, key=lambda x: x['nb_etudiants'])['code']} avec {max(filieres_stats, key=lambda x: x['nb_etudiants'])['nb_etudiants']} inscrits.

Souhaitez-vous des détails sur une filière spécifique ?"""
    
    # Questions sur les enseignants
    elif any(word in message for word in ['enseignant', 'professeur', 'prof', 'teacher']):
        return f"""👨‍🏫 **Corps enseignant ENSAKH:**

• **Total:** {context['total_enseignants']} enseignants qualifiés
• **Ratio:** Environ 1 enseignant pour {context['total_etudiants'] // context['total_enseignants']} étudiants
• **Expertise:** Couvrant toutes les spécialités des {context['total_filieres']} filières

Nos enseignants sont des experts dans leurs domaines, alliant expérience académique et industrielle pour offrir une formation de qualité.

Voulez-vous des informations sur l'équipe pédagogique d'une filière particulière ?"""
    
    # Questions sur les filières
    elif any(word in message for word in ['filière', 'filières', 'spécialité', 'département']):
        filieres_details = '\n\n'.join([
            f"🎓 **{f['code']}** - {f['nom']} ({f['nb_etudiants']} étudiants)"
            for f in filieres_stats
        ])
        
        return f"""🎓 **Les {context['total_filieres']} filières de l'ENSAKH:**

{filieres_details}

Chaque filière propose un cursus complet sur 3 ans avec des stages en entreprise et des projets de fin d'études.

Sur quelle filière souhaitez-vous plus de détails ?"""
    
    # Questions sur les modules
    elif any(word in message for word in ['module', 'modules', 'cours', 'matière']):
        return f"""📚 **Modules d'enseignement:**

• **Total:** {context['total_modules']} modules disponibles
• **Organisation:** Répartis sur 6 semestres (3 ans)
• **Types:** Cours magistraux, TD, TP, projets

**Catégories principales:**
• Sciences fondamentales
• Sciences de l'ingénieur
• Spécialisation par filière
• Langues et communication
• Management et entrepreneuriat

Voulez-vous connaître les modules d'une filière spécifique ?"""
    
    # Questions sur les statistiques
    elif any(word in message for word in ['statistique', 'stats', 'chiffres', 'données']):
        return f"""📈 **Statistiques ENSAKH 2024:**

**👥 Communauté:**
• Étudiants: {context['total_etudiants']}
• Enseignants: {context['total_enseignants']}
• Ratio: 1 enseignant / {context['total_etudiants'] // context['total_enseignants']} étudiants

**🎓 Formation:**
• Filières: {context['total_filieres']}
• Modules: {context['total_modules']}
• Durée: 3 ans (6 semestres)

**📊 Répartition par filière:**
{chr(10).join([f"• {f['code']}: {f['nb_etudiants']} étudiants" for f in filieres_stats])}

**🏆 Taux de réussite:** 92%
**💼 Taux d'insertion:** 95% dans les 6 mois"""
    
    # Recherche spécifique par filière
    elif any(code.lower() in message for code in ['gi', 'ge', 'iid', 'iric', 'mgsi', 'gpee']):
        for filiere in filieres_stats:
            if filiere['code'].lower() in message:
                return f"""🎓 **{filiere['code']} - {filiere['nom']}:**

• **Étudiants:** {filiere['nb_etudiants']}
• **Durée:** 3 ans (6 semestres)
• **Débouchés:** Ingénieur spécialisé dans le domaine

Cette filière forme des ingénieurs compétents et polyvalents dans leur spécialité.

Souhaitez-vous plus d'informations sur les modules ou les débouchés de cette filière ?"""
    
    # Aide
    elif any(word in message for word in ['aide', 'help', 'support', 'assistance']):
        return """🤝 **Comment puis-je vous aider ?**

Je peux vous renseigner sur :

**📊 Données générales:**
• Statistiques de l'école
• Nombre d'étudiants/enseignants

**🎓 Filières:**
• Détails des spécialités
• Programmes et débouchés

**📚 Pédagogie:**
• Modules d'enseignement
• Organisation des études

**🔍 Recherches spécifiques:**
• Informations sur une filière
• Comparaisons entre spécialités

Posez-moi votre question, je suis là pour vous aider !"""
    
    # Remerciements
    elif any(word in message for word in ['merci', 'thank', 'remercie']):
        return """De rien ! 😊 Je suis toujours là pour vous aider avec toutes vos questions sur l'ENSAKH.

N'hésitez pas à me solliciter pour :
• Des informations complémentaires
• Des précisions sur les filières
• Des statistiques détaillées
• Tout autre renseignement

Bonne continuation ! 🎓"""
    
    # Réponse par défaut
    else:
        return """🤔 Je ne suis pas sûr de bien comprendre votre question, mais je peux vous aider avec :

**💡 Suggestions:**
• "Combien d'étudiants en GI ?" - Infos sur une filière
• "Quelles sont les filières ?" - Liste complète
• "Statistiques ENSAKH" - Données générales
• "Modules informatique" - Programmes d'études

**🎯 Ou essayez:**
• Des questions sur les étudiants/enseignants
• Des informations sur les filières
• Des détails sur les modules

Reformulez votre question, je ferai de mon mieux pour vous aider ! 😊"""
