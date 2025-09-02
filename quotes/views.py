from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from .models import Quote, SiteStats
from .forms import QuoteForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required


def random_quote(request):
    quotes = Quote.objects.all()
    if not quotes:
        return render(request, 'quotes/random_quote.html', {'quote': None})
    
    # Увеличиваем счетчик просмотров для каждой цитаты при показе
    for quote in quotes:
        quote.views += 1
        quote.save()
    
    weights = [quote.weight for quote in quotes]
    chosen_quote = random.choices(quotes, weights=weights, k=1)[0]
    return render(request, 'quotes/random_quote.html', {'quote': chosen_quote})


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return redirect('random_quote')


def dislike_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return redirect('random_quote')


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quotes/add_quote.html', {
                'form': QuoteForm(),
                'success_message': 'Цитата успешно добавлена!'
            })
    else:
        form = QuoteForm()
    
    return render(request, 'quotes/add_quote.html', {'form': form})


def popular_quotes(request):
    # Берем 10 цитат с наибольшим количеством лайков
    popular = Quote.objects.all().order_by('-likes')[:10]
    return render(request, 'quotes/popular_quotes.html', {'quotes': popular})

@login_required
def dashboard(request):
    # Общая статистика
    stats = SiteStats.get_stats()
    total_quotes = Quote.objects.count()
    total_sources = Quote.objects.values('source').distinct().count()
    total_likes = Quote.objects.aggregate(Sum('likes'))['likes__sum'] or 0
    total_dislikes = Quote.objects.aggregate(Sum('dislikes'))['dislikes__sum'] or 0
    # total_views = Quote.objects.aggregate(Sum('views'))['views__sum'] or 0
    total_views = stats.total_views or 0
    
    # Самые популярные источники
    popular_sources = Quote.objects.values('source').annotate(
        quote_count=Count('id'),
        total_likes=Sum('likes')
    ).order_by('-total_likes')[:5]
    
    context = {
        'total_quotes': total_quotes,
        'total_sources': total_sources,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_views': total_views,
        'popular_sources': popular_sources,
    }
    return render(request, 'quotes/dashboard.html', context)


def random_quote(request):
    # Увеличиваем общий счетчик просмотров
    stats = SiteStats.get_stats()
    stats.total_views += 1
    stats.save()
    
    quotes = Quote.objects.all()
    if not quotes:
        return render(request, 'quotes/random_quote.html', {
            'quote': None,
            'total_views': stats.total_views
        })
    
    weights = [quote.weight for quote in quotes]
    chosen_quote = random.choices(quotes, weights=weights, k=1)[0]
    
    return render(request, 'quotes/random_quote.html', {
        'quote': chosen_quote,
        'total_views': stats.total_views
    })
