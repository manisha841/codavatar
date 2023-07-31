# getting user input
name = input("Enter your name")

age = int(input("Enter your age"))

# string formatting in Python

print(f'My name is {name} and my age is {age}')

print('My name is {} and my age is {}'.format(name,age))

#string assignment 

name = 'Manisha'

#string assignment solution(Together)
fname = 'Manisha'
lname = 'Bhandari'

full_name = fname + lname

#lists in Python
num = [1,2,4,5,6,7,8]

sum_ = 0
for n in num:
    sum_ = sum_+n
print(sum_)

print(sum(num))

num1 = [1,2,3,4,5,6]
num2 = [3,9,8,0,1]

print(num1.append(0))

print(num1.extend(num2))

# insert 0 at the first index of list num
num.insert(1,0) 

# access the first element of the list which is zeroth index
print(num1[0]) 

# access the last three elements of list num1 using negative indexing
print(num1[-3:]) 

# remove 1 from list num
num.remove(1) 

# sets and tuples
# Set is a mutable data structure in Python while tuple is non mutable data structure in Python
#sets are defined using curly braces 

empty_set = set()

#even though set is defined with curly brances adding empty curly braces will make a dictionary
empty_set = {} 

#adding and updating elements in set
numbers = {1,2,3,4,5}
numbers.add(6)

numbers.update([0,6]) # can't do numbers.update(0)

print(numbers)

#tuple: unlike list and set, tuple is immutable i.e. once the tuple is created the items inside can't be modified
#tuple is created using parenthesis () separated by commas.

my_tuple = ()

my_tuple = (1,1,2,3,4)

my_tuple[0]

my_tuple[1:3]

my_tuple.count(1)

my_tuple.index(4)


# List Assignment

list1 = [1,2,3]
list2 = [3,5,9]

list1=list1+list2
print(set(list1)) 
# print(list2)

dict1={"a":1,"b":2}

dict2=dict1.copy()
dict2["b"]=3

print(id(dict1))
print(id(dict2))

#booleans and operators in Python


#If else statements: if else are conditionals statements which run once certain conditions are met
weekdays = ['M','T','W','Th','F']
weekends = ['Sat','Sun']

your_day = input('Enter your day')

if your_day in weekdays:
    print('You gotta keep working')

elif your_day in weekends:
    print('Its your day off!')

else:
    pass

#loops in Python: loops are used to iterate over a sequence of data, that can be list,tuple,set,dict, string
# for loop and while loop
for i in range(len(weekdays)):
    print(weekdays[i])

#remove all the occurrence of 1 from the given list.
num = [1,1,2,4,1,2,4]
while 1 in num:
    n.remove(1)



