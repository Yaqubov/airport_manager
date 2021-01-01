import requests
from requests.auth import HTTPDigestAuth
import json
import argparse
from termcolor import colored
from getpass import getpass

BASE = 'http://127.0.0.1:5000/'


class User():
    def __init__(self):
        self.token = None
        self.username = None
        self.password = None

    def get(self):
        print(colored("Write parameters of flight which you want to get", 'yellow'))
        url = BASE + 'flights' + '/' + \
            input("From city: ") + "/" + input("To city: ")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                flights = response.json()
                for i in flights:
                    print(colored(
                        f"{i['frm']} --> {i['to']} \nDeparture time: {i['departure']}\nArrival time: {i['arrival']}\nAirplane: {i['airplane']}\nPassengers: {i['passengers']}\n-------------------------------------", 'green'))
            else:
                print(colored(response.json()['message'], 'red'))
        except:
            print('error')

    def delete(self):
        print(colored("Write parameters of flight you want to delete", 'yellow'))
        url = BASE + 'flights' + '/' + \
            input("From city: ") + "/" + input('To city: ')
        header = {'x-access-tokens': self.token}
        try:
            response = requests.delete(url, headers=header)
            if response.status_code == 200:
                print(colored(response.json(), 'green'))
            else:
                print(colored(response.json(), 'red'))
        except:
            print('error')

    def put(self):
        print(colored("Write parameters of flight you want to update", 'yellow'))
        url = BASE + 'flights' + '/' + \
            input("From city:") + "/" + input("To ciy")
        header = {'content-type': 'application/json',
                  'x-access-tokens': self.token}
        print("Write parameters you want to update")
        payload = {
            "frm": input('From city: '),
            "to": input("To city: "),
            "departure": input("Departure Time: "),
            "arrival": input("Arrival Time: "),
            "airplane": input("Airplane Info: "),
            "passengers": input("Passengers count: ")
        }
        data = {}

        for key in payload:
            if payload[key]:
                data[key] = payload[key]
        try:
            response = requests.put(
                url, json.dumps(data), headers=header)
            if response.status_code == 200:
                print(colored(response.json(), 'green'))
            else:
                print(colored(response.json(), 'red'))
        except:
            print('error')

    def post(self):
        url = BASE + 'flights'
        print(colored("Write parameters of flight you want to add", 'yellow'))
        payload = {
            "frm": input('From city: '),
            "to": input("To city: "),
            "departure": input("Departure Time: "),
            "arrival": input("Arrival Time: "),
            "airplane": input("Airplane Info: "),
            "passengers": input("Passengers count: ")
        }
        data = {}

        for key in payload:
            if payload[key]:
                data[key] = payload[key]

        header = {'content-type': 'application/json',
                  'x-access-tokens': self.token}
        try:
            response = requests.post(
                url, data=json.dumps(data), headers=header)
            if response.status_code == 201:
                print(colored(response.json(), 'green'))
            else:
                print(colored(response.json(), 'red'))
        except:
            print('error')

    def authen_author(self):
        print(colored("Write the username and password to login as admin", 'yellow'))
        self.username = input("Username: ")
        self.password = getpass()

        response = requests.get(
            BASE+'authentication_authorization', auth=(self.username, self.password))
        if response.status_code == 200:
            token = response.json()
            self.token = token
            print(colored('Succesful login!', 'green'))
        else:
            print(colored(response.json()['message'], 'red'))

    def end_session(self):
        self.token = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--admin', help='logging as admin',
                        action="store_true")
    args = parser.parse_args()
    if args.admin:
        while True:
            user = User()
            print('1.Login \n2.Exit')
            opt = int(input(colored('Select option: ', 'yellow')))
            if opt == 1:
                user.authen_author()
                if user.token:
                    while True:
                        print(
                            'What do you want to do? \n1. Add a new flight \n2. Update a flight \n3. Delete a flight \n4. Get a flight \n5. Log out')
                        option = int(
                            input(colored('Select option: ', 'yellow')))
                        if option == 1:
                            user.post()
                        elif option == 2:
                            user.put()
                        elif option == 3:
                            user.delete()
                        elif option == 4:
                            user.get()
                        elif option == 5:
                            user.end_session()
                            break
                        else:
                            print(colored('No such an option', 'red'))
            elif opt == 2:
                break
            else:
                print(colored('No such a option', 'red'))
    else:
        user = User()
        while True:
            print('1.Find flight \n2.Exit')
            option = int(input(colored('Select option: ', 'yellow')))
            if option == 1:
                user.get()
            elif option == 2:
                break
            else:
                print(colored('No such an option', 'red'))


if __name__ == '__main__':
    main()
