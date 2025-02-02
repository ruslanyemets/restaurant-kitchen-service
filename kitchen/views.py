from django.shortcuts import render
from django.views import generic

from kitchen.models import Cook, Dish, DishType


def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    queryset = DishType.objects.all()
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type").order_by("id")
    template_name = "kitchen/dish_list.html"
    paginate_by = 5


class CookListView(generic.ListView):
    model = Cook
    queryset = Cook.objects.all()
    template_name = "kitchen/cook_list.html"
    paginate_by = 5
