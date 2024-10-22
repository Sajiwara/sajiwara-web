from django.shortcuts import render
from django.db.models import Q
from search.models import Restaurant

def show_search(request):
    name_query = request.GET.get('name', '').strip()
    food_type_query = request.GET.get('food_type', '').strip()
    rating_query = request.GET.get('rating', '')

    # Start with all restaurants
    restaurants = Restaurant.objects.all()

    # Name search with partial matching
    if name_query:
        name_filters = Q(nama__icontains=name_query)
        # Add similar name matching (e.g., if someone types "sushi", it might match "sushian")
        words = name_query.split()
        for word in words:
            name_filters |= Q(nama__icontains=word)
        restaurants = restaurants.filter(name_filters)

    # Food type with flexible matching
    if food_type_query:
        food_type_filters = Q(jenis_makanan__iexact=food_type_query)
        # Add partial matching for food type
        food_type_filters |= Q(jenis_makanan__icontains=food_type_query)
        restaurants = restaurants.filter(food_type_filters)

    # Rating with range matching
    if rating_query:
        try:
            rating_value = float(rating_query)
            # Get restaurants within 0.5 stars of the requested rating
            restaurants = restaurants.filter(
                rating__gte=rating_value - 0.5,
                rating__lte=rating_value + 0.5
            )
        except ValueError:
            pass

    # Order results by relevance (exact matches first, then partial matches)
    if name_query or food_type_query:
        restaurants = restaurants.order_by(
            # Exact matches first
            ~Q(nama__iexact=name_query),
            ~Q(jenis_makanan__iexact=food_type_query),
            # Then partial matches
            'nama',
            'rating'
        )

    context = {
        'restaurants': restaurants,
        'search_params': {
            'name': name_query,
            'food_type': food_type_query,
            'rating': rating_query
        }
    }
    return render(request, 'search.html', context)