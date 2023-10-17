import { useState } from "react";
import Error from "../Error";
import "./TodoItem.css";

const TodoItem = ({ todo, setReload }) => {
  const { _id, task, completed } = todo;
  const [error, setError] = useState(null);

  const handleDelete = () => {
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/${_id}/`, {
      method: "DELETE",
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

  const handleCheck = (e) => {
    e.preventDefault();
    const status = e.target.checked;
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/${_id}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ completed: status }),
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

  return (
    <div>
      <div className="flex w-full justify-between todo-item white">
        <div className="flex">
          <div className="checkbox-wrapper-1">
            <input
              id={_id}
              className="substituted"
              type="checkbox"
              aria-hidden="true"
              name="status"
              checked={completed}
              onChange={handleCheck}
            />
            <label for={_id} className={completed ? "text completed" : "text"}>
              {task}
            </label>
          </div>
        </div>
        <button className="delete white" onClick={handleDelete}>
          &#x2715;
        </button>
      </div>
      {error && <Error error={error} />}
    </div>
  );
};

export default TodoItem;
