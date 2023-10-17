import { useState } from "react";

const DeleteAllTodos = ({ setReload }) => {
  const [error, setError] = useState(null);
  const deleteAllTodos = () => {
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/`, {
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
  return (
    <button className="btn btn-danger" onClick={deleteAllTodos}>
      Delete All
    </button>
  );
};

export default DeleteAllTodos;
