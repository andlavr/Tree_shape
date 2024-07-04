import random

from faker import Faker
import json

fake = Faker('ru_RU')
print(fake.name())

print(fake.job())

print(fake.date())

# зарплата ? либо просто числол и ф строка Руб

employer_dict = []
for name in range(100):
    employer_dict.append({"name": fake.name(), "job": fake.job(), "salary": random.randint(10000, 100000), "data": fake.date()})
print(employer_dict)




with open('employer_dict.json', 'w') as employer_file:
    json.dump(employer_dict, employer_file, ensure_ascii=False, indent=4)

with open('employer_dict.json', 'r') as employer_file:
    employer_dict = json.load(employer_file)

# print(employer_dict[1]['salary'])
for mini_dict in employer_dict:
    # print(mini_dict['name'], mini_dict['job'], mini_dict['salary'])
    name_ = mini_dict["name"]

    salary_ = mini_dict["salary"]
    job = mini_dict["job"]
    surname = name_.split()[0]
    personal_name = name_.split()[1]
    patronymic = name_.split()[2]


#
