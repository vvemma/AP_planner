import datetime
PRIORITY ={"PRIORITY1":1,"PRIORITY2":2,"PRIORITY2":3}
from prettytable import PrettyTable

assign_table ={}
day_capacity = 5
today = datetime.date.today().day
now = datetime.datetime.now()
days = 30

def print_dic(dic):
    for k,v in dic.items():
        if len(v)>0:
            print(k,'\t',v)
def print_assign_table(assign_table):
    table = PrettyTable()
    field_names = ['날짜']
    for i in range(day_capacity):
        field_names.append('할당'+str(i+1))

    table.field_names = field_names
    for k,v in assign_table.items():
        add_row = [k]
        assigned = False
        for i in range(day_capacity):
            if i<len(v):
                assigned = True
                add_row.append(v[i])
            else:
                add_row.append("")
        if assigned:
            table.add_row(add_row)
    print(table)

def day_diff(start_day,end_day):
    end_day = end_day.split("-",3)
    start_day = start_day.split("-",3)
    d0 = datetime.date(int(start_day[0]),int(start_day[1]),int(start_day[2]))
    d1 = datetime.date(int(end_day[0]),int(end_day[1]),int(end_day[2]))
    delta = d1 - d0
    return delta.days

def day_conflict_task(target_task,tasks):
    task1_start = target_task[1]
    task1_end = target_task[2]

    dic = {}

    for task in tasks:
        if target_task[0]==task[0]:
            continue
        task2_start = task[1]
        task2_end = task[2]
        start_diff = day_diff(task1_start,task2_start)
        end_diff = day_diff(task1_end,task2_end)

        if day_diff(task1_start,task2_end)<=0:
            dic.update({task[0]:0})
        elif day_diff(task1_end,task2_start)>=0:
            dic.update({task[0]:0})
        else:
            if start_diff>0:
                conflict_start = task2_start
            else:
                conflict_start = task1_start
            if end_diff>0:
                conflict_end = task1_end
            else:
                conflict_end = task2_end

            dic.update({task[0]:day_diff(conflict_start,conflict_end)})
    return dic

def sort_schedule(tasks,method=0):
    
    #0 criteria: higher load
    if method==0:
        tasks = sorted(tasks,key=lambda x: -x[3])
    #1 criteria: 1 less duration, 2: earlier start_day
    elif method==0:
        tasks = sorted(tasks,key=lambda x:(day_diff(x[1],x[2]),x[2]))
    #2 criteria: higher priority
    else:
        tasks = sorted(tasks,key=lambda x: -x[4])
    return tasks

def acc_empty_hours(assign_table):
    #accumulative empty hour by day
    sorted_keys = sorted(assign_table.keys())
    avail={}
    for k in range(len(sorted_keys)):
        sum=0
        for h in range(k,len(sorted_keys)):
            hour = day_capacity - len(assign_table[sorted_keys[h]])
        sum + hour
    avail.update({sorted_keys[k]:sum})

    return avail
def find_assigned_task(assign_table,tasks):
    all_tasks = []
    for task in tasks:
        all_tasks.append(task[0])
    assigned_task = set()
    for k,v in assign_table.items():
        temp = set(v)
        assigned_task = temp|assigned_task
    not_assigned_task = set(all_tasks)-assigned_task
    
    return list(assigned_task),list(not_assigned_task)

def find_avail_hour(assign_table,start_day,end_day):
    keys = list(assign_table.keys())
    start_index = keys.index(start_day)
    end_index = keys.index(end_day)

    hours = 0

    for index in range(start_index,end_index):
        current_index = keys[index]
        hours +=day_capacity-len(assign_table[current_index])
    
    return hours

def check_task_add(assign_table,task):
    start_day = task[1]
    end_day = task[2]
    work_hour = task[3]
    task_name = task[0]
    total_avail_hours = find_avail_hour(assign_table,start_day,end_day)
    return total_avail_hours - work_hour

def do_assign_table(assign_table,from_date,task,rule):
    start_day = task[1]
    end_day = task[2]
    work_hour = task[3]
    task_name = task[0]

    keys = list(assign_table.keys())
    from_index = keys.index(from_date)
    start_index = max(keys.index(start_day),from_index)
    end_index = keys.index(end_day)

    if rule==0:
        index = start_index
        while work_hour>0:
            if index<end_index:
                current_key = keys[index]
                left_load = day_capacity - len(assign_table[current_key])
                if left_load>0:
                    assign_table[current_key].append(task_name)
                    work_hour -=1
                index +=1
            else:
                index = start_index
            
    elif rule==1:
        index = start_index
        while work_hour>0:
            current_key=keys[index]
            left_load = day_capacity-len(assign_table[current_key])
            if left_load>0:
                if work_hour>left_load:
                    assign_table[current_key].extend([task_name]*left_load)
                    work_hour -=left_load
                else:
                    assign_table[current_key].extend([task_name]*work_hour)
                    work_hour -= work_hour
            index +=1
    elif rule==2:
        index= end_index -1
        while work_hour>0:
            if index>=start_index:
                current_key=keys[index]
                left_load = day_capacity-len(assign_table[current_key])
                if left_load>0:
                    assign_table[current_key].append(task_name)
                    work_hour -=1
                index -=1
            else:
                index = end_index-1
    else:
        index = end_index -1
        while work_hour>0:
            current_key=keys[index]
            left_load = day_capacity-len(assign_table[current_key])
            if left_load>0:
                if work_hour>left_load:
                    assign_table[current_key].extend([task_name]*left_load)
                    work_hour -=left_load
                else:
                    assign_table[current_key].extend([task_name]*work_hour)
                    work_hour -=work_hour
            index -=1
    
    return assign_table

def remove_task(assign_table,task_name):
    for k,v in assign_table.items():
        list_ = [value for value in v if value!=task_name]
        assign_table[k]=list_
    return assign_table

def conflict_task(assign_table,target_task,tasks):
    task_name = target_task[0]
    start_day = target_task[1]
    end_day = target_task[2]

    keys = list(assign_table.keys())
    start_index = keys.index(start_day)
    end_index = keys.index(end_day)
    mySet = set()
    
    for index in range(start_index,end_index):
        key=keys[index]
        temp = set(assign_table[key])
        mySet = mySet|temp
    mylist = list(mySet)

    conflict_task = []

    for task in tasks:
        if task[0] in mylist:
            conflict_task.append(task)
    return conflict_task

def replace_task(assign_table,new_task,tasks,rule):
    org_assign_table = assign_table
    success_replace = []

    target_tasks = conflict_task(assign_table,new_task,tasks)

    for task in target_tasks:
        assign_table = remove_task(assign_table,task[0])
    
    check = check_task_add(assign_table,new_task)

    if check<0:
        assign_table = org_assign_table
    else:
        assign_table = do_assign_table(assign_table,new_task[1],new_task,rule)
        sort_target_tasks = target_tasks
        for task in sort_target_tasks:
            check = check_task_add(assign_table,task)
            if check>=0:
                assign_table = do_assign_table(assign_table,task[1],task,rule)
                success_replace.append(task[0])

    return assign_table,success_replace

# Find task which load is more than day-capacity
def check_schedule(schedule):
    value=[]
    for task in schedule:
        end_day=task[2]
        start_day=task[1]
        diff=day_diff(start_day,end_day)
        hours=task[3]
        max_hours = diff*day_capacity
        if hours>max_hours:
            value.append(task[0])
    return value

def init_done_table(assign_table):
    if not assign_table:
        return False
    
    for value in assign_table.values():
        if value:
            return True
    return False

def init_assign_table(assign_table):
    start_date = datetime.date(2024, 6, 1)
    end_date = datetime.date(2024, 7, 31)
    delta = datetime.timedelta(days=1)
    while (start_date <= end_date):
        c_day = start_date.strftime("%Y-%m-%d")
        start_date += delta
        assign_table[c_day]=[]


    # for day in range(days):
    #     c_day = (now+datetime.timedelta(days=day))
    #     c_day = c_day.strftime("%Y-%m-%d")
    #     assign_table[c_day]=[]
    # print("--"*10)
    # print_dic(assign_table)
    return assign_table
    

def assign_main(test_case):
    assigned = []
    not_assigned = [] 
    

    check = check_schedule(test_case)
    global assign_table
    # print(test_case)
    # print_dic(assign_table)

    if len(check)>0:
        assign_table = init_assign_table(assign_table)
        return assign_table, assigned, not_assigned    
    else:
        # if not init_done_table:
        if not init_done_table:
            assign_table = init_assign_table(assign_table)
        # print_dic(assign_table)
           
        best_method = -1
        best_rule = -1
        max_task = 0
        task_list = []
        for method in range(3):
            s_schedule = sort_schedule(test_case,method)
            check = check_schedule(test_case)
            if len(check)>0:
                print("schedule has problem",check)
                break
            else:
                for rule in range(4):
                    assign_table = init_assign_table(assign_table)
                    for task in s_schedule:
                        check = check_task_add(assign_table,task)
                        if check>=0:
                            from_date = now.strftime("%Y-%m-%d")
                            assign_table=do_assign_table(assign_table,from_date,task,rule)
                            
                            # print(method,rule)
                            # print_dic(assign_table)
                            # ch = input()

                        
                    assigned,not_assigned = find_assigned_task(assign_table,s_schedule)

                    # print(method,rule,find_assigned_task(assign_table,s_schedule))
                    # print_dic(assign_table)
                    if len(assigned)>0:
                        if len(assigned)>max_task:
                            best_method = method
                            best_rule = rule
                            max_task = len(assigned)

        

        if best_method!=-1 and best_rule !=-1:
            assign_table = init_assign_table(assign_table)
            s_schedule = sort_schedule(test_case,best_method)
            # print("++"*10)
            # print(best_method,best_rule)
            # print_dic(assign_table)
            # print(s_schedule)
            for task in s_schedule:
                check =  check_task_add(assign_table,task)
                if check>=0:
                    from_date = now.strftime("%Y-%m-%d")
                    assign_table = do_assign_table(assign_table,from_date,task,best_rule)
                    #  print(task)
                    #  print_dic(assign_table)
                    
        else:
            assign_table = init_assign_table(assign_table)
            s_schedule = sort_schedule(test_case,0)
            from_date = now.strftime("%Y-%m-%d")
            # print("---"*10)
            # print_dic(assign_table)
            # print(task)
            assign_table = do_assign_table(assign_table,from_date,task,0)

        assigned,not_assigned = find_assigned_task(assign_table,s_schedule)
        return assign_table, assigned, not_assigned 
        


        # print(a,b)
        # print(best_method,best_rule)
        # print_dic(assign_table)

        # assign_table,success = replace_task(assign_table,task_new,s_schedule,best_rule)
        # a,b = find_assigned_task(assign_table,s_schedule)
        # print(a,b)
        # print_dic(assign_table)





