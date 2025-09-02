const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");

const UserSchema = new mongoose.Schema(
  {
    username: { type: String, required: true, trim: true },
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
    },

    password: { type: String, required: true },
    role: {
      type: String,
      enum: ["buyer", "farmer", "equipment", "grocery"],
      default: "farmer",
    },
  },
  { timestamps: true }
);

// Hash password before saving
UserSchema.pre("save", async function (next) {
  if (!this.isModified("password")) return next();
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (err) {
    next(err);
  }
});

// Compare entered password with stored hashed password
UserSchema.methods.comparePassword = function (password) {
  return bcrypt.compare(password, this.password);
};

// Generate JWT tokens
UserSchema.methods.generateTokens = function () {
  const payload = { userId: this._id };
  const accessToken = jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: "15m",
  });
  const refreshToken = jwt.sign(payload, process.env.JWT_REFRESH_SECRET, {
    expiresIn: "7d",
  });
  return { accessToken, refreshToken };
};

module.exports = mongoose.model("User", UserSchema);
