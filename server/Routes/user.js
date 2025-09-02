const express = require("express");
const router = express.Router();
const authController = require("../Controllers/user");
const authMiddleware = require("../Middlewares/authMiddleware");

// User Registration
router.post("/register", authController.register);

// User Login
router.post("/login", authController.login);

// User Logout
router.post("/logout", authController.logout);

// Get User Profile (Protected)
router.get("/profile", authMiddleware.verifyToken, authController.profile);

// Refresh Access Token
router.post("/refresh", authController.refreshToken);

module.exports = router;
