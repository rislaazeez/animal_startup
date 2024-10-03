from services.etl import transform_animal

def test_transform_animal():
    animal = {
        "id": 1394,
        "name": "Hippopotamus",
        "born_at": 1682234660289,
        "friends": "Meerkat,Otter"
    }
    transformed = transform_animal(animal)
    
    assert transformed["friends"] ==  ['Meerkat', 'Otter']
    assert transformed["born_at"] == "2023-04-23T07:24:20.289000+00:00"