from .models import Base, Patrol, Intelligence

# Import data by running the following:
# python manage.py shell -c 'from RadioActiv8 import test_data;
# test_data.load()'


def load_model(model, keys, values_list):
    print(f"Loading {model.__name__}s...")
    for values in values_list:
        # Convert to list
        entity = dict(zip(keys, values))
        # Remove empty values
        entity = {k: v for k, v in entity.items() if v is not None}
        model(**entity).save()


# Return the first result of a given object time whose key matches the chosen
# value


def find_first_object(model, key, value):
    return model.objects.filter(**{key: value}).first()


# Return the first base with the given name


def named_base(name):
    return find_first_object(Base, "name", name)


# Return the first patrol with the given name


def named_patrol(name):
    return find_first_object(Patrol, "name", name)


def load():
    # Base data
    base_keys = ["name", "gps_location", "min_patrols", "max_patrols"]
    base_values_list = [
        ["Yellow", None, 0, 0],
        ["Red", None, 0, 0],
        ["Green", None, 0, 0],
        ["Blue", None, 0, 0],
        ["Pink", None, 0, 0],
        ["Black", None, 0, 0],
        ["Orange", None, 0, 0],
        ["Purple", None, 0, 0],
        ["Grey", None, 0, 0],
        ["Brown", None, 0, 0],
        ["Aqua", None, 0, 0],
        ["Indigo", None, 0, 0],
    ]
    load_model(Base, base_keys, base_values_list)

    # Patrol data
    patrol_keys = ["name"]
    patrol_values_list = [
        ["Maverick"],
        ["Goose"],
        ["Iceman"],
        ["Viper"],
    ]
    load_model(Patrol, patrol_keys, patrol_values_list)

    # Intelligence data
    intelligence_keys = ["base", "question", "answer"]
    intelligence_values_list = [
        [named_base("Yellow"), "A", "Moira"],
        [named_base("Yellow"), "B", "Barry's Reef"],
        [named_base("Yellow"), "C", "Pax Hill"],
        [named_base("Yellow"), "D", "Mafeking"],
        [named_base("Yellow"), "E", "Bermingham"],
        [named_base("Yellow"), "F", "Eumeralla"],
        [named_base("Red"), "A", "Brucknell"],
        [named_base("Red"), "B", "Noonameena"],
        [named_base("Red"), "C", "Gilwell"],
        [named_base("Red"), "D", "Treetops"],
        [named_base("Red"), "E", "Lake Fyans"],
        [named_base("Red"), "F", "Rowallan"],
        [named_base("Green"), "A", "Cresco"],
        [named_base("Green"), "B", "Mataranka"],
        [named_base("Green"), "C", "Camp Niall"],
        [named_base("Green"), "D", "WF Waters Lodge"],
        [named_base("Green"), "E", "Warburton"],
        [named_base("Green"), "F", "Lake Eppalock"],
        [named_base("Blue"), "A", "Clifford Park"],
        [named_base("Blue"), "B", "Gunbower Island"],
        [named_base("Blue"), "C", "Bay Park"],
        [named_base("Blue"), "D", "Mallangeeba"],
        [named_base("Blue"), "E", "Alpine Adventure Centre"],
        [named_base("Blue"), "F", "Cooinda-Burrong"],
        [named_base("Pink"), "A", "Patanga"],
        [named_base("Pink"), "B", "Koolamurt"],
        [named_base("Pink"), "C", "Dallas Brooks"],
        [named_base("Pink"), "D", "Caringal"],
        [named_base("Pink"), "E", "Warringal"],
        [named_base("Pink"), "F", "Heany Park"],
        [named_base("Black"), "A", "Melbourne"],
        [named_base("Black"), "B", "Mt Dandenong"],
        [named_base("Black"), "C", "Plenty Valley"],
        [named_base("Black"), "D", "Lerderderg"],
        [named_base("Black"), "E", "Bays"],
        [named_base("Black"), "F", "Gippsland"],
        [named_base("Orange"), "A", "BAYWAC"],
        [named_base("Orange"), "B", "Captain Hurley Rover Hut"],
        [named_base("Orange"), "C", "GWS Anderson"],
        [named_base("Orange"), "D", "Clive Disher Park"],
        [named_base("Orange"), "E", "Harkaway"],
        [named_base("Orange"), "F", "Connan Park"],
        [named_base("Purple"), "A", "Northern Rivers"],
        [named_base("Purple"), "B", "Wimmera"],
        [named_base("Purple"), "C", "Ballarat"],
        [named_base("Purple"), "D", "Glenelg River"],
        [named_base("Purple"), "E", "Otway Plains"],
        [named_base("Purple"), "F", "Barwon"],
        [named_base("Grey"), "A", "Geelong"],
        [named_base("Grey"), "B", "West Coast"],
        [named_base("Grey"), "C", "Western"],
        [named_base("Grey"), "D", "Loddon-Mallee"],
        [named_base("Grey"), "E", "Northern"],
        [named_base("Grey"), "F", "Sunraysia"],
        [named_base("Brown"), "A", "Bendigo"],
        [named_base("Brown"), "B", "Alpine Gateway"],
        [named_base("Brown"), "C", "Goulburn Murray"],
        [named_base("Brown"), "D", "River Gums"],
        [named_base("Brown"), "E", "Upper Murray"],
        [named_base("Brown"), "F", "South Gippsland"],
        [named_base("Aqua"), "A", "South Western"],
        [named_base("Aqua"), "B", "Frankston"],
        [named_base("Aqua"), "C", "Geelong Rivers"],
        [named_base("Aqua"), "D", "East Gippsland"],
        [named_base("Aqua"), "E", "Mt Baw Baw"],
        [named_base("Aqua"), "F", "Strzelecki"],
        [named_base("Indigo"), "A", "Wellington"],
        [named_base("Indigo"), "B", "Kingston"],
        [named_base("Indigo"), "C", "Emu"],
        [named_base("Indigo"), "D", "Geelong Peninsula"],
        [named_base("Indigo"), "E", "Cardinia"],
        [named_base("Indigo"), "F", "Casey"],
    ]
    load_model(Intelligence, intelligence_keys, intelligence_values_list)
