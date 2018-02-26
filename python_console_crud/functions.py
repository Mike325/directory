# coding:utf-8

from data import *


def get_spaces():
    for record in elements:
        for key, value in record.items():
            value_length = len(value)
            translit_length = len(translits[key])

            if spaces[key] < value_length or spaces[key] < translit_length:
                if value_length > translit_length:
                    spaces[key] = value_length
                else:
                    spaces[key] = translit_length
    return spaces


        
def print_to_console():
    if elements:
        print "========================================================================================================"
        spaces = get_spaces()
        print '| id | Name{name_space}| Last Name{last_name_space}| Address{address_space}| Cellphone{cellphone_space}| Email{email_space}| Social Network{social_network_space}|'.format(
            name_space = ' ' * (spaces['name']-len(translits['name'])+1),
            last_name_space = ' ' * (spaces['last_name']-len(translits['last_name'])+1),
            address_space = ' ' * (spaces['address']-len(translits['address'])+1),
            cellphone_space = ' ' * (spaces['cellphone']-len(translits['cellphone'])+1),
            email_space = ' ' * (spaces['email']-len(translits['email'])+1),
            social_network_space = ' ' * (spaces['social_network']-len(translits['social_network'])+1),
        )
        for element in elements:
            id_space = ' ' * (spaces['id']-len(element['id']))
            name_space = ' ' * (spaces['name']-len(element['name']))
            last_name_space = ' ' * (spaces['last_name']-len(element['last_name']))
            address_space = ' ' * (spaces['address']-len(element['address']))
            cellphone_space = ' ' * (spaces['cellphone']-len(element['cellphone']))
            email_space = ' ' * (spaces['email']-len(element['email']))
            social_network_space = ' ' * (spaces['social_network']-len(element['social_network']))
            print '| {id} | {name} | {last_name} | {address} | {cellphone} | {email} | {social_network} |'.format(
                id = element['id']+id_space,
                name = element['name'] + name_space,
                last_name = element['last_name'] + last_name_space,
                address = element['address'] + address_space,
                cellphone = element['cellphone'] + cellphone_space,
                email = element['email'] + email_space,
                social_network = element['social_network'] + social_network_space
            )
        print "========================================================================================================"
    else:
        print 'Empty directory'


def get_next_id():
    if len(elements):
        max_id = int(max(i['id'] for i in elements))
        return str(max_id + 1)
    return 0