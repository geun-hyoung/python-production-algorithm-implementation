from tkinter import *   # 파이썬 라이브러리 tkinter를 사용해, 사용자가 그래픽을 통하여 컴퓨터와 상호작용할 수 있는 환경을 구현
import math     # 제곱근 계산을 위한 라이브러리

class Market():     # 절차 지향인 파이썬의 단점을 보완하기 위해 객체 class를 사용해서 각 시장들의 정보를 저장

    def __init__(self, x, y, demand, transport_cost):   # 클래스안에 정보를 담기 위해서는 __init__ 함수를 사묭해 원하는 변수들을 저장해준다.
        self.x = x      # 시장 x의 위치
        self.y = y      # 시장 y의 위치
        self.weight_value = demand * transport_cost     # 각 시장의 가중치 = 수요 * 단위 수송비
        market_list.append(self)    # 기본 python에는 db를 따로 연결하지 않는 이상 객체가 초기화 되기 때문에 list안에 객체를 담아서 저장한다.
        print(market_list[0].weight_value)
    
    def get_distance(self, obj):    # 각 객체간의 거리를 class안에 함수로 만들어 계산 거리는 지속적으로 사용되기 때문에 함수를 만들어 추후에 쉽게 사용
        distance = math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)
        return distance

def add_market(screen):     # gui를 통해 객체에 값을 넣어주는 함수를 구성
    global i    # 시장을 추가할때마다 행을 구분해주기 위해서 전역변수인 i를 사용한다. 초기에 시장의 갯수를 입력받아서 그 만큼의 칸을 만들어줘도 되긴한다.

    Label(screen, text = '시장: M{0}'.format(i)).grid(row=i, column = 0, padx=5, pady=5)    # 시장의 이름은 자동적으로 들어온 순서로 Ex) M1부터 지정 들어온 차례로 1번부터 배정한다.

    Label(screen, text="위치(x):").grid(row=i, column=1, padx=5, pady=5)    
    x_entry = Entry(screen, width=5)
    x_entry.grid(row=i, column=2, padx=5, pady=5)

    Label(screen, text="위치(y):").grid(row=i, column=3, padx=5, pady=5)      
    y_entry = Entry(screen, width=5)
    y_entry.grid(row=i, column=4, padx=5, pady=5)

    Label(screen, text="연간수요량(톤):").grid(row=i, column=5, padx=5, pady=5) 
    demang_entry = Entry(screen, width=10)
    demang_entry.grid(row=i, column=6, padx=5, pady=5)

    Label(screen, text="수송운임(달러/톤):").grid(row=i, column=7, padx=5, pady=10)
    trans_entry = Entry(screen, width=10)
    trans_entry.grid(row=i, column=8, padx=5, pady=5)

    Button(screen, text="저장", command=lambda: Market(
        int(x_entry.get()), int(y_entry.get()), int(demang_entry.get()), int(trans_entry.get()))).grid(row=i, column=9, padx=5, pady=5)    # 값을 입력한 후 객체에 저장하기 위한 활성화 버튼 눌러줘야 저장된다.

    i += 1

def muti_heuristic(fix_entry, stock_entry, scale_entry, market_list):   # 알고리즘 복수물류입지 휴리스틱 적용 부분   
    global i    # gui를 구성시 행을 구분을 위해 전역변수 global를 사용 

    fix_cost = float(fix_entry.get())       # 사전에 입력받은 고정비                                               
    stock_cost = float(stock_entry.get())       # 사전에 입력받은 재고관리비                                                 
    K = float(scale_entry.get())        # 사전에 입력받은 축척치  
                         
    return_list = []     # n = 1부터 n = N 까지 각각의 갯수마다 최적의 비용 지점을 저장
    sort_market = sorted(market_list, key = lambda x: -x.weight_value)      # sorted를 사용한 이유는 원본은 유지, 객체들의 가중치를 기준으로 높은 순으로 정렬해서 입지를 선정할 때 시장으로 선점하기 위해

    n = 1       # 입지가 1일 때부터

    while n <= len(market_list) :       # 입지가 N개 일때 까지 경우의 수를 확인 

        from_market = sort_market[:n]       # n개의 물류센터 입지 선정된 시장 들 n 갯수에 따라                                                                     
        to_market = sort_market[n:]         # 물류센터로 선정되지 않은 시장들                        
        from_to = []       # 물류센터 선정 그룹과 그렇지 않은 그룹의 수송 흐름과 비용을 저장할 리스트

        if n == 1:      # n = 1
            cost = 0    # 비용
            select_index = market_list.index(sort_market[0])    # 가중치가 가장 높은 시장이기 때문에 단일 입지에서는 물류센터 입지로 선정 

            for to in to_market:        # 시장 별로 물류센터입지와 거리와 가중치와 축척치를 곱해서 각 시장별 비용
                cost += market_list[select_index].get_distance(to) * to.weight_value * K    # 비용을 순차적으로 
                from_to.append([select_index+1, market_list.index(to)+1, cost])    # 각 흐름에 따른 비용을 계산, index 이기 때문에 시장 번호를 저장하기 위해 + 1, 위에서는 1부터 이름을 지정해서
                
            sum = cost + fix_cost + stock_cost      # 총 비용 계산
            return_list.append([n, select_index + 1, from_to, cost, fix_cost, stock_cost, sum])         # 위에서 선언했던 리스트에 시장과 흐름과 수송비, 고정, 재고 비용

        else:       # n = 2
            from_list = []
            for fr in from_market:      # 물류센터로 선정된 그룹에서 
                cost = 0
                from_list.append(market_list.index(fr)+1)   # 입지로 선정된 그룹 이름을 저장하기 위해 index + 1

                for to in to_market:    # 입지로 선정되지 않은 그룹
                    cost = fr.get_distance(to) * to.weight_value * K        # 흐름별 수송비를 전체 구하고
                    from_to.append([market_list.index(fr)+1, market_list.index(to)+1, cost])        # 리스트에 담아준다. 즉 전체 수송비들을 저장해서 비교해주기 위해

            from_to.sort(key = lambda x: x[2])       # 각 흐름별 비용을 수송비가 적은순으로 정렬                                                        
            check_list = []      # 입지로 선정되지 않는 그룹 중 중복을 방지하기 위한 확인 리스트                                                                    
            flow = []       # 시장이 n개 일떄 실제 최종 흐름이 이루어지는 과정을 담기 위한 리스트                                                                   
                                                                                   
            total_cost = 0      # 총비용
                                            
            for x in from_to:      # 수송비가 적은 순으로 반복문을 시행해 입지와 연결해준다.                                                                  
                if x[1] in check_list:      # 만약 to_market이 어떤 물류센터로 갈지 정했다면 패스해준다 .
                    pass
                else:       # 정해지지 않았다면                                                
                    check_list.append(x[1])     # 확인을 하기 위해 리스트에 담아준다.                                                             
                    flow.append([x[0], x[1], 'M' + str(x[0]) + '->' + 'M' + str(x[1])])     # 실제 흐름을 저장해 결과값을 확인하기 위함 .                                                     
                    total_cost += x[2]       # 각 흐름별 수송비를 더 해준다.                                                                

                    if len(check_list) == len(to_market):       # 만약 어떤 물류센터로 이동할지 다 연결되었다면 반복문을 종료.                                               
                        break            

            flow.sort(key = lambda x: x[0])  # 이름순으로 정렬, m1, m2 이런식으로 ...
            from_list.sort()         # 입지로 선정된 시장들을 이름으로 정렬
            sum = total_cost + fix_cost * n + stock_cost * math.sqrt(n)            # 총 비용                                
            return_list.append([n, from_list, flow, total_cost, fix_cost * n, stock_cost * math.sqrt(n), sum])        # 입지 갯수에 따른 입지로 선정된 시장, 흐름, 수송비, 고정, 재고 비용

        if n == len(market_list):       # 만약 n = N 이면 최종 입지로 선정된 결과값을 보여주고 반복문을 종료한다. 
            return_list.sort(key = lambda x : x[6])     # 최종 리스트에서 총 비용을 기준으로 정렬해주고 

            Label(screen, text = '최적해').grid(row = i + 2, column = 0, padx=5, pady=5)    
            Label(screen, text = 'n : {0}'.format(str(return_list[0][0]))).grid(row = i + 2, column = 1, padx=5, pady=5)      #최적해 입지의 수
                         
            k = 0
            for s in return_list[0][1]:
                Label(screen, text = '물류센터 선정 입지 : M{0}'.format(str(s))).grid(row = i + k + 2, column = 2, padx=5, pady=5) # 물류센터로 선정된 입지들을 보여준다.
                k += 1

            m = 0
            for obj in return_list[0][2]:       # 입지로 선정된 시장과 아닌 시장과의 흐름, 자기 자신으로 흐름이 있는것은 제외 
                Label(screen, text = '흐름 : {0}'.format(str(obj[2]))).grid(row = i + m + 2 , column = 3, padx=10, pady=5)  # 입지로 선정된 그룹과 그에 따른 시장 흐름
                m += 1  

            Label(screen, text = '수송비 : {0}'.format(int(return_list[0][3]))).grid(row = i + 2, column = 4, padx=10, pady=5)      # 최적해의 수송비
            Label(screen, text = '고정비 : {0}'.format(int(return_list[0][4]))).grid(row = i + 2, column = 5, padx=10, pady=5)      # 최적해의 고정비
            Label(screen, text = '재고유지비 : {0}'.format(int(return_list[0][5]))).grid(row = i + 2, column = 6, padx=10, pady=5)      # 최적해의 재고유지비
            Label(screen, text = '총비용 : {0}'.format(int(return_list[0][6]))).grid(row = i + 2, column = 7, padx=10, pady=5)      # 최적해의 총비용
            print(market_list)
            break

        n += 1
                                    
screen = Tk()       # tkinter의 Tk 함수를 screen 이라는 변수에 저장해서 사용
screen.title("복수물류설비입지 휴리스틱")       # 화면 구성 부분    
screen.geometry("1200x500")
screen.resizable(True, True)    # 화면의 크기를 조정가능하게 해준다.

Label(screen, text = '연간고정비 : ').grid(row = 0, column = 0, padx=10, pady=5)
Label(screen, text = '연간재고관리비 : ').grid(row = 0, column = 2, padx=5, pady=5)
Label(screen, text = '축적치 : ').grid(row = 0, column = 4, padx=5, pady=10)

fix_entry = Entry(screen, width = 10)
fix_entry.grid(row = 0, column = 1, padx=10, pady=10)

stock_entry = Entry(screen, width = 10)
stock_entry.grid(row = 0, column = 3, padx=5, pady=10)

scale_entry = Entry(screen, width = 5)
scale_entry.grid(row = 0, column = 5, padx=5, pady=10)

i = 1
market_list = []

Button(screen, text="새로운 시장 추가", command=lambda: add_market(screen)).grid(row = 0, column = 6, padx=5, pady=5)   # 새로운 시장을 추가하는 버튼   
Button(screen, text="실행", command=lambda: muti_heuristic(fix_entry, stock_entry, scale_entry, market_list)).grid(row=0, column=8, padx=5, pady=10)    # 모든 정보를 입력한 후 누르며 최적해가 나온다.

screen.mainloop()       # tkinter를 실행


        




