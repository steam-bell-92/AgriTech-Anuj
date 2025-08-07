function handleRegister(event, url) {
  event.preventDefault();
  alert("Registration Successful! Redirecting to Login...");
  window.location.href = url;
}

function handleLogin(event, url) {
  event.preventDefault();
  alert("Login Successful! Redirecting to Dashboard...");
  window.location.href = url;
}
