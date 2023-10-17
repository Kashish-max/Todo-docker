import { useState } from "react";
import TodoList from "./components/TodoList/TodoList";
import AddTodo from "./components/AddTodo/AddTodo";
import "./App.css";

export function App() {
  const [reload, setReload] = useState(false);
  return (
    <div className="App flex items-center flex-col">
      <div className="list-container w-full">
        <h2 className="font-bold text-right" style={{ padding: "0 40px 20px" }}>
          Create Todos
        </h2>
        <div className="bg-white list-wrapper">
          <AddTodo reload={reload} setReload={setReload} />
          <TodoList reload={reload} setReload={setReload} />
        </div>
      </div>
    </div>
  );
}

export default App;
