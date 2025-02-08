from django.shortcuts import render
import random

# Create your views here.
QUOTES = [
    'Anything I do, I want to do it well.',
    'No such thing as a life that’s better than yours.',
    'We don’t look nothin’ like the people on the screen / You know, them movie stars, picture-perfect beauty queens / But we got dreams, and we got the right to chase ‘em.'
]

IMAGES = [
    'https://www.udiscovermusic.com/wp-content/uploads/2021/05/J.-Cole_Lead-Promo-Image-1024x1024.jpg',
    'https://static.wikia.nocookie.net/jcole/images/0/02/J._Cole.jpg/revision/latest?cb=20231020222449',
    'https://static01.nyt.com/images/2024/04/08/multimedia/08xp-jcole/08xp-jcole-superJumbo.jpg?quality=75&auto=webp'
]


def quote(request):
    selected_quote = random.choice(QUOTES)
    selected_image = random.choice(IMAGES)
    return render(request, 'quotes/quote.html', {'quote': selected_quote, 'image': selected_image})
def show_all(request):
    return render(request, 'quotes/show_all.html', {'quotes': QUOTES, 'images': IMAGES})
def about(request):
    return render(request, 'quotes/about.html')