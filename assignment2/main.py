#dictionaries in Python: dictionaries are the data structure in Python which has key value pair as the data format. Dictionaries are unordered, indexed by keys.

#creating an empty dictionary
my_dict = dict()
my_dict = {}

#adding and updating items in the dictionary
my_dict = {
    'name':'Manisha',
    'age': 23,
    'address': 'Kirtipur, Kathmandu'
}

my_dict['country'] = 'Nepal'

my_dict.update(dict(gender = 'Female'))

#accessing elements with get and keys
my_dict['address']

my_dict.get('address',None)

new_dict = my_dict.copy()

for key, value in my_dict.items():
    print(key,value)

if 'origin' in my_dict:
    pass
else:
    my_dict['origin'] = 'Kirtipur'

#Functions in Python
def solution(sentence):
    words = sentence.split()
    return '#'.join(words)

solution('What is your name?')