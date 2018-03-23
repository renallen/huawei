
# coding=utf-8
def predict_vm(ecs_lines, input_lines):
    # Do your work from here#)
    size_list1 = ["flavor15", "flavor14", "flavor13", "flavor12", "flavor11", "flavor10", "flavor9", "flavor8",
                 "flavor7","flavor6", "flavor5", "flavor4", "flavor3", "flavor2", "flavor1"
                 ]
    size_list2 = ["flavor15", "flavor14", "flavor12", "flavor13", "flavor11", "flavor9", "flavor10", "flavor8",
                  "flavor6", "flavor7", "flavor5", "flavor3", "flavor4", "flavor2", "flavor1"
                  ]
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    CPU, MEM, VM_number, flavors_r, flavors_size, test_type, start_time, stop_time=get_input(input_lines)
    # print(flavors)
    flavors = []
    if test_type == "CPU":
        size_list=size_list1[::-1]
    else:
        size_list = size_list2[::-1]
    for flavor in size_list:
        if flavor in flavors_r:
            flavors.append(flavor)
        else:
            pass
    times, ys = get_data(ecs_lines)
    fla_number=[]
    m=get_time(start_time, stop_time)
    # w = [0.3, 0.2, 0.2, 0.12, 0.08, 0.08, 0.08, 0.06, 0.05, 0.03, 0.028, 0.027, 0.022, 0.017]  # 87.79
    # w =[0.3, 0.25, 0.2, 0.15, 0.1, 0.09, 0.08, 0.07, 0.05, 0.04, 0.03, 0.03, 0.02, 0.017]  # 86498
    w = [0.3, 0.2, 0.2, 0.12, 0.08, 0.08, 0.08, 0.06, 0.05, 0.03, 0.028, 0.027, 0.022, 0.017]  # 87.79
    for flavor in flavors:
        data=ys[flavor]
        fla_number.append(predict_data(times, data,w,2,5, m))
    VM_total=sum(fla_number)
    result.append(str(int(VM_total)))
    #print CPU, MEM, VM_number, flavors, flavor_CPU, flavor_MEM, test_type, start_time, stop_time
    for i in range(VM_number):
        result.append(flavors[i]+" "+str(int(fla_number[i])))
    result.append('')



    if test_type == "CPU":
        r1=CPU
        r2=MEM
    else:
        r1=MEM
        r2=CPU
    l=assign_VM(r1,r2,flavors,flavors_size,fla_number)
    H=len(l)

    result.append(str(H))
    for i in range(H):
        result.append(str(i+1))
        for items in l[i].keys():
            result[-1]=result[-1]+" "+items+" "+str(l[i][items])

    return result


def get_input(input_lines):
    VM_number=0
    flavors=[]
    flavor_CPU=[]
    flavor_MEM = []
    CPU=0
    MEM=0
    test_type, start_time, stop_time=[],[],[]
    for index in range(len(input_lines)):
        if index ==0:
            CPU,MEM=int(input_lines[index].split(" ")[0]),int(input_lines[index].split(" ")[1])
        elif index==2:
            VM_number=int(input_lines[index].split(" ")[0])
        elif index>2 and 2+VM_number>=index:
            flavors.append(input_lines[index].split(" ")[0])
            flavor_CPU.append(int(input_lines[index].split(" ")[1]))
            flavor_MEM.append(int(int(input_lines[index].split(" ")[2])/1024))
        elif index== 4+VM_number:
            test_type=input_lines[index].split("\n")[0]
        elif index== 6+VM_number:
            start_time=input_lines[index].split(" ")[0]
        elif index== 7+VM_number:
            stop_time=input_lines[index].split(" ")[0]
        else: pass
    flavors_size={}
    if test_type[0]=="CPU":
        for i in range(VM_number):
            flavors_size[flavors[i]]=(flavor_CPU[i],flavor_MEM[i])
    else:
        for i in range(VM_number):
            flavors_size[flavors[i]]=(flavor_MEM[i],flavor_CPU[i])
    return CPU,MEM,VM_number,flavors,flavors_size,test_type[0],start_time,stop_time


## get the input data
def get_data(ecs_lines):
    DICT = {}
    flavors = ["flavor15","flavor14","flavor13","flavor12","flavor11","flavor10","flavor9",
               "flavor8", "flavor7", "flavor6", "flavor5", "flavor4", "flavor3", "flavor2","flavor1"
               ]
    times = []
    for item in ecs_lines:
        values = item.split("\t")
        flavorName = values[1]
        createTime = values[2].split(" ")[0]
        if (flavorName not in DICT):
            DICT[flavorName] = {}
            DICT[flavorName][createTime] = 1
        else:
            if (createTime not in DICT[flavorName].keys()):
                DICT[flavorName][createTime] = 1
            else:
                DICT[flavorName][createTime] = DICT[flavorName][createTime] + 1
        if createTime not in times:
            times.append(createTime)
        else:
            pass

    ys = {}
    for flavorName in flavors:
        y = []
        y_sum=0
        for time in times:
            if time not in DICT[flavorName].keys():
                y.append(y_sum)
            else:
                y_sum=y_sum+DICT[flavorName][time]
                y.append(y_sum)
                # y.append(DICT[flavorName][time])

        ys[flavorName] = y

    return times,ys


## a simple method to predict the future data, input the old times data, w is the weight of linear factor,
#  k is the slide filter , n is the number between two data , m is the predict days length ，output the predict data
## times是历史数据的时间
## data是历史数据的关于时间的累加和
## w增量的权重，
## n代表n个数一个做一个差分，也就是n个数的之间增量*w
## k是我做的对数据的滑动滤波
## m是从输入文件中读取的预测时间天数
## 输出最终预测的结果
def predict_data(times,data,w,n=5,k=5,m=7):
    tmp=[]
    for i in range(len(times)):
        if i<k-1:
            tmp.append(data[i])
        else:
            tmp.append(sum(data[i-k+1:i+1])/k)

    for t in range(m):
        data_sum = 0
        for i in range(len(w)):
            # for j in range(n):
            #     if j==n-1:
            data_sum=data_sum+w[i]*(tmp[-1-n*i]-tmp[-n-n*i])
        tmp.append(data_sum+tmp[-n+1])

    return round(tmp[-1]-tmp[-m])

##get the predict times length
#input start_time and stop_time, output length
def get_time( start_time, stop_time):
    start=start_time.split('-')
    stop = stop_time.split('-')
    month_day=0
    if int(stop[2])<int(start[2]):
        if  start[1] in ["01","03","05","07","08","10","12"]:
            month_day=31
        elif start[1] in ["02"]:
            if (int(start[0])%4==0 and int(start[0])%100!=0) or (int(start[0])%100==0 and int(start[0])%400==0):
                month_day=29
            else:
                month_day = 28
        else:
            month_day = 30
    else:
        pass
    return  month_day+int(stop[2]) - int(start[2])


# assign VM to computer
## input the first assigned type: CPU or MEM
#the list of predict flavors and their size and their number
#output the result of assignation a list of dict
def assign_VM(r1,r2,flavors,flavors_size,fla_number):
    R1 = [r1]
    l = [{}]
    k = 0
    R2 = [r2]
    for j in fla_number:
        # print(j)
        z = 0
        if j == 0:
            pass
        else:
            for i in range(int(j)):

                for r in range(len(R1)):
                    if R1[r] >= flavors_size[flavors[k]][0] and R2[r] >= flavors_size[flavors[k]][
                        1] and r <= len(R1) - 1:
                        R1[r] = R1[r] - flavors_size[flavors[k]][0]
                        z = z + 1
                        l[r][flavors[k]] = z
                        R2[r] = R2[r] - flavors_size[flavors[k]][1]
                        break
                    elif (R1[r] < flavors_size[flavors[k]][0] or R2[r] < flavors_size[flavors[k]][1]) and len(
                            R1) == r + 1:
                        R1.append(r1 - flavors_size[flavors[k]][0])
                        l.append({flavors[k]: 1})
                        z = 1
                        R2.append(r2 - flavors_size[flavors[k]][1])
                        break
                    else:
                        pass

        k = k + 1
    return l