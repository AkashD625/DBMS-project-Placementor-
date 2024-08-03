// document.addEventListener('DOMContentLoaded', () => {
//     const loginButton = document.querySelector('.btn');
//     const createAccountButton = document.querySelector('.create-account');
//     const createAccountFormButton = document.querySelector('.create-account-btn');
//     const userTypeInputs = document.querySelectorAll('input[name="user-type"]');

//     loginButton?.addEventListener('click', (event) => {
//         event.preventDefault();

//         let userType;
//         userTypeInputs.forEach(input => {
//             if (input.checked) {
//                 userType = input.value;
//             }
//         });

//         if (userType) {
//             // Adding visual transition effect
//             document.body.classList.add('fade-out');

//             setTimeout(() => {
//                 if (userType === 'student') {
//                     window.location.href = 'student-home.html';
//                 } else if (userType === 'admin') {
//                     window.location.href = 'admin-home.html';
//                 }
//             }, 500); 
//         }
//     });

//     createAccountButton?.addEventListener('click', () => {
//         // Adding visual transition effect
//         document.body.classList.add('fade-out');

//         setTimeout(() => {
//             window.location.href = 'student-acc.html';
//         }, 500); // Match this duration with the CSS transition time
//     });

//     createAccountFormButton?.addEventListener('click', (event) => {
//         event.preventDefault();

//         // Add form validation here if needed

//         // Adding visual transition effect
//         document.body.classList.add('fade-out');

//         setTimeout(() => {
//             window.location.href = 'index.html';
//         }, 500); // Match this duration with the CSS transition time
//     });
// });
