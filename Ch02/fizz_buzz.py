class FizzBuzzer:
  def __init__(self):
    self.n = 0
  def foo(self,_):
    self.n += 1
    if (self.n % 3)  == 0:
      x = "buzz"
    else: x = "fizz"
    print(x)
    return x

FB = FizzBuzzer()
for i in range(21):
  FB.foo(i)
