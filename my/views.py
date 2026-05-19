# файл views.py
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from .models import Ad

def test_orm_view(request) -> HttpResponse:
    """this is a test ORM view"""
    one_month_ago = timezone.now() - timedelta(days=30)
    ads_last_month = Ad.objects.filter(created_at__gte=one_month_ago)

    active_ads_in_category = Ad.objects.filter(cathegory_id=1, is_active=True)

    ads_with_comment_count = Ad.objects.annotate(comments_count=Count('comment'))

    user_ads = Ad.objects.filter(user_id=1) 


    output = "<h1>Результати ORM запитів:</h1>"
    
    output += "<h3>1. Створені за останній місяць:</h3>"
    for ad in ads_last_month:
        output += f"- {ad.title} (створено: {ad.created_at})<br>"
        
    output += "<h3>2. Активні в категорії №1:</h3>"
    for ad in active_ads_in_category:
        output += f"- {ad.title}<br>"
        
    output += "<h3>3. Кількість коментарів до кожного оголошення:</h3>"
    for ad in ads_with_comment_count:
        output += f"- {ad.title} — Коментарів: {ad.comments_count}<br>"
        
    output += "<h3>4. Оголошення користувача №1:</h3>"
    for ad in user_ads:
        output += f"- {ad.title}<br>"
    return HttpResponse(output)