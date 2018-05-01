with open('myIndex/index.txt', 'a+') as f:
    f.seek(0)
    for line in f:
        print line.rstrip('\n')
    f.write('input')