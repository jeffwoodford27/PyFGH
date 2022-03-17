class input_object:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class output_object:
    def __init__(self,z):
        self.z = z

bob = input_object(2,3)

# send bob to child process
# child process creates doug by adding x and y contained within bob

sum = bob.x + bob.y
doug = output_object(sum)

# child process sends doug back to parent process

print(doug.z)

