import os
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoInputSerializer
from pymongo import MongoClient

mongo_uri = "mongodb://" + os.environ["MONGO_HOST"] + ":" + os.environ["MONGO_PORT"]
db = MongoClient(mongo_uri)["test_db"]
todo_collection = db["todo"]


class TodoListView(APIView):
    def get(self, request):
        # Return all todo items from db instance above.
        try:
            todos = list(todo_collection.find())
            for todo in todos:
                todo["_id"] = str(todo["_id"])
                del todo["string_id"]

            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # Accept a todo item in a mongo collection.

        try:
            serializer = TodoInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # save the todo item in the db instance above and save the response in a variable

            response = todo_collection.insert_one(
                {
                    "task": request.data["task"],
                    "completed": False,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            )
            # update the collection with the inserted id
            todo_collection.update_one(
                {"_id": response.inserted_id},
                {"$set": {"string_id": str(response.inserted_id)}},
            )

            # fix Object of type InsertOneResult is not JSON serializable error
            response = {
                "message": "Todo item created successfully",
                "id": str(response.inserted_id),
                "task": request.data["task"],
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete all todo items from db instance above.

        try:
            todo_collection.delete_many({})
            return Response(
                {"message": "Todo items deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TodoItemView(APIView):
    def get(self, request, todo_id):
        # Return a todo item from db instance above.
        try:
            todo = todo_collection.find_one({"string_id": todo_id})
            todo["_id"] = str(todo["_id"])
            del todo["string_id"]
            return Response(todo, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Todo item does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, todo_id):
        # Delete a todo item from db instance above.
        try:
            todo_collection.delete_one({"string_id": todo_id})
            return Response(
                {"message": "Todo item deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, todo_id):
        try:
            todo_collection.update_one(
                {"string_id": todo_id},
                {"$set": request.data, "$currentDate": {"updated_at": True}},
            )
            todo = todo_collection.find_one({"string_id": todo_id})
            todo["_id"] = str(todo["_id"])
            del todo["string_id"]
            return Response(todo, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
