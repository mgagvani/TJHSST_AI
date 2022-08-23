# fancy pyhton

# enumerate
example = [3, 6, 5, 4, 7, 11]
for i in range(len(example)):
    print(i, example[i])

for i, val in enumerate(example):
    print(i, val)

# objects are bad do tuple packing
def example_ret():
    a = "epic"
    b = 255
    return a, b

aa, bb = example_ret()
print(aa, bb)

# walrus
if len(example) < 10:
    print(len(example)) # you called len() twice

x = len(example)
if x < 10:
    print(x)

if (x := len(example)) < 10: # assigns to x and also returns
    print(x)

# boolean tricks
if example: #true ish
    print("HI")

l = []
if not l: # false ish
    print("NO")

# comprehensions

new_list = []
for value in example:
    new_list.append(value * 2)

new_list = [value * 2 for value in example]

#pairs of all nunbers if sum is even
newnew = [a + b for a in example for b in new_list if a+b%2 == 0]