// app.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageDiv = document.getElementById('message');
    const releaseButton = document.getElementById('releaseButton');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
    
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
    
        try {
            const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
            });
    
            if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/ebook';
            } else {
            const errorData = await response.json();
            messageDiv.textContent = errorData.msg;
            }
        } catch (error) {
            console.error('Error:', error);
            messageDiv.textContent = 'An error occurred. Please try again.';
        }
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
        
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;
        
            try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
        
            if (response.ok) {
                const data = await response.json();
                messageDiv.textContent = data.msg;
                registerForm.reset();
            } else {
                const errorData = await response.json();
                messageDiv.textContent = errorData.msg;
            }
            } catch (error) {
            console.error('Error:', error);
            messageDiv.textContent = 'An error occurred. Please try again.';
            }
        });
    }
    

    if (releaseButton) {
      releaseButton.addEventListener('click', async () => {
        const accessToken = localStorage.getItem('access_token');
  
        try {
          const response = await fetch('/release_ebook', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            },
          });
  
          if (response.ok) {
            const data = await response.json();
            messageDiv.textContent = data.msg;
            // Perform any additional actions after releasing the e-book
          } else {
            const errorData = await response.json();
            messageDiv.textContent = errorData.msg;
          }
        } catch (error) {
          console.error('Error:', error);
          messageDiv.textContent = 'An error occurred. Please try again.';
        }
      });
    }
  });