import re

class PhoneFormatter:
    def __init__(self):
        self.r = re.compile(r"\d")
        
    def pretty_format(self, phone_number):
        numbers = self.r.findall(phone_number)
        area_code = "".join(numbers[-10:-7])
        first_3 = "".join(numbers[-7:-4])
        last_4 = "".join(numbers[-4:len(numbers)])
        return "({}) {}-{}".format(area_code, first_3, last_4)

if __name__ == "__main__":
    phone_numbers = [
        "(123) 456-7890",
        "1234567890",
        "123.456.7890",
        "+1 123 456-7890"
    ]

    P = PhoneFormatter()

    print(list(map(P.pretty_format, phone_numbers)))