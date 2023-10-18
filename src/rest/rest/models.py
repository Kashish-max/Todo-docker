from datetime import datetime

# Define a TodoItem class to represent a todo item data model
class TodoItem:
    _id: int
    string_id: str
    task: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        _id=None,
        string_id=None,
        task=None,
        completed=False,
        created_at=None,
        updated_at=None,
    ):
        self._id = _id
        self.string_id = string_id
        self.task = task
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def serialized_data(self, exclude=[]):
        self._id = str(self._id)
        return {
            key: value for key, value in self.__dict__.items() if key not in exclude
        }
