import { useState } from "react";
import DeleteAllTodos from "../DeleteAllTodos/DeleteAllTodos";
import Error from "../Error";
import "./AddTodo.css";

const AddTodo = ({ reload, setReload }) => {
  const [error, setError] = useState(null);

  const addTodo = (json) => {
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(json),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        if (data.error) setError(data.error);
        else setReload((prevState) => !prevState);
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(error);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const text = e.target.todo.value.trim();
    if (!text) return;
    addTodo({ task: text });
  };

  return (
    <form onSubmit={handleSubmit} className="add-item flex">
      <input
        type="text"
        name="todo"
        placeholder="Do some nerdy stuff!"
        className="grow"
        required
      />

      <button type="submit" className="btn btn-primary">
        Add
      </button>
      <DeleteAllTodos setReload={setReload} />

      {error && <Error error={error} />}
    </form>
  );
};

export default AddTodo;
