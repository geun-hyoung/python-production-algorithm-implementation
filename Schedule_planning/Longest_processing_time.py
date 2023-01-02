def LPT():
    order_table = open('../data/orderlist16_5_10.txt', 'r')

    num1_order = order_table.readlines()
    order_list = list()

    for line in num1_order:
        line = line.rstrip('\n')
        order = line.split(',')
        order_list.append(order)

    del order_list[0]

    order_list.sort(key=lambda x: (int(x[2]), -int(x[1])))
    order_table.close()

    for i in order_list:
        print(i)
    print('LPT')

    x = 1  # 마지막 머신의 번호를 같이 출력하기 위해 설정한 간단한 변수
    num1 = 0  # 주문 50개의 번호 0부터 시작한다.
    num2 = 0  # 기계번호 총 16개가 있음.
    job_change = 0  # 작업이 바뀌는 횟수를 저장
    Due_date_violation = 0  # 위반하는 작업의 수를 저장
    order_sum = 50  # 총 작업의 수
    machine_sum = 16  # 총 기계의 수
    machine = []  # 배치를 실제 넣어주고 계산해주는 리스트,
    gant_chart = []  # 간트차트의 가시성을 위해 뒤에 주문번호를 붙여서 머신 리스트와 같은 방식

    for i in range(machine_sum):
        machine.append([])
        gant_chart.append([])

    for i in range(16):
        machine[i].append([])

    for i in range(len(order_list)):
        order_list[i][2] = int(order_list[i][2])
        order_list[i][1] = int(order_list[i][1]) // 10

    while num1 < order_sum:
        while num2 < machine_sum:
            len_mc = []
            for i in range(machine_sum):
                len_mc.append(len(machine[i]))

            if machine[num2][-1] == order_list[num1][0] and \
                    order_list[num1][2] + 1 >= order_list[num1][1] + len(machine[num2]):
                for i in range(order_list[num1][1]):
                    machine[num2].append(order_list[num1][0])
                    gant_chart[num2].append(order_list[num1][0] + str(f'{num1:02}'))
                break

            elif machine[num2] == [[]]:
                for i in range(order_list[num1][1]):
                    machine[num2].append(order_list[num1][0])
                    gant_chart[num2].append(order_list[num1][0] + str(f'{num1:02}'))
                break

            elif machine[num2][-1] != order_list[num1][0] and \
                    order_list[num1][2] + 1 >= order_list[num1][1] + len(machine[num2]) and \
                    len(machine[num2]) == min(len_mc):
                job_change += 1
                for i in range(order_list[num1][1]):
                    machine[num2].append(order_list[num1][0])
                    gant_chart[num2].append(order_list[num1][0] + str(f'{num1:02}'))
                break

            elif num2 == 15:
                for i in range(machine_sum):
                    len_mc.append(len(machine[i]))

                y = len_mc.index(min(len_mc))

                if order_list[num1][0] == machine[y][-1] and \
                        order_list[num1][2] + 1 < order_list[num1][1] + len(machine[y]):
                    for i in range(order_list[num1][1]):
                        machine[y].append(order_list[num1][0])
                        gant_chart[y].append('ㅣ' + order_list[num1][0] + str(f'{num1:02}'))
                    Due_date_violation += 1
                    break

                elif order_list[num1][0] != machine[y][-1] and \
                        order_list[num1][2] + 1 < order_list[num1][1] + len(machine[y]):
                    for i in range(order_list[num1][1]):
                        machine[y].append(order_list[num1][0])
                        gant_chart[y].append('ㅣ' + order_list[num1][0] + str(f'{num1:02}'))
                    Due_date_violation += 1
                    job_change += 1
                    break
            else:
                num2 += 1

        num2 = 0
        num1 += 1

    for i in gant_chart:
        print('MC' + str(f'{x:02}'), ':', i)
        x = x + 1

    print('job_change:', job_change)
    print('Due_date_violation:', Due_date_violation)
    print('cost:', Due_date_violation * 10 + job_change * 2)

LPT()






