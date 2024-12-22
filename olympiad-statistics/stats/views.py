from django.db.models import Count, Q, Avg
from django.shortcuts import render
from django.core.exceptions import BadRequest

from stats.models import Statistics, Athlete, OlympiadInfo, Country


def index(request):
    return render(request, 'stats/index.html')


def q_athletes_by_age(request):
    return render(request, 'stats/q_athletes_by_age.html')


def q_athletes_by_medals(request):
    return render(request, 'stats/q_athletes_by_medals.html')


def q_athletes_by_weight(request):
    return render(request, 'stats/q_athletes_by_weight.html')


def q_countries_by_athletes_count(request):
    return render(request, 'stats/q_countries_by_athletes_count.html')


def q_countries_by_gold_medals(request):
    return render(request, 'stats/q_countries_by_gold_medals.html')


def q_countries_by_medals(request):
    return render(request, 'stats/q_countries_by_medals.html')


def q_mean_height(request):
    return render(request, 'stats/q_mean_height.html')


def q_sex_percentage(request):
    return render(request, 'stats/q_sex_percentage.html')


def q_sport_by_athlete_count(request):
    return render(request, 'stats/q_sport_by_athlete_count.html')


def add_data(request):
    return render(request, 'stats/add_data.html')


def delete_data(request):
    return render(request, 'stats/delete_data.html')


def countries_by_medals(request):
    year = request.GET.get("year")
    medal = request.GET.get("medal")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/countries_by_medals.html')
        res = Statistics.objects.filter(games__year=year)
    else:
        res = Statistics.objects

    if medal == "gold":
        result = res.filter(medal__icontains='gold')
    elif medal == "silver":
        result = res.filter(medal__icontains='silver')
    elif medal == "bronze":
        result = res.filter(medal__icontains='bronze')
    else:
        return render(request, 'stats/countries_by_medals.html')

    result = result.values('country_code__country_name') \
        .annotate(medals_count=Count('country_code')) \
        .order_by('-medals_count')

    if not result:
        return render(request, 'stats/countries_by_medals.html')

    context = {'res': result, 'color': medal, 'year': year}
    return render(request, 'stats/countries_by_medals.html', context)


def athletes_by_medals(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/athletes_by_medals.html')
        result = Statistics.objects.filter(games__year=year)
    else:
        result = Statistics.objects

    result = result.exclude(medal__icontains='NA') \
        .values('player_id__name') \
        .annotate(gold_counts=Count('medal', filter=Q(medal__icontains='gold'))) \
        .annotate(silver_counts=Count('medal', filter=Q(medal__icontains='silver'))) \
        .annotate(bronze_counts=Count('medal', filter=Q(medal__icontains='bronze'))) \
        .filter(Q(gold_counts__gte=1) | Q(silver_counts__gte=1) | Q(bronze_counts__gte=1)) \
        .order_by('-gold_counts', '-silver_counts', '-bronze_counts')

    if not result:
        return render(request, 'stats/athletes_by_medals.html')

    context = {'res': result, 'year': year}
    return render(request, 'stats/athletes_by_medals.html', context)


def countries_by_athletes_count(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/countries_by_athletes_count.html')
        result = Statistics.objects.filter(games__year=year)
    else:
        result = Statistics.objects

    result = result.values('country_code__country_name') \
        .annotate(athlete_count=Count('player_id', distinct=True)) \
        .order_by('-athlete_count')

    if not result:
        return render(request, 'stats/countries_by_athletes_count.html')

    context = {'res': result, 'year': year}
    return render(request, 'stats/countries_by_athletes_count.html', context)


def sex_percentage(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/sex_percentage.html')
        res = Statistics.objects.filter(games__year=year)
    else:
        res = Statistics.objects

    female_count = res.filter(player_id__sex='F').values('player_id').distinct().count()
    male_count = res.filter(player_id__sex='M').values('player_id').distinct().count()

    if not female_count or not male_count:
        return render(request, 'stats/sex_percentage.html')

    context = {'female': 100 * round(female_count / (female_count + male_count), 3),
               'male': 100 * round(male_count / (female_count + male_count), 3),
               'year': year}
    return render(request, 'stats/sex_percentage.html', context)


def sport_by_athlete_count(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/sport_by_athlete_count.html')
        result = Statistics.objects.filter(games__year=year)
    else:
        result = Statistics.objects

    result = result.values('player_id__statistics__sport') \
        .annotate(athlete_count=Count('player_id', distinct=True)) \
        .order_by('-athlete_count')

    if not result:
        return render(request, 'stats/sport_by_athlete_count.html')

    context = {'res': result, 'year': year}
    return render(request, 'stats/sport_by_athlete_count.html', context)


def athletes_by_weight(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/athletes_by_weight.html')
        result = Statistics.objects.filter(games__year=year)
    else:
        result = Statistics.objects

    result = result.values('player_id__name', 'weight').order_by('-weight').distinct()

    if not result:
        return render(request, 'stats/athletes_by_weight.html')

    context = {'res': result, 'year': year}
    return render(request, 'stats/athletes_by_weight.html', context)


def athletes_by_age(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/athletes_by_age.html')
        result = Statistics.objects.filter(games__year=year)
    else:
        result = Statistics.objects

    result = result.exclude(age=-1).values('player_id__name', 'age').order_by('-age').distinct()

    if not result:
        return render(request, 'stats/athletes_by_age.html')

    context = {'res': result, 'year': year}
    return render(request, 'stats/athletes_by_age.html', context)


def countries_by_gold_medals(request):
    country = request.GET.get("country")
    if country:
        result = Statistics.objects.filter(country_code__country_name__icontains=country) \
            .filter(medal__icontains='gold') \
            .values('games_id').annotate(medal_count=Count('games_id')) \
            .order_by('-medal_count')
    else:
        result = None

    if not result:
        return render(request, 'stats/countries_by_gold_medals.html')

    context = {'res': result, 'country': country}
    return render(request, 'stats/countries_by_gold_medals.html', context)


def mean_height(request):
    year = request.GET.get("year")
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/mean_height.html')
        result = Athlete.objects.filter(statistics__games__year=year)
    else:
        result = Athlete.objects

    f = result.filter(sex__exact='F').exclude(height=-1)\
        .aggregate(Avg('height'))
    m = result.filter(sex__exact='M').exclude(height=-1)\
        .aggregate(Avg('height'))

    f['height__avg'] = round(f['height__avg'], 1)
    m['height__avg'] = round(m['height__avg'], 1)

    if not f or not m:
        return render(request, 'stats/mean_height.html')

    context = {'female_mean': f, 'male_mean': m, 'year': year}
    return render(request, 'stats/mean_height.html', context)


def q_athlete(request):
    return render(request, 'stats/q_athlete.html')


def q_olympiad(request):
    return render(request, 'stats/q_olympiad.html')


def q_add_athlete_result(request):
    return render(request, 'stats/q_athlete_result.html')


def add_new_athlete(request):
    contex = {'msg': "Failed to add athlete to the database, make sure all fields are correct."}

    name = request.POST['name']
    if not name:
        return render(request, 'stats/after_adding.html', contex)

    height = request.POST['height']
    if height:
        try:
            height = int(height)
        except:
            return render(request, 'stats/after_adding.html', contex)
    else:
        return render(request, 'stats/after_adding.html', contex)

    sex = request.POST['sex']
    if sex != "F" and sex != "M":
        return render(request, 'stats/after_adding.html', contex)

    new_athlete = Athlete(name=name, height=height, sex=sex)
    try:
        new_athlete.save()
    except BadRequest as e:
        return handler_400(request, e)

    if new_athlete.id:
        contex = {'msg': "Added athlete to the database."}

    return render(request, 'stats/after_adding.html', contex)


def add_olympiad(request):
    contex = {'msg': "Failed to add olympiad to the database, make sure all fields are correct."}

    season = request.POST['season']
    if not season:
        return render(request, 'stats/after_adding.html', contex)

    year = request.POST['year']
    if year:
        try:
            year = int(year)
        except:
            return render(request, 'stats/after_adding.html', contex)
    else:
        return render(request, 'stats/after_adding.html', contex)

    city = request.POST['city']
    if not city:
        return render(request, 'stats/after_adding.html', contex)

    new_olympiad = OlympiadInfo(year=year, season=season, city=city, games=str(year)+season)
    try:
        new_olympiad.save()
    except BadRequest as e:
        return handler_400(request, e)

    if new_olympiad.id:
        contex = {'msg': "Added olympiad to the database."}

    return render(request, 'stats/after_adding.html', contex)


def add_athlete_result(request):
    contex = {'msg': "Failed to add athlete results to the database, make sure all fields are correct."}

    name = request.POST['athlete_name']
    if not name:
        return render(request, 'stats/after_adding.html', contex)

    weight = request.POST['weight']
    if weight:
        try:
            weight = int(weight)
        except:
            return render(request, 'stats/after_adding.html', contex)
    else:
        return render(request, 'stats/after_adding.html', contex)

    games = request.POST['games_id']
    if not games:
        return render(request, 'stats/after_adding.html', contex)

    sport = request.POST['sport']
    if not sport:
        return render(request, 'stats/after_adding.html', contex)

    event = request.POST['event']
    if not event:
        return render(request, 'stats/after_adding.html', contex)

    medal = request.POST['medal']
    if not medal:
        return render(request, 'stats/after_adding.html', contex)

    country = request.POST['country']
    if not country:
        return render(request, 'stats/after_adding.html', contex)

    age = request.POST['age']
    if age:
        try:
            age = int(age)
        except:
            return render(request, 'stats/after_adding.html', contex)
    else:
        return render(request, 'stats/after_adding.html', contex)

    # making sure that the athlete exists
    athlete_id = Athlete.objects.get(name__iexact=name).id
    if not athlete_id:
        return render(request, 'stats/after_adding.html', contex)

    # making sure that the olympics exists
    games_id = OlympiadInfo.objects.get(games__iexact=games).games
    if games_id is None:
        return render(request, 'stats/after_adding.html', contex)

    # making sure that the country exists
    country_code = Country.objects.get(country_name__iexact=country).country_code
    if not country_code:
        return render(request, 'stats/after_adding.html', contex)

    new_result = Statistics(player_id_id=athlete_id, weight=weight, games_id=games_id, sport=sport,
                            event=event, medal=medal, country_code_id=country_code, age=age)
    try:
        new_result.save()
    except BadRequest as e:
        return handler_400(request, e)

    if new_result.id:
        contex = {'msg': "Added athlete results to the database."}

    return render(request, 'stats/after_adding.html', contex)


def delete_statistics_by_id(request):
    context = {'msg': "Delete failed. Make sure to put the correct id."}

    stats_id = request.POST['stats_id']
    if stats_id:
        try:
            stats_id = int(stats_id)
        except:
            return render(request, 'stats/after_deleting.html', context)
    else:
        return render(request, 'stats/after_adding.html', context)
    try:
        record = Statistics.objects.get(pk=stats_id)
        record.delete()
    except:
        return render(request, 'stats/after_deleting.html', context)

    context = {'msg': "Successfully deleted the results."}
    return render(request, 'stats/after_deleting.html', context)


def handler_400(request, exception: BadRequest):
    contex = {'msg': str(exception)}
    return render(request, 'stats/error_400.html', contex, status=400)
