from Python.lesson_class import Car
import  math

a = 1
b = 0
c = 0
d = 1

x = (((4*(a**2)*(d**2) - 4*a*(b**3) - 8*a*(b**2)*d + 4*a*b*(c**2) - (b**4) - 4*(b**3)*d + 6*(b**2)*(c**2) - 4*(b**2)*(d**2) + 4*(b)*(c**2)*d - (c**4) + 4*(c**2)*(d**2))**(0.5))/(2*(((a**2) + 2*a*b + 2*(b**2) + 2*d*b + (d**2))**(0.5))))
print(x)
diag = (((a+b)**2) + ((c+d)**2))**(0.5)
print(x*diag)
# (sqrt(a^2 + c^2 - x^2) +sqrt(d^2 + b^2 - x^2))^2 = (a+b)^2 + (d+b)^2