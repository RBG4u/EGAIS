import pandas as pd

from objects import Beer
from save_files import make_xlsx


def name_reference_check(beer, ost):
    ost_name = ost[ost['Номенклатура'].str.contains(beer.name, na=False)]
    for index, row in ost_name.iterrows():
        if row['Количество'] >= beer.count and beer.count != 0:
            beer.new_references.append([beer.count,
                                        row['Справка 2'],
                                        row['Дата подтверждения ЕГАИС']])
            row['Количество'] -= beer.count
            beer.count = 0
            ost.loc[ost['N'] == row['N'], 'Количество'] = row['Количество']
        if row['Количество'] < beer.count and row['Количество'] != 0:
            beer.new_references.append([row['Количество'],
                                        row['Справка 2'],
                                        row['Дата подтверждения ЕГАИС']])
            beer.count -= row['Количество']
            row['Количество'] = 0
            ost.loc[ost['N'] == row['N'], 'Количество'] = row['Количество']

    return ost


def alc_prod_reference_check(beer, ost):
    ost_name = ost[ost['Алкогольная продукция'].str.contains(beer.alc_prod, na=False)]
    for index, row in ost_name.iterrows():
        if row['Количество'] >= beer.count and beer.count != 0:
            beer.new_references.append([beer.count,
                                        row['Справка 2'],
                                        row['Дата подтверждения ЕГАИС']])
            row['Количество'] -= beer.count
            beer.count = 0
            ost.loc[ost['N'] == row['N'], 'Количество'] = row['Количество']
        if row['Количество'] < beer.count and row['Количество'] != 0:
            beer.new_references.append([row['Количество'],
                                        row['Справка 2'],
                                        row['Дата подтверждения ЕГАИС']])
            beer.count -= row['Количество']
            row['Количество'] = 0
            ost.loc[ost['N'] == row['N'], 'Количество'] = row['Количество']

    return ost


def creating_correct_rows(row, beer, act_new, act_del):
    for ref in beer.new_references:
        row['Количество'] = ref[0]
        row['Справка 2'] = ref[1]
        row['Дата подтверждения ЕГАИС'] = ref[2]
        act_new.loc[len(act_new)] = row
    if beer.count != 0:
        row['Количество'] = beer.count
        row['Справка 2'] = 'NaN'
        act_del.loc[len(act_del)] = row
    return act_new, act_del


def drop_dal(ost):
    indexes_to_drop = ost[ost['Номенклатура'].str.contains('ДАЛ', na=False)].index
    ost_drop_dal = ost.drop(indexes_to_drop, axis=0)

    return ost_drop_dal


def make_acts(act_path, ost_path, save_path):
    act = pd.read_excel(act_path)
    ost = pd.read_excel(ost_path)

    ost = drop_dal(ost)

    act_new = act.drop(act.index, axis=0)
    act_del = act.drop(act.index, axis=0)
    for index, row in act.iterrows():
        beer = Beer(name=row['Номенклатура'],
                    alc_prod=row['Алкогольная продукция'],
                    count=row['Количество'],
                    reference=row['Справка 2'],
                    new_references=[])
        if ost['Номенклатура'].isin([beer.name]).any():
            ost = name_reference_check(beer, ost)
        if ost['Алкогольная продукция'].isin([beer.alc_prod]).any() and beer.count != 0:
            ost = alc_prod_reference_check(beer, ost)

        act.loc[index, 'Справка 2'] = 'del'

        act_new, act_del = creating_correct_rows(row, beer, act_new, act_del)

    act_new['N'] = act_new.apply(lambda row: row.name + 1, axis=1)

    make_xlsx(act_new, act_del, save_path)


def creation_of_acts(act_path, ost_path, save_path):
    try:
        make_acts(act_path, ost_path, save_path)
        return 'Готово'
    except pd.errors.EmptyDataError:
        return 'Ошибка: один из файлов пустой!'
    except pd.errors.ParserError:
        return 'Ошибка: неправильный формат файла!'
    except FileNotFoundError:
        return 'Ошибка: файл не найден!'
    except PermissionError:
        return 'Ошибка: путь сохранения не задан!'
    except KeyError as err:
        return f'Ошибка: не найдена кололнка {str(err)}'
    except ValueError as err:
        return f'Ошибка: {str(err)}'
