import matplotlib.pyplot as plt

files = ["ping_cabo","ping_2.4g","ping_5g"]
number=0
for file_name in files:
    file = open(f'{file_name}','r')
    info = file.readlines()
    values =[]
    check_number=0
    for sample, line in enumerate(info):
        check_number+=1
        values.append((float(line.split(" ")[6].split('=')[1])))

    plt.plot(values,label=f"{file_name}")
    file.close()
    if check_number > number:
        number = check_number


plt.xlim([0,number])
plt.ylabel("Ping (ms)")
plt.legend()
plt.show()