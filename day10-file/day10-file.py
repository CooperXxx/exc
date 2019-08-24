import json


def main():
    # with open("cfile.txt",'x',encoding="utf-8") as f:
    #     f.write("fwqfqfgvwdfgvwegvwefgv\n"
    #             "qfwklfnlqwfqw  啊")

    # f.close()


    # filelist=['d','e','f']
    # fs=[open(x+"file.txt",'x',encoding="utf-8") for x in filelist]
    # for f in fs:
    #     # print(f.read())
    #     f.write("45157452757nfghjfg5\n")
    #     f.seek(5,0)
    #     print(f.read())

    mydict = {
        'name': '骆昊',
        'age': 38,
        'qq': 957658,
        'friends': ['王大锤', '白元芳'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'Audi', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }
    sstr=json.dumps(mydict)


    with open("jsonfile.txt", 'r', encoding="utf-8") as f:
        # json.dump(mydict,f)
        # f.write(mydict)
        dd= json.load(f)
    print(dd)
    dicc = json.loads(sstr)
    # print(mydict)
    # print(dicc)



if __name__ == '__main__':
    main()