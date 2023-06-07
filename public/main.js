window.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#prompt-form");
  const promptInput = document.querySelector("#prompt-input");
  const outputDiv = document.querySelector("#output");
  const loginButton = document.querySelector("#login-button");
  const registerButton = document.querySelector("#register-button");
  const logoutButton = document.querySelector("#logout-button");
  const loginMessage = document.querySelector("#login-message");
  const submitButton = document.querySelector("#submit-button");
  const spinner = document.querySelector("#spinner");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submitButton.style.display = "none";
    spinner.style.display = "block";
    const prompt = promptInput.value;
    const response = await fetch("https://flask-production-4552.up.railway.app/process_prompt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        prompt
      })
    });

    const responseSection = document.querySelector("#response-section");

    if (response.ok) {
      const data = await response.json();
      outputDiv.innerHTML = `<pre style="white-space: pre-wrap;">${JSON.stringify(
        data,
        null,
        2
      )}</pre>`;
      document.querySelector("#response-section").classList.remove("hidden");
    } else {
      outputDiv.textContent = `Error: ${response.status}`;
      document.querySelector("#response-section").classList.remove("hidden");
    }
    submitButton.style.display = "block";
    spinner.style.display = "none";
  });

  registerButton.addEventListener("click", async () => {
    const username = prompt("Enter your username");
    const email = prompt("Enter your email");
    const password = prompt("Enter your password");
    const response = await fetch("https://flask-production-4552.up.railway.app/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        email,
        password
      })
    });

    if (response.ok) {
      alert("User registered successfully");
      loginMessage.classList.add("hidden");
    } else {
      alert("Registration failed");
    }
  });

  loginButton.addEventListener("click", async () => {
    const email = prompt("Enter your email");
    const password = prompt("Enter your password");
    const response = await fetch("https://flask-production-4552.up.railway.app/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email,
        password
      })
    });

    if (response.ok) {
      const data = await response.json();
      const { access_token } = data;
      localStorage.setItem("access_token", access_token);
      form.classList.remove("hidden");
      loginButton.classList.add("hidden");
      registerButton.classList.add("hidden");
      logoutButton.classList.remove("hidden");
      loginMessage.classList.add("hidden");
    } else {
      alert("Login failed");
    }
  });

  logoutButton.addEventListener("click", () => {
    localStorage.removeItem("access_token");
    form.classList.add("hidden");
    loginButton.classList.remove("hidden");
    registerButton.classList.remove("hidden");
    logoutButton.classList.add("hidden");
    loginMessage.classList.remove("hidden");
  });

  const access_token = localStorage.getItem("access_token");
  if (access_token) {
    form.classList.remove("hidden");
    loginButton.classList.add("hidden");
    registerButton.classList.add("hidden");
    logoutButton.classList.remove("hidden");
    loginMessage.classList.add("hidden");
  }
});
