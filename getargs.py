def getargs(s):
    # amount of arguments in s
    # there is definitely a better way to do this
    argc = 0
    for c in s:
        if c == ' ':
            argc += 1

    i    = argc
    a    = 0
    argv = []
    while i >= 0:
        stri = ''
        for a,c in enumerate(s):
            if c == ' ':
                s = s.replace(c,"",1)
                break
            else:
                stri += c
                s     = s.replace(c,"",1)
        argv.append(stri)
        i -= 1

    return argc, argv
