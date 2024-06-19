import task_schedule
from task_schedule import PRIORITY
from task_schedule import check_schedule, sort_schedule,init_assign_table,print_dic, print_assign_table
from task_schedule import check_task_add, do_assign_table, find_assigned_task,assign_table,replace_task,assign_main
import csv

from flask import Flask, jsonify
from prettytable import PrettyTable
import os.path




app = Flask(__name__)
all_schedule = [None for _ in range(50)]

@app.route('/')
@app.route('/home')
def home():
    return 'Hello, 인곽!'

@app.route('/<case_id>')
def app_assign_main(case_id):
    id = int(case_id)
    #case1의 list index는 0
    id = id -1
    print(id)
    print(all_schedule[id])
    assign_table, assigned, non_assign=assign_main(all_schedule[id])
    #여기가 보내는 코드
    return jsonify({
        "assigned_tasks": assigned,
        "unassigned_tasks": non_assign,
        "assign_table": assign_table
    })


if __name__ == "__main__":  
    #여기는 파일을 case를 읽어오는 부분이라서 꼭 있어야 함
    for id in range(1,30+1):
        file_name = "flask/test_case"+str(id)+"_csv.csv"
        if not os.path.isfile(file_name):
            break 
        f = open(file_name, 'r',encoding='utf-8')
        rdr = csv.reader(f)
        tasks=[]
        for line in rdr:
            task = line
            task[3] = int(task[3])
            task[4] = int(task[4])
            tasks.append(task)
        f.close()
        all_schedule[id-1]=tasks


    # 여기서 부터 69까지는 결과를 미리 확인해보는 부분임.. 한번 돌려보고 되면 최종은 주석으로 하고 돌리기
    table = PrettyTable()
    table.field_names = ['Case','과목', '시작일', '종료일', '할당시간','중요도',"할당여부"]
    for id in range(1,30+1):
        tasks=all_schedule[id-1]
        if tasks is not None:    
            assign_table, assigned, non_assign=assign_main(tasks)
            for task in tasks:
                if task[0] in assigned:
                    result = "성공"
                else:
                    result = "실패"
                table.add_row([str(id),task[0], task[1], task[2],task[3],task[4],result])
                
            print("Case:",id,"="*20)    
            print_assign_table(assign_table)
    print(table)

    # Flask  구동할때 필요함
    app.run(debug=True)





