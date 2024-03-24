const tabs = document.querySelectorAll('.nav-tabs li');
const forms = document.querySelectorAll('.form-content form');

// Define existing user credentials (replace with your desired credentials)
const users = [
  { username: 'user1', password: 'password1' },
  { username: 'user2', password: 'password2' }
];

tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    forms.forEach(f => f.style.display = 'none');
    tabs[index].classList.add('active');
    forms[index].style.display = 'block';
  });
});

const signInForm = document.getElementById('sign-in-form');
const signUpForm = document.getElementById('sign-up-form');

signInForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Validate username and password
  let foundUser = false;
  for (const user of users) {
    if (user.username === username && user.password === password) {
      foundUser = true;
      break;
    }
  }

  if (foundUser) {
    alert('Sign in successful!');
    // Redirect to home page after successful sign in
    window.location.href = "http://localhost:5000/"; // Replace with your actual home page path
  } else {
    alert('Invalid username or password!');
  }
});

signUpForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  const newUsername = document.getElementById('new-username').value;
  const newPassword = document.getElementById('new-password').value;

  // Basic validation for username uniqueness (replace with server-side validation)
  let usernameExists = false;
  for (const user of users) {
    if (user.username === newUsername) {
      usernameExists = true;
      break;
    }
  }

  if (usernameExists) {
    alert('Username already exists!');
  } else {
    // Add new user to the in-memory list (replace with server-side storage)
    // users.push({ username: newUsername, password: newPassword });
    alert('Sign up successful! Please sign in with your new credentials.');
  }
});
