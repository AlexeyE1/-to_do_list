from django.conf import settings


class ToDoList:
    def __init__(self, request):
        self.session = request.session
        list = self.session.get(settings.TASKS_SESSION_ID)
        if not list:
            list = self.session.get(settings.TASKS_SESSION_ID) = {}
        self.list = list
    

    def add(self, task):
        task_id = str(task.id)
        if task_id not in self.list:
            self.list[task_id] = {}
        self.save()
    

    def save(self):
        self.session[settings.TASKS_SESSION_ID] = self.cart
        self.session.modified = True
    

    def remove(self, task):
        task_id = str(task.id)
        if task_id in self.list:
            del self.list[task_id]
            self.save()
    

    def change_status(self, task):
        if task.completed:
            task.completed = 0
        else:
            task.completed = 1


    def clear(self):
        del self.list[settings.TASKS_SESSION_ID]
        self.session.modified = True