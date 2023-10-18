import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TodoInputSerializer
from .repositories import TodoRepository

mongo_uri = "mongodb://" + os.environ["MONGO_HOST"] + ":" + os.environ["MONGO_PORT"]
db_name = "test_db"
todo_repository = TodoRepository(mongo_uri, db_name)


class TodoListView(APIView):
    # Return all todo items.
    def get(self, request):
        try:
            todos = todo_repository.get_all_todos(exclude_fields=["string_id"])
            return Response(todos, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Create a todo item.
    def post(self, request):
        try:
            serializer = TodoInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            todo_id = todo_repository.create_todo(**serializer.validated_data)
            todo = todo_repository.get_todo_by_id(todo_id, exclude_fields=["string_id"])
            response = {
                "message": "Todo item created successfully",
                "data": todo,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Delete all todo items.
    def delete(self, request):
        try:
            todo_repository.delete_all_todos()
            return Response(
                {"message": "Todo items deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TodoItemView(APIView):
    # Return a todo item by id.
    def get(self, request, todo_id):
        try:
            todo = todo_repository.get_todo_by_id(todo_id, exclude_fields=["string_id"])
            return Response(todo, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Todo item does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Delete a todo item by id.
    def delete(self, request, todo_id):
        try:
            todo_repository.delete_todo_by_id(todo_id)
            return Response(
                {"message": "Todo item deleted successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Update a todo item by id.
    def patch(self, request, todo_id):
        try:
            serializer = TodoInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            todo_repository.update_todo(
                todo_id,
                **serializer.validated_data,
            )
            todo = todo_repository.get_todo_by_id(todo_id, exclude_fields=["string_id"])
            response = {
                "message": "Todo item updated successfully",
                "data": todo,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
