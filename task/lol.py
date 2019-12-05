lol = [1, 2, 3, 4, 5, 6, 7, 8]
sec = [2, 4, 6, 8]

for i in lol:
    if i in sec:
        lol.remove(i)

print(lol)
