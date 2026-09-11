import { useState } from "react";

const API_URL = "https://voiceforge-backend-5ci6.onrender.com/api";

function Login({ onLogin, onShowRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!email.trim()) {
      setError("Please enter your email.");
      return;
    }

    if (!password) {
      setError("Please enter your password.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `${API_URL}/auth/login`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            email: email.trim(),
            password: password,
          }),
        }
      );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Invalid email or password."
        );
      }

      if (!data.access_token) {
        throw new Error(
          "Invalid login response."
        );
      }

      onLogin(data.access_token);

    } catch (err) {
      console.error(
        "Login error:",
        err
      );

      setError(
        err.message ||
          "Unable to login. Please try again."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="vf-auth-page">

      {/* =========================================
          BACKGROUND
      ========================================= */}

      <div className="vf-auth-background">

        <div className="vf-orb vf-orb-purple"></div>

        <div className="vf-orb vf-orb-blue"></div>

        <div className="vf-orb vf-orb-pink"></div>

        <div className="vf-particle particle-1"></div>
        <div className="vf-particle particle-2"></div>
        <div className="vf-particle particle-3"></div>
        <div className="vf-particle particle-4"></div>
        <div className="vf-particle particle-5"></div>
        <div className="vf-particle particle-6"></div>

        {/* Audio waves */}

        <div className="vf-wave wave-one"></div>

        <div className="vf-wave wave-two"></div>

        <div className="vf-wave wave-three"></div>

      </div>


      {/* =========================================
          SIDE TEXT
      ========================================= */}

      <div className="vf-side-text vf-left-text">
        <span>YOUR WORDS</span>
        <span>OUR VOICES</span>
      </div>

      <div className="vf-side-text vf-right-text">
        <span>LISTEN</span>
        <span>CREATE</span>
        <span>INSPIRE</span>
      </div>


      {/* =========================================
          LEFT BRAND
      ========================================= */}

      <div className="vf-brand-side">

        <div className="vf-brand-name">
          VoiceForge
        </div>

        <div className="vf-brand-line"></div>

        <div className="vf-brand-subtitle">
          TEXT-TO-SPEECH STUDIO
        </div>

      </div>


      {/* =========================================
          LOGIN CARD
      ========================================= */}

      <div className="vf-login-card">

        {/* Window dots */}

        <div className="vf-window-dots">

          <span className="dot-pink"></span>

          <span className="dot-purple"></span>

          <span className="dot-blue"></span>

        </div>


        {/* Logo */}

        <div className="vf-login-logo">
          🎙️
        </div>


        {/* Heading */}

        <div className="vf-login-heading">

          <h1>
            Welcome <span>Back</span>
          </h1>

          <p>
            Login to continue using VoiceForge
          </p>

        </div>


        {/* Error */}

        {error && (
          <div className="vf-auth-error">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}


        {/* Form */}

        <form
          className="vf-login-form"
          onSubmit={handleSubmit}
        >

          {/* Email */}

          <div className="vf-input-group">

            <label htmlFor="email">
              <span className="vf-input-icon">
                ✉
              </span>
              Email
            </label>

            <div className="vf-input-wrapper">

              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(event) => {
                  setEmail(
                    event.target.value
                  );

                  setError("");
                }}
                autoComplete="email"
              />

            </div>

          </div>


          {/* Password */}

          <div className="vf-input-group">

            <label htmlFor="password">

              <span className="vf-input-icon">
                🔒
              </span>

              Password

            </label>

            <div className="vf-input-wrapper">

              <input
                id="password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Enter your password"
                value={password}
                onChange={(event) => {
                  setPassword(
                    event.target.value
                  );

                  setError("");
                }}
                autoComplete="current-password"
              />

              <button
                type="button"
                className="vf-password-toggle"
                onClick={() =>
                  setShowPassword(
                    !showPassword
                  )
                }
                aria-label={
                  showPassword
                    ? "Hide password"
                    : "Show password"
                }
              >
                {showPassword
                  ? "🙈"
                  : "👁️"}
              </button>

            </div>

          </div>


          {/* Login button */}

          <button
            type="submit"
            className="vf-login-button"
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="vf-spinner"></span>
                Signing in...
              </>
            ) : (
              <>
                <span>Login</span>
                <span className="vf-login-arrow">
                  →
                </span>
              </>
            )}

          </button>

        </form>


        {/* Register */}

        <div className="vf-register-text">

          <span>
            Don't have an account?
          </span>

          <button
            type="button"
            onClick={onShowRegister}
          >
            Create Account
          </button>

        </div>


        {/* Security */}

        <div className="vf-security">

          <span>🔐</span>

          <span>
            Secure authentication powered by JWT
          </span>

        </div>

      </div>


      {/* =========================================
          TAGLINE
      ========================================= */}

      <div className="vf-tagline">

        <span>Convert Text</span>

        <span>into Life</span>

        <div></div>

      </div>


      {/* =========================================
          FOOTER
      ========================================= */}

      <div className="vf-auth-footer">
        © {new Date().getFullYear()} VoiceForge.
        All rights reserved.
      </div>

    </div>
  );
}

export default Login;