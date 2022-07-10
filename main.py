
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# преобразование телефонов к единому виду
  list_for_csv = []
  for row in contacts_list:
    text = ",".join(row)
    patern = re.compile(
      r"(\+7|8[^@])\s?\(?(\d{,3})\)?\s?\-?(\d{,3})\-?(\d{,2})\-?(\d{,2})\s?\(?(\w?\w?\w?\.?)\s?(\d?\d?\d?\d?)\)?")
    substitute = r"+7(\2)\3-\4-\5 \6\7"
    resoult = patern.sub(substitute, text)
    new_text = resoult.split(',')
    list_for_csv.append(new_text)

  # расставление ФИО на свои места
  for index, element in enumerate(list_for_csv):
    if index != 0 and index <= len(list_for_csv)-1:
      el = ' '.join(list_for_csv[index]).split(' ')[0:3]
      for ids, name in enumerate(list_for_csv[index]):
        if ids <= 2:
          list_for_csv[index][ids] = el[ids]

  # объединение дублей
  dict_for_index = {}
  name_list = []
  duble_list = []
  for id_1, element_list in enumerate(list_for_csv):
    name_list.append(element_list[0:2])
    if name_list.count(name_list[id_1]) > 1:
      duble_list.append(list_for_csv[id_1][0:2])

  for element_db in duble_list:
    for id_row, list_row in enumerate(list_for_csv):
      if element_db == list_for_csv[id_row][0:2]:
        dict_for_index.update({id_row: list_for_csv[id_row]}) #вспомогательный словарь из фамилий имен дублей

  count = 0
  position_1 = 0
  position_2 = 0
  person_list = []
  full_person_list = []

  def update_info(position_1, position_2):
    for id, elmt in enumerate(list_for_csv[position_1]):
      person_list.append(elmt)
      if '' == person_list[id]:
        person_list[id] = list_for_csv[position_2][id]

    add_list = list.copy(person_list)
    full_person_list.append(add_list) #объединение информации из дублей
    person_list.clear()

  for key in dict_for_index.keys(): # частный случай для двух пар задублированных позици(
    count += 1
    for id, el in enumerate(list_for_csv):
      if dict_for_index[key] == list_for_csv[id] and count == 1:
        position_1 = key
      if dict_for_index[key] == list_for_csv[id] and count == 2:
        position_2 = key
        update_info(position_1, position_2)
      if dict_for_index[key] == list_for_csv[id] and count == 3:
        position_1 = key
      if dict_for_index[key] == list_for_csv[id] and count == 4:
        position_2 = key
        update_info(position_1, position_2)


  for id_fl, pos in enumerate(full_person_list):
    for id_lfc, pos_lfc in enumerate(list_for_csv):
      if list_for_csv[id_lfc][0:2] == full_person_list[id_fl][0:2]:
        list_for_csv[id_lfc] = full_person_list[id_fl]
  for pos_duble in list_for_csv:
    if list_for_csv.count(pos_duble) > 1:
      list_for_csv.remove(pos_duble)


# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(list_for_csv)
