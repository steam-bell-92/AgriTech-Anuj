import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-auth.js";

// Secure Firebase configuration - fetched from server
let firebaseConfig = null;
let app = null;
let auth = null;

// Initialize Firebase securely
async function initializeFirebase() {
  try {
    const response = await fetch('/api/firebase-config');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    firebaseConfig = await response.json();
    
    // Validate that we have the required configuration
    if (!firebaseConfig.apiKey || !firebaseConfig.authDomain || !firebaseConfig.projectId) {
      throw new Error('Incomplete Firebase configuration received from server');
    }
    
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    auth.languageCode = 'en';
    
    console.log('Firebase initialized successfully');
    return true;
  } catch (error) {
    console.error('Failed to initialize Firebase:', error);
    return false;
  }
}

const provider = new GoogleAuthProvider();

// Initialize Firebase and set up event listeners
async function setupFirebaseAuth() {
  const initialized = await initializeFirebase();
  if (!initialized) {
    console.error('Firebase initialization failed. Google login will not work.');
    return;
  }
  
  const googleLogin = document.getElementById("google-login-btn");
  if (googleLogin) {
        googleLogin.addEventListener("click", async function () {
      try {
        const result = await signInWithPopup(auth, provider);
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const user = result.user;
        console.log(user);
        window.location.href = "index.html"; // Redirect to home page after successful login
      } catch (error) {  
        const errorCode = error.code;
        const errorMessage = error.message;

        console.error("Google sign-in error:", errorCode, errorMessage);

        // Show user-friendly message
        switch (errorCode) {
          case 'auth/popup-closed-by-user':
            alert("Sign-in popup was closed before completing. Please try again.");
            break;
          case 'auth/cancelled-popup-request':
            alert("Multiple sign-in attempts detected. Please wait and try again.");
            break;
          case 'auth/popup-blocked':
            alert("Popup was blocked by the browser. Please allow popups and try again.");
            break;
          case 'auth/network-request-failed':
            alert("Network error occurred. Check your connection and try again.");
            break;
          default:
            alert("Google sign-in failed. Please try again later.");
        }
      }
    });
  }
}

// Initialize Firebase authentication when the script loads
setupFirebaseAuth();
});