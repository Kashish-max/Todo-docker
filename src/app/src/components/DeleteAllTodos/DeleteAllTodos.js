const DeleteAllTodos = ({ setReload }) => {
  const deleteAllTodos = () => {
    fetch(`${process.env.REACT_APP_SERVER_URL}/todos/`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setReload((prevState) => !prevState);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  return (
    <button className="btn btn-danger" onClick={deleteAllTodos}>
      Delete All
    </button>
  );
};

export default DeleteAllTodos;
