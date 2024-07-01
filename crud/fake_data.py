from faker import Faker

fake = Faker('ru_RU')
print(fake.name())

print(fake.job())

print(fake.date())

# зарплата ? либо просто числол и ф строка Руб

emloyer_dict = []
for name in range(100):
    emloyer_dict.append({"name": fake.name(), "job": fake.job(), "data": fake.date()})
print(emloyer_dict)

