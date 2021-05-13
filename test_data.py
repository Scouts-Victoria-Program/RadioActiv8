from .models import *

# Import data by running the following:
#   python manage.py shell -c 'from RadioActiv8 import test_data; test_data.load()'

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
        return find_first_object(Base, 'name', name)

# Return the first patrol with the given name
def named_patrol(name):
        return find_first_object(Patrol, 'name', name)

def load():

    # Base data
    base_keys = ['name', 'gps_location', 'min_patrols', 'max_patrols']
    base_values_list = [
            ['Black', None, 0, 0],
            ['Green', None, 0, 0],
            ['Orange', None, 0, 0],
            ['Pink', None, 0, 0],
            ['Red', None, 0, 0],
            ['Yellow', None, 0, 0],
            ]
    load_model(Base, base_keys, base_values_list)

    # Patrol data
    patrol_keys = ['name', 'gps_location']
    patrol_values_list = [
            ['Maverick', None],
            ['Goose', Point(144, -36)],
            ['Iceman', 'POINT(-95.3385 29.7245)'],
            ['Viper', None],
            ]
    load_model(Patrol, patrol_keys, patrol_values_list)

    # Intelligence data
    intelligence_keys = ['base', 'question', 'answer']
    intelligence_values_list = [
            [named_base('Pink'), 'a', '1'],
            [named_base('Orange'), 'b', '2'],
            ]
    load_model(Intelligence, intelligence_keys, intelligence_values_list)

    # Queue data
    queue_keys = ['sequence', 'base', 'patrol']
    queue_values_list = [
            [1, named_base('Pink'),   named_patrol('Maverick')],
            [2, named_base('Black'),  named_patrol('Goose')],
            [3, named_base('Yellow'), named_patrol('Iceman')],
            [4, named_base('Green'),  named_patrol('Viper')],
            [5, named_base('Orange'), named_patrol('Maverick')],
            [6, named_base('Red'),    named_patrol('Goose')],
            [7, named_base('Black'),  named_patrol('Iceman')],
            [8, named_base('Yellow'), named_patrol('Viper')],
            ]
    load_model(Queue, queue_keys, queue_values_list)