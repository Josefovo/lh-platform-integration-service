def test_add_greeting(model, db):
    model.greetings.add_greeting('ahoj')
    assert db['greetings'].find_one()['text'] == 'ahoj'
