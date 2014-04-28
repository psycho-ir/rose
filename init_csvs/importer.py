import csv


class Town:
    def __init__(self, _province, _town):
        self.province = _province
        self.town = _town

    def __str__(self):
        return self.province + '    ' + self.town + '   ' + str(self.province_id)


class Province:
    def __init__(self, _id, _name):
        self.id = _id
        self.name = _name


provinces = set()
rigid_provinces = set()
towns = set()

with open('province_town.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)
    for row in reader:
        provinces.add(row[0])
        towns.add(Town(row[0], row[2]))
        #print ', '.join(row)

    id_generator = 1

    for p in provinces:
        rigid_provinces.add(Province(id_generator, p))
        id_generator += 1

    for t in towns:
        t.province_id = list((x.id for x in rigid_provinces if x.name == t.province))[0]
        # print t

    for p in rigid_provinces:
        pass
        # print('{"model":"rose_config.province", "pk":"' + str(p.id) + '","fields":{"name":"' + str(
        #     p.name) + '","local_name":"' + str(p.name) + '"}},')

    id_generator = 1
    for t in towns:
        print('{"model":"rose_config.town", "pk":"' + str(id_generator) + '","fields":{"name":"' + str(
            t.town) + '","local_name":"' + str(t.town) + '","province":"' + str(t.province_id) + '"}},')
        id_generator += 1

print(len(towns))

