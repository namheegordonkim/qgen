glossary_f = open("glossary.txt", "r")
lines = glossary_f.readlines()
glossary_f.close()

sublines = lines[1:]
sublines.sort()

glossary_f = open("glossary.txt", "w")

for line in [lines[0]] + sublines:
    glossary_f.write(line)

glossary_f.close()
