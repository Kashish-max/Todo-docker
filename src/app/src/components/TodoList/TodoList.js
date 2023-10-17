import { useEffect, useState } from "react";
import TodoItem from "../TodoItem/TodoItem";
import "./TodoList.css";

const TodoList = ({ reload, setReload }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/`)
      .then((response) => response.json())
      .then((data) => setData(data));
  }, [reload]);

  return (
    <div className="w-full white todo-list">
      {data.length ? (
        data.map((todo) => (
          <TodoItem key={todo._id} todo={todo} setReload={setReload} />
        ))
      ) : (
        <p className="white">No Todos Yet...</p>
      )}
    </div>
  );
};

export default TodoList;
