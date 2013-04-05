ADDRESS = 'http://localhost:8080/troia-server-1.0'

ITERATIONS = 5

CATEGORIES = ["porn", "notporn"]

CATEGORY_PRIORS = [{"categoryName": "porn", "value": 0.5}, {"categoryName": "notporn", "value": 0.5}]

COST_MATRIX = [{"from": "porn", "to": "notporn", "value": 1.0}, {"from": "porn", "to": "porn", "value": 0.0}, 
               {"from": "notporn", "to": "porn", "value": 1.0}, {"from": "notporn", "to": "notporn", "value": 0.0}]

ASSIGNED_LABELS = [
    ('worker1', 'url1', 'porn'),
    ('worker1', 'url2', 'porn'),
    ('worker1', 'url3', 'porn'),
    ('worker1', 'url4', 'porn'),
    ('worker1', 'url5', 'porn'),
    ('worker2', 'url1', 'notporn'),
    ('worker2', 'url2', 'porn'),
    ('worker2', 'url3', 'notporn'),
    ('worker2', 'url4', 'porn'),
    ('worker2', 'url5', 'porn'),
    ('worker3', 'url1', 'notporn'),
    ('worker3', 'url2', 'porn'),
    ('worker3', 'url3', 'notporn'),
    ('worker3', 'url4', 'porn'),
    ('worker3', 'url5', 'notporn'),
    ('worker4', 'url1', 'notporn'),
    ('worker4', 'url2', 'porn'),
    ('worker4', 'url3', 'notporn'),
    ('worker4', 'url4', 'porn'),
    ('worker4', 'url5', 'notporn'),
    ('worker5', 'url1', 'porn'),
    ('worker5', 'url2', 'notporn'),
    ('worker5', 'url3', 'porn'),
    ('worker5', 'url4', 'notporn'),
    ('worker5', 'url5', 'porn')]

GOLD_SAMPLES = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
    ]

EVALUATION_DATA = [
    ('url1', 'notporn'),
    ('url2', 'porn'),
    ('url3', 'notporn'),
    ('url4', 'porn'),
    ('url5', 'notporn')
]

OBJECTS = ['url1', 'url2', 'url3', 'url4', 'url5']
