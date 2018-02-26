#!/usr/bin/python
# coding:utf-8

from functions import *


# ==================== CREATE ====================
def create_record():
    name = raw_input('Enter name: ')
    last_name = raw_input('Enter last name: ')
    address = raw_input('Enter address: ')
    cellphone = raw_input('Enter cellphone: ')
    email = raw_input('Enter email address: ')
    social_network = raw_input('Enter social network: ')
    for record in elements:
        if set([name, last_name, address, cellphone, email, social_network]).issubset(record.values()):
            print 'Record: {name} {last_name} {cellphone} is already in the database'
            return
    if name and last_name and cellphone:
        elements.append({
            'id': get_next_id(),
            'name': name,
            'last_name': last_name,
            'address': address,
            'cellphone': cellphone,
            'email': email,
            'social_network': social_network
        })
        print 'User added successfully'
    else:
        print 'You have added empty values' 
        
        
# ==================== UPDATE ====================
def update_record():
    if elements:
        print_to_console()
        record_id = raw_input('Input the user key: ')
        for record in elements:
            if record['id'] == record_id:
                for key, value in record.items():
                    if key == 'id':
                        continue
                    new_record = raw_input(
                        'Actual Value -> {current_name}: {current_record}, Enter new value or leave it empty: '.format(
                            current_name = translits.get(key), current_record = value
                        )
                    )
                    if new_record:
                        record[key] = new_record
                        print 'User updated successfully'
                break
        else:
            print 'User not found'
    else:
        print 'No elements to show'


# ==================== DELETE ====================
def delete_record():
    if elements:
        print_to_console()
        record_id = raw_input('Enter user ID: ')
        for record in elements:
            if record['id'] == record_id:
                elements.remove(record)
                print 'User deleted successfully'
                break
        else:
            print 'User not found'
    else:
        print 'No elements to show'


# ==================== MAIN ====================
def main():
    while True:
        action = raw_input(MAIN_MENU)
        if action == '1':
            create_record()
        elif action == '2':
            print_to_console()
        elif action == '3':
            update_record()
        elif action == '4':
            delete_record()
        elif action == 'E' or 'e':
            break
        else:
            print 'Sin acción en {action}'.format(action=action)


if __name__ == '__main__':
    main()
