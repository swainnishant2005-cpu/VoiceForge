import { useState } from "react";

const API_URL = "https://voiceforge-backend-5ci6.onrender.com/api";

function Register({ onShowLogin }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/auth/register`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            username,
            email,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Registration failed."
        );
      }

      setMessage(
        "Account created successfully. You can now login."
      );

      setUsername("");
      setEmail("");
      setPassword("");

    } catch (error) {
      setError(error.message);

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
          BRAND
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
          REGISTER CARD
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
            Create <span>Account</span>
          </h1>

          <p>
            Join VoiceForge and create natural speech
          </p>

        </div>


        {/* Error */}

        {error && (
          <div className="vf-auth-error">

            <span>⚠️</span>

            <span>
              {error}
            </span>

          </div>
        )}


        {/* Success */}

        {message && (
          <div className="vf-auth-success">

            <span>✓</span>

            <span>
              {message}
            </span>

          </div>
        )}


        {/* Form */}

        <form
          className="vf-login-form"
          onSubmit={handleRegister}
        >

          {/* Username */}

          <div className="vf-input-group">

            <label htmlFor="register-username">

              <span className="vf-input-icon">
                👤
              </span>

              Username

            </label>

            <div className="vf-input-wrapper">

              <input
                id="register-username"
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(event) => {
                  setUsername(
                    event.target.value
                  );

                  setError("");
                  setMessage("");
                }}
                minLength={3}
                maxLength={50}
                autoComplete="username"
                required
              />

            </div>

          </div>


          {/* Email */}

          <div className="vf-input-group">

            <label htmlFor="register-email">

              <span className="vf-input-icon">
                ✉
              </span>

              Email

            </label>

            <div className="vf-input-wrapper">

              <input
                id="register-email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(event) => {
                  setEmail(
                    event.target.value
                  );

                  setError("");
                  setMessage("");
                }}
                autoComplete="email"
                required
              />

            </div>

          </div>


          {/* Password */}

          <div className="vf-input-group">

            <label htmlFor="register-password">

              <span className="vf-input-icon">
                🔒
              </span>

              Password

            </label>

            <div className="vf-input-wrapper">

              <input
                id="register-password"
                type="password"
                placeholder="Minimum 6 characters"
                value={password}
                onChange={(event) => {
                  setPassword(
                    event.target.value
                  );

                  setError("");
                  setMessage("");
                }}
                minLength={6}
                maxLength={100}
                autoComplete="new-password"
                required
              />

            </div>

          </div>


          {/* Create Account */}

          <button
            type="submit"
            className="vf-login-button"
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="vf-spinner"></span>

                Creating Account...
              </>
            ) : (
              <>
                <span>
                  Create Account
                </span>

                <span className="vf-login-arrow">
                  →
                </span>
              </>
            )}

          </button>

        </form>


        {/* Login */}

        <div className="vf-register-text">

          <span>
            Already have an account?
          </span>

          <button
            type="button"
            onClick={onShowLogin}
          >
            Login
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

export default Register;