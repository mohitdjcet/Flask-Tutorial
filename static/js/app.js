const todoForm = document.getElementById("todoForm");
const todoInput = document.getElementById("todoInput");
const todoList = document.getElementById("todoList");

const totalTasks = document.getElementById("totalTasks");
const completedTasks = document.getElementById("completedTasks");
const pendingTasks = document.getElementById("pendingTasks");

const loading = document.getElementById("loading");
const emptyState = document.getElementById("emptyState");
const message = document.getElementById("message");

// Show message
function showMessage(text, type = "success") {
  message.textContent = text;
  message.className = type === "success" ? "message-success" : "message-error";

  setTimeout(() => {
    message.textContent = "";
    message.className = "";
  }, 2500);
}

// Fetch all todos
async function fetchTodos() {
  try {
    loading.classList.remove("hidden");

    const response = await fetch("/todos");

    if (!response.ok) {
      throw new Error("Failed to fetch todos");
    }

    const data = await response.json();

    renderTodos(data.todos);
  } catch (error) {
    console.error(error);

    showMessage("Unable to load tasks", "error");
  } finally {
    loading.classList.add("hidden");
  }
}

// Render todos
function renderTodos(todos) {
  todoList.innerHTML = "";

  totalTasks.textContent = todos.length;

  const completed = todos.filter((todo) => todo.completed).length;

  const pending = todos.length - completed;

  completedTasks.textContent = completed;
  pendingTasks.textContent = pending;

  if (todos.length === 0) {
    emptyState.classList.remove("hidden");

    return;
  }

  emptyState.classList.add("hidden");

  todos.forEach((todo) => {
    const todoElement = document.createElement("div");

    todoElement.className = `todo-item ${todo.completed ? "completed" : ""}`;

    todoElement.innerHTML = `
            <input
                type="checkbox"
                ${todo.completed ? "checked" : ""}
                onchange="toggleTodo(
                    ${todo.id},
                    this.checked
                )"
            >

            <div class="todo-content">
                <div class="todo-title">
                    ${escapeHtml(todo.title)}
                </div>
            </div>

            <div class="todo-actions">

                <button
                    onclick="editTodo(
                        ${todo.id},
                        '${escapeForAttribute(todo.title)}'
                    )"
                >
                    ✏️
                </button>

                <button
                    onclick="deleteTodo(${todo.id})"
                >
                    🗑️
                </button>

            </div>
        `;

    todoList.appendChild(todoElement);
  });
}

// Add Todo
todoForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const title = todoInput.value.trim();

  if (!title) {
    showMessage("Please enter a task", "error");

    return;
  }

  try {
    const response = await fetch("/todos", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title: title,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Unable to add task");
    }

    todoInput.value = "";

    showMessage("Task added successfully");

    fetchTodos();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

// Toggle completed
async function toggleTodo(id, completed) {
  try {
    const response = await fetch(`/todos/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        completed: completed,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Unable to update task");
    }

    showMessage(completed ? "Task completed" : "Task marked as pending");

    fetchTodos();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

// Edit Todo
async function editTodo(id, oldTitle) {
  const newTitle = prompt("Update your task:", oldTitle);

  if (newTitle === null) {
    return;
  }

  const title = newTitle.trim();

  if (!title) {
    showMessage("Task title cannot be empty", "error");

    return;
  }

  try {
    const response = await fetch(`/todos/${id}`, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title: title,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Unable to update task");
    }

    showMessage("Task updated successfully");

    fetchTodos();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

// Delete Todo
async function deleteTodo(id) {
  const confirmed = confirm("Are you sure you want to delete this task?");

  if (!confirmed) {
    return;
  }

  try {
    const response = await fetch(`/todos/${id}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || "Unable to delete task");
    }

    showMessage("Task deleted successfully");

    fetchTodos();
  } catch (error) {
    showMessage(error.message, "error");
  }
}

// Basic HTML escaping
function escapeHtml(value) {
  const div = document.createElement("div");

  div.textContent = value;

  return div.innerHTML;
}

// Safe value for the prompt argument
function escapeForAttribute(value) {
  return value
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'")
    .replace(/\r?\n/g, " ");
}

// Initial load
fetchTodos();
