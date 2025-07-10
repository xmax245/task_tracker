import argparse
import json
import os.path
import datetime

def readjson(add: bool = False) -> list:
    try:
        if os.path.exists('tasks.json'):
            with open('tasks.json') as f:
                data = json.load(f)
                if type(data) == list:
                    return data
                else:
                    return []
        elif add == True:
            return []
        else:
            raise Exception('json file error')
    except:
        print("Tasks list dosent exist please use add to create new list or delete broken tasks.json file")
        exit()
        
def savejson(data: list):
    with open('tasks.json','w+') as f:
        json.dump(data,f,indent="")

def statuscheck(status: str) -> str:
    if status == "in-progress" or status == "i":
        status = "in-progress"
    elif status == "done" or status == "d":
        status = "done"
    elif status == "todo" or status == "t":
        status = "todo"
    else:
        raise Exception('Error : incorrect status')
    return status  
    
def findid(data: list,id: int) -> int:
    y = 0
    for x in data:
        if x['id'] == id:
            return y
        else:
            y +=1
    print('Wrong task ID')
    raise Exception('no id in list')
    
def task_add(task: str):
    data = readjson(True)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = len(data)+1    
    try:
        data.append({'id':id,'desc':task,'status':'todo','create':time,'updated':time})
        print('Task added successfully (ID: '+str(id)+')')
    except:
        print('Failed to add a task check your input')
    savejson(data)
    
def task_update(id: int,task: str):
    data = readjson()
    try:
        data[findid(data,id)].update({'desc':task,'updated':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        print('Task updated successfully (ID: '+str(id)+')')
    except:
        print('Failed to update a task check your input')
    savejson(data)
    
    
def task_delete(id: int):
    data = readjson()
    try:
        data.pop(findid(data,id))
        print('Task deleted successfully (ID: '+str(id)+')')
    except:
        print('Failed to delete a task check your input')
    savejson(data)

def task_mark(id: int,status: str):
    data = readjson()
    try:
        data[findid(data,id)].update({'status':statuscheck(status),'updated':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        print('Task marked successfully (ID: '+str(id)+')')
    except:
        print('Failed to mark a task check your input')
        
    savejson(data)
    

def task_list(status: str):
    data = readjson()
    try:
        status=statuscheck(status)
    except:
        print('Failed to list a task check your input')
        return
    print('ID Description Status Create-date Update-date')
    for x in data:
        if status != None and status != x['status']:
            continue
        else:
            print('{0} {1} {2} {3} {4}'.format(x['id'],x['desc'],x['status'],x['create'],x['updated']))
    
    

def cli_entry_point():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    parser_add = subparsers.add_parser('add',help='Add new task to a list')
    parser_add.add_argument('task',type=str,help='task description in "" example: "Cook dinner"')
    
    parser_update = subparsers.add_parser('update',help='Update existing task description in a list')
    parser_update.add_argument('id',type=int,help='task id "" example: 1')
    parser_update.add_argument('task',type=str,help='task description in "" example: "Cook dinner"')
    
    parser_delete = subparsers.add_parser('delete',help='Delete an existing task from a list')
    parser_delete.add_argument('id',type=int,help='task id "" example: 1')
    
    parser_mark = subparsers.add_parser('mark',help='Change existing task status in a list')
    parser_mark.add_argument('id',type=int,help='task id "" example: 1')
    parser_mark.add_argument('status',type=str,help='task status  example: done | in-progress ,default: todo')
    
    parser_list = subparsers.add_parser('list',help='lists all tasks or by task status from a list example: done | todo | in-progress')
    parser_list.add_argument('status',type=str,nargs='?',default=None)
    
    
    args = parser.parse_args()
    
    if args.command == 'add':
        task_add(args.task)
    elif args.command == 'update':
        task_update(args.id,args.task)
    elif args.command == 'delete':
        task_delete(args.id)
    elif args.command == 'mark':
        task_mark(args.id,args.status)
    elif args.command == 'list':
        task_list(args.status)
    else:
        parser.print_help()