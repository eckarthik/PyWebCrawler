def fun():
    return (1,2)

print(type(fun()))

if isinstance(fun(),tuple):
    print("It was a tuple")

