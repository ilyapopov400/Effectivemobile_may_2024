a = ["yes", "no", False]

print(a)

b = filter(lambda x: bool(x), a)
print(*b)