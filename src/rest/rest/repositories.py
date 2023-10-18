from datetime import datetime
from .models import TodoItem
from pymongo import MongoClient


class TodoRepository:
    # Initialize the TodoRepository class with a mongo_uri and db_name
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.todo_collection = self.db["todo"]

    # Method: Get all todo items
    def get_all_todos(self, exclude_fields=[]):
        todos = list(self.todo_collection.find())
        return [
            TodoItem(**todo).serialized_data(exclude=exclude_fields) for todo in todos
        ]

    # Method: Get a todo item by id
    def get_todo_by_id(self, todo_id, exclude_fields=[]):
        todo = self.todo_collection.find_one({"string_id": todo_id})
        return TodoItem(**todo).serialized_data(exclude=exclude_fields)

    # Method: Create a todo item
    def create_todo(self, **kwargs):
        todo_data = TodoItem(**kwargs).serialized_data(exclude=["_id"])
        result = self.todo_collection.insert_one(todo_data)

        # Introduce string_id field to identify todo items as _id is an ObjectId
        self.todo_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"string_id": str(result.inserted_id)}},
        )
        return str(result.inserted_id)

    # Method: Update a todo item by id
    def update_todo(self, todo_id, **kwargs):
        update_fields = {}
        todo_collection_fields = list(TodoItem.__annotations__.keys())
        for key, value in kwargs.items():
            if key in todo_collection_fields:
                update_fields[key] = value
        update_fields["updated_at"] = datetime.now()

        if update_fields:
            self.todo_collection.update_one(
                {"string_id": todo_id}, {"$set": update_fields}
            )

    # Method: Delete a todo item by id
    def delete_todo_by_id(self, todo_id):
        self.todo_collection.delete_one({"string_id": todo_id})

    # Method: Delete all todo items
    def delete_all_todos(self):
        self.todo_collection.delete_many({})
