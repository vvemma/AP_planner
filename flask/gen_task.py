import datetime
import random
import csv

#이값을 바꿈
random.seed(120)

start_date = datetime.date(2024, 6, 20)
end_date = datetime.date(2024, 7, 30)
delta = datetime.timedelta(days=1)
test_day=[]
while (start_date < end_date):
    c_day = start_date.strftime("%Y-%m-%d")
    start_date += delta
    test_day.append(start_date)
test_class = ["고급수학", "경제","AP미적분", "AP물리", "AP화학", "AP생명과학", "AP지구과학","AP프로그래밍","독서","영어"]
test_priority = [1,2,3]

# num_task = random.randint(1,10)
for case_id in range(6,31):
    # f = open(file_name, 'w',encoding='utf-8')
    num_task = random.randint(1,len(test_class))
    # num_task = len(test_class)
    # cls = test_class
    tasks = []
    for idx in range(num_task):
        cls = random.choice(test_class)
        items = test_day[:-2]
        s_date = random.choice(items)
        s_index = test_day.index(s_date)
        items = test_day[s_index+1:]
        e_date = random.choice(items)
        e_index = test_day.index(e_date)
        hours = random.randint(5,min(20,5*(e_index-s_index)))
        pri = random.choice(test_priority)
        task = [cls,s_date,e_date,hours,pri]
        tasks.append(task)
    
    #파일 저장 위치 지정
    file_name = "flask/test_case"+str(case_id)+"_csv.csv"
    with open(file_name, 'w', encoding='utf-8',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tasks)
    


