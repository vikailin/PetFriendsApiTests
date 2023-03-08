import pytest
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, invalid_auth_key
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Bam', animal_type='rat', age='2',
                                     pet_photo='images/b14.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert status == 200
    assert result['name'] == name
    assert my_list['pets'][0]['name'] == name


def test_update_pet_info_with_valid_data(name='Bob', animal_type='dog', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_list['pets']) > 0:
        pet_id = my_list['pets'][0]['id']
        status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
        _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
        assert status == 200
        assert result['name'] == name
        assert my_list['pets'][0]['name'] == name
    else:
        raise Exception("There is no my pets")


def test_delete_pet_by_pet_id_successfully():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_list['pets']) > 0:
        pet_id = my_list['pets'][0]['id']
        status = pf.delete_pet_by_pet_id(auth_key, pet_id)
        assert status == 200
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_simple_with_valid_data(name='Bonnie', animal_type='cat', age='7'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    assert status == 200
    assert result['name'] == name
    assert my_list['pets'][0]['name'] == name


def test_add_photo_of_pet_with_valid_data(pet_photo='images/cat1.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if len(my_list['pets']) > 0:
        pet_id = my_list['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
        assert status == 200
        assert result['pet_photo'] == my_list['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")


def test_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    print(f'\nResponse status: {status}. Api_key not received.\n{result}')
    assert 'key' not in result


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    print(f'\nResponse status: {status}. Api_key not received.\n{result}')
    assert 'key' not in result


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status != 200
    print(f'\nResponse status: {status}. Api_key not received.\n{result}')
    assert 'key' not in result


def test_add_new_pet_simple_with_invalid_auth_key(name='Bonnie', animal_type='cat', age='7'):
    auth_key = invalid_auth_key
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status != 200
    print(f'\nResponse status: {status}.\n{result}')


def test_add_new_pet_simple_with_empty_data(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if status == 200:
        assert result['name'] == name
        assert my_list['pets'][0]['name'] == name
        print('\nСистема допускает добавление питомца с пустыми данными!')
    else:
        assert name not in result['name']
        assert name not in my_list['pets'][0]['name']
        print('\nСистема не допускает добавление питомца с пустыми данными.')


def test_add_new_pet_simple_with_name_consisting_of_symbols(name='@#$%^&*()-±?`~|/=+',
                                                            animal_type='dog', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if status == 200:
        assert result['name'] == name
        assert my_list['pets'][0]['name'] == name
        print(f'\nСистема допускает добавление имени питомца, состоящего из символов!\n{result}')
    else:
        assert name not in result['name']
        assert name not in my_list['pets'][0]['name']
        print('\nСистема не допускает добавление питомца с именем, состоящим из символов.')


def test_add_new_pet_simple_with_very_long_name(animal_type='dog', age='1'):
    name = 'CpeZ5e69i1u20zqzveOx32Snjr0OFliAvzOhtdIJRQqJ8zQkK2Vwjl8CaZ2A6UyJp1Lv9zP0pw6nRQ9a0tov0nOfN3pf1fGH2uRs'
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if status == 200:
        assert result['name'] == name
        assert my_list['pets'][0]['name'] == name
        print(f'\nСистема допускает добавление имени питомца, состоящего из {len(name)} символов!\n{result}')
    else:
        assert name not in result['name']
        assert name not in my_list['pets'][0]['name']
        print(f'\nСистема не допускает добавление питомца с очень длинным именем ({len(name)} символов).\n{result}')


def test_add_new_pet_simple_with_non_standard_animal_type(name='Lucky',
                                                            animal_type="rabbit's foot", age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if status == 200:
        assert result['animal_type'] == animal_type
        assert my_list['pets'][0]['animal_type'] == animal_type
        print(f'\nСистема допускает добавление нестандартных значений типа животного!\n{result}')
    else:
        assert animal_type not in result['animal_type']
        assert animal_type not in my_list['pets'][0]['animal_type']
        print('\nСистема не допускает добавление нестандартных значений типа животного.')


def test_add_new_pet_simple_with_non_standard_age(name='Fairy', animal_type='goldfish', age='10000'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    _, my_list = pf.get_list_of_pets(auth_key, filter='my_pets')
    if status == 200:
        assert result['age'] == age
        assert my_list['pets'][0]['age'] == age
        print(f'\nСистема допускает добавление невозможных значений возраста животного!\n{result}')
    else:
        assert age not in result['age']
        assert age not in my_list['pets'][0]['age']
        print('\nСистема не допускает добавление невозможных значений возраста животного.')
