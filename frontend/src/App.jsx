import { useEffect, useState } from "react";
import Login from "./Auth/Login";
import Register from "./Auth/Register";
import "./App.css"
const API_URL = "http://127.0.0.1:8000/api";

function App() {
  // =========================================================
  // AUTHENTICATION
  // =========================================================

  const [token, setToken] = useState(
    localStorage.getItem("voiceforge_token")
  );

  const [showRegister, setShowRegister] = useState(false);

  // =========================================================
  // TTS STATE
  // =========================================================

  const [text, setText] = useState("");

  const [language, setLanguage] = useState("");

  const [voice, setVoice] = useState("");

  const [speed, setSpeed] = useState(1);

  const [voices, setVoices] = useState([]);

  const [loadingVoices, setLoadingVoices] = useState(true);

  const [generating, setGenerating] = useState(false);

  const [audioUrl, setAudioUrl] = useState("");

  const [audioHistory, setAudioHistory] = useState([]);

  // =========================================================
  // FAVORITES STATE
  // =========================================================

  const [favorites, setFavorites] = useState([]);

  // =========================================================
  // FILE UPLOAD STATE
  // =========================================================

  const [uploadingFile, setUploadingFile] = useState(false);

  const [uploadedFileName, setUploadedFileName] = useState("");

  const [error, setError] = useState("");

  const [backendOnline, setBackendOnline] = useState(false);

  // =========================================================
  // DAILY USAGE
  // =========================================================

  const [usage, setUsage] = useState({
    used: 0,
    limit: 10,
    remaining: 10
  });
  // =========================================================
  // AI ENHANCEMENT STATE
  // =========================================================

  const [aiLoading, setAiLoading] = useState(false);
  const [aiAction, setAiAction] = useState("");
  // =========================================================
  // AUTH FUNCTIONS
  // =========================================================

  const handleLogin = (accessToken) => {
    localStorage.setItem(
      "voiceforge_token",
      accessToken
    );

    setToken(accessToken);
  };

  const handleLogout = () => {
    localStorage.removeItem(
      "voiceforge_token"
    );

    setToken(null);

    setShowRegister(false);

    setAudioUrl("");

    setAudioHistory([]);

    setFavorites([]);

    setUploadedFileName("");

    setText("");

    setError("");
  };

  // =========================================================
  // LOAD DATABASE HISTORY
  // =========================================================

  useEffect(() => {
    const loadHistory = async () => {
      if (!token) {
        return;
      }

      try {
        const response = await fetch(
          `${API_URL}/history`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        if (response.status === 401) {
          handleLogout();
          return;
        }

        if (!response.ok) {
          throw new Error(
            data.detail || "Failed to load speech history."
          );
        }

        const history = Array.isArray(data)
          ? data
          : [];

        const formattedHistory = history.map(
          (item) => ({
            id: item.id,
            text: item.text,
            language: item.language,
            voice: item.voice,
            speed: item.speed,
            audioUrl:
              `${API_URL.replace("/api", "")}/api/audio/${item.audio_filename}`,
            createdAt: item.created_at,
          })
        );

        setAudioHistory(formattedHistory);

      } catch (error) {
        console.error(
          "Failed to load speech history:",
          error
        );

        setError(
          "Unable to load speech history."
        );
      }
    };

    loadHistory();
  }, [token]);



  // =========================================================
  // LOAD FAVORITES
  // =========================================================

  const loadFavorites = async () => {
    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/favorites`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        setError("Your session has expired. Please login again.");
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load favorites."
        );
      }

      setFavorites(
        Array.isArray(data.favorites) ? data.favorites : []
      );
    } catch (error) {
      console.error("Failed to load favorites:", error);
      setError("Unable to load favorites.");
    }
  };


  // =========================================================
  // FAVORITE TOGGLE
  // =========================================================

  const toggleFavorite = async (historyId) => {
    if (!token) {
      setError("Please login before using favorites.");
      return;
    }

    const isFavorite = favorites.some(
      (item) => item.history_id === historyId
    );

    try {
      const response = await fetch(
        `${API_URL}/favorites/${historyId}`,
        {
          method: isFavorite ? "DELETE" : "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        setError("Your session has expired. Please login again.");
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to update favorite."
        );
      }

      await loadFavorites();
    } catch (error) {
      console.error("Favorite error:", error);
      setError(
        error.message || "Unable to update favorite."
      );
    }
  };


  // =========================================================
  // CHECK BACKEND
  // =========================================================

  const checkBackend = async () => {
    try {
      const response = await fetch(
        `${API_URL}/health`
      );

      if (!response.ok) {
        throw new Error(
          "Backend is unavailable."
        );
      }

      setBackendOnline(true);
    } catch (error) {
      console.error(
        "Backend health check failed:",
        error
      );

      setBackendOnline(false);
    }
  };

  // =========================================================
  // LOAD VOICES
  // =========================================================

  // =========================================================
  // LOAD DAILY USAGE
  // =========================================================

  const loadUsage = async () => {
    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/usage`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load usage."
        );
      }

      setUsage({
        used: data.used,
        limit: data.limit,
        remaining: data.remaining
      });

    } catch (error) {
      console.error(
        "Failed to load daily usage:",
        error
      );
    }
  };

  const loadVoices = async () => {
    try {
      setLoadingVoices(true);

      const response = await fetch(
        `${API_URL}/voices`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load voices."
        );
      }

      const data =
        await response.json();

      const availableVoices =
        Array.isArray(data.voices)
          ? data.voices
          : [];

      setVoices(availableVoices);

      if (availableVoices.length > 0) {
        const firstVoice =
          availableVoices[0];

        setLanguage(
          firstVoice.language ||
          firstVoice.code ||
          firstVoice.id ||
          ""
        );

        setVoice(
          firstVoice.voice ||
          firstVoice.id ||
          firstVoice.code ||
          ""
        );
      }
    } catch (error) {
      console.error(
        "Failed to load voices:",
        error
      );

      setError(
        "Unable to load available voices."
      );
    } finally {
      setLoadingVoices(false);
    }
  };

  // =========================================================
  // INITIAL DATA LOAD
  // =========================================================

  useEffect(() => {
    if (!token) {
      return;
    }

    checkBackend();

    loadVoices();

    loadFavorites();
  }, [token]);

  // =========================================================
  // LANGUAGES
  // =========================================================

  const languages = [
    ...new Map(
      voices.map((item) => {
        const languageCode =
          item.language ||
          item.code ||
          item.id;

        const languageName =
          item.language_name ||
          item.name ||
          languageCode;

        return [
          languageCode,
          {
            code: languageCode,
            name: languageName,
          },
        ];
      })
    ).values(),
  ];

  // =========================================================
  // LANGUAGE CHANGE
  // =========================================================

  const handleLanguageChange = (
    selectedLanguage
  ) => {
    setLanguage(selectedLanguage);

    const matchingVoice =
      voices.find((item) => {
        const itemLanguage =
          item.language ||
          item.code ||
          item.id;

        return (
          itemLanguage ===
          selectedLanguage
        );
      });

    if (matchingVoice) {
      setVoice(
        matchingVoice.voice ||
        matchingVoice.id ||
        matchingVoice.code ||
        ""
      );
    } else {
      setVoice("");
    }
  };

  // =========================================================
  // CLEAR TEXT
  // =========================================================

  const clearText = () => {
    setText("");

    setUploadedFileName("");

    setError("");
  };
  // =========================================================
  // FILE UPLOAD
  // =========================================================

  const uploadFile = async (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");

    const allowedExtensions = [".txt", ".pdf", ".docx"];
    const extension = "." + file.name.split(".").pop().toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      setError("Unsupported file type. Please upload TXT, PDF, or DOCX.");
      event.target.value = "";
      return;
    }

    const maxFileSize = 10 * 1024 * 1024;

    if (file.size > maxFileSize) {
      setError("File size cannot exceed 10 MB.");
      event.target.value = "";
      return;
    }

    if (!token) {
      setError("Please login before uploading a file.");
      event.target.value = "";
      return;
    }

    try {
      setUploadingFile(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/files/extract`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        setError("Your session has expired. Please login again.");
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to extract text from the file."
        );
      }

      setText(data.text || "");
      setUploadedFileName(data.filename || file.name);
    } catch (error) {
      console.error("File upload error:", error);
      setError(error.message || "Unable to upload file.");
    } finally {
      setUploadingFile(false);
      event.target.value = "";
    }
  };


  // =========================================================
  // AI TEXT ENHANCEMENT
  // =========================================================

  const enhanceText = async (action) => {
    setError("");

    if (!token) {
      setError("Please login before using AI enhancement.");
      return;
    }

    if (!text.trim()) {
      setError("Please enter some text first.");
      return;
    }

    if (text.trim().length > 5000) {
      setError("Text cannot exceed 5000 characters.");
      return;
    }

    try {
      setAiLoading(true);
      setAiAction(action);

      const response = await fetch(
        `${API_URL}/ai/enhance`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            text: text.trim(),
            action: action,
          }),
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();

        setError(
          "Your session has expired. Please login again."
        );

        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to enhance text."
        );
      }

      setText(data.enhanced_text);

    } catch (error) {
      console.error(
        "AI enhancement error:",
        error
      );

      setError(
        error.message ||
        "Unable to enhance text."
      );

    } finally {
      setAiLoading(false);
      setAiAction("");
    }
  };

  // =========================================================
  // CLEAR HISTORY
  // =========================================================


  // CLEAR DATABASE HISTORY
  // =========================================================

  const clearHistory = async () => {
    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/history`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();

        setError(
          "Your session has expired. Please login again."
        );

        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to clear speech history."
        );
      }

      // Clear history from the UI
      setAudioHistory([]);

      setFavorites([]);

      console.log(
        "History cleared:",
        data.deleted_count
      );

    } catch (error) {
      console.error(
        "Clear history error:",
        error
      );

      setError(
        error.message ||
        "Unable to clear speech history."
      );
    }
  };
  // =========================================================
  // DELETE ONE HISTORY ITEM
  // =========================================================

  const deleteHistoryItem = async (historyId) => {
    if (!token) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/history/${historyId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();

        setError(
          "Your session has expired. Please login again."
        );

        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to delete speech history."
        );
      }

      // Remove the deleted item from the UI
      setAudioHistory((previousHistory) =>
        previousHistory.filter(
          (item) => item.id !== historyId
        )
      );

      setFavorites((previousFavorites) =>
        previousFavorites.filter(
          (item) => item.history_id !== historyId
        )
      );

    } catch (error) {
      console.error(
        "Delete history error:",
        error
      );

      setError(
        error.message ||
        "Unable to delete speech history."
      );
    }
  };

  // =========================================================
  // GENERATE SPEECH
  // =========================================================

  const generateSpeech = async () => {
    setError("");

    if (!token) {
      setError("Please login before generating speech.");
      return;
    }

    if (!text.trim()) {
      setError("Please enter some text first.");
      return;
    }

    if (text.trim().length > 5000) {
      setError("Text cannot exceed 5000 characters.");
      return;
    }

    if (!language) {
      setError("Please select a language.");
      return;
    }

    if (!voice) {
      setError("Please select a voice.");
      return;
    }

    try {
      setGenerating(true);

      // =========================================
      // 1. GENERATE SPEECH
      // =========================================

      const response = await fetch(
        `${API_URL}/tts`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            text: text.trim(),
            language: language,
            voice: voice,
            speed: Number(speed),
          }),
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();

        setError(
          "Your session has expired. Please login again."
        );

        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
          "Failed to generate speech."
        );
      }

      // =========================================
      // 2. CREATE FULL AUDIO URL
      // =========================================

      const fullAudioUrl =
        data.audio_url.startsWith("http")
          ? data.audio_url
          : `${API_URL.replace("/api", "")}${data.audio_url}`;

      setAudioUrl(fullAudioUrl);

      // =========================================
      // 3. SAVE HISTORY TO DATABASE
      // =========================================

      const historyResponse = await fetch(
        `${API_URL}/history`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },

          body: JSON.stringify({
            text: text.trim(),
            language: language,
            voice: voice,
            speed: Number(speed),
            audio_filename:
              data.audio_url.split("/").pop(),
          }),
        }
      );

      const historyData =
        await historyResponse.json();

      if (historyResponse.status === 401) {
        handleLogout();

        setError(
          "Your session has expired. Please login again."
        );

        return;
      }

      if (!historyResponse.ok) {
        console.error(
          "Failed to save speech history:",
          historyData
        );
      } else {
        // =========================================
        // 4. UPDATE FRONTEND HISTORY
        // =========================================

        const historyItem = {
          id: historyData.id,

          text: historyData.text,

          language: historyData.language,

          voice: historyData.voice,

          speed: historyData.speed,

          audioUrl: fullAudioUrl,

          createdAt:
            historyData.created_at,
        };

        setAudioHistory(
          (previousHistory) => [
            historyItem,
            ...previousHistory,
          ]
        );
      }

    } catch (error) {
      console.error(
        "Speech generation error:",
        error
      );

      setError(
        error.message ||
        "Unable to generate speech."
      );

    } finally {
      setGenerating(false);
    }
  };
  // =========================================================
  // WORD COUNT
  // =========================================================

  const wordCount = text.trim()
    ? text.trim().split(/\s+/).length
    : 0;

  // =========================================================
  // AUTH SCREEN
  // =========================================================

  if (!token) {
    if (showRegister) {
      return (
        <Register
          onShowLogin={() =>
            setShowRegister(false)
          }
        />
      );
    }

    return (
      <Login
        onLogin={handleLogin}
        onShowRegister={() =>
          setShowRegister(true)
        }
      />
    );
  }

  // =========================================================
  // MAIN VOICEFORGE UI
  // =========================================================

  return (
    <div className="app">
      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">
        <div className="header-inner">

          <div className="brand">
            <div className="brand-icon">
              🎙️
            </div>

            <div>
              <h1>VoiceForge</h1>

              <p>
                Text-to-Speech Studio
              </p>
            </div>
          </div>

          <div className="header-right">

            <div className="usage-badge">
              <span>Daily Usage</span>
              <strong>
                {usage.used} / {usage.limit}
              </strong>
            </div>

            <div
              className={`backend-status ${backendOnline
                ? "online"
                : "offline"
                }`}
            >
              <span className="status-dot"></span>

              {backendOnline
                ? "Backend Online"
                : "Backend Offline"}
            </div>

            <button
              type="button"
              className="logout-button"
              onClick={handleLogout}
            >
              Logout
            </button>

          </div>
        </div>
      </header>

      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="main-container">

        {/* ===================================================
            HERO
        =================================================== */}

        <section className="hero-section">

          <div className="hero-content">

            <span className="hero-badge">
              AI POWERED VOICE STUDIO
            </span>

            <h2>
              Turn your words into
              <span>
                {" "}natural speech.
              </span>
            </h2>

            <p>
              Create high-quality speech
              from your text using multiple
              languages and customizable
              speaking speeds.
            </p>

          </div>

          <div className="hero-decoration">
            <div className="sound-wave">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>

        </section>

        {/* ===================================================
            WORKSPACE
        =================================================== */}

        <section className="workspace">

          {/* =================================================
              TEXT CARD
          ================================================= */}

          <div className="card text-card">

            <div className="card-header">

              <div>
                <h3>
                  Enter your text
                </h3>

                <p>
                  Write or paste the text
                  you want to convert.
                </p>
              </div>

              <button
                type="button"
                className="clear-button"
                onClick={clearText}
                disabled={!text}
              >
                Clear
              </button>

            </div>

            <textarea
              className="text-input"
              placeholder="Type or paste your text here..."
              value={text}
              onChange={(event) =>
                setText(
                  event.target.value
                )
              }
              maxLength={5000}
            />
            {/* ===================================================
    AI ENHANCEMENT
=================================================== */}

            <div className="ai-enhancement">

              <div className="ai-header">
                <div>
                  <h4>✨ AI Text Enhancement</h4>
                  <p>
                    Improve your text before converting it to speech.
                  </p>
                </div>
              </div>

              <div className="ai-buttons">

                <button
                  type="button"
                  className="ai-button"
                  onClick={() => enhanceText("improve")}
                  disabled={aiLoading || !text.trim()}
                >
                  {aiLoading && aiAction === "improve"
                    ? "Improving..."
                    : "✨ Improve"}
                </button>

                <button
                  type="button"
                  className="ai-button"
                  onClick={() => enhanceText("grammar")}
                  disabled={aiLoading || !text.trim()}
                >
                  {aiLoading && aiAction === "grammar"
                    ? "Correcting..."
                    : "✓ Grammar"}
                </button>

                <button
                  type="button"
                  className="ai-button"
                  onClick={() => enhanceText("professional")}
                  disabled={aiLoading || !text.trim()}
                >
                  {aiLoading && aiAction === "professional"
                    ? "Rewriting..."
                    : "💼 Professional"}
                </button>

                <button
                  type="button"
                  className="ai-button"
                  onClick={() => enhanceText("conversational")}
                  disabled={aiLoading || !text.trim()}
                >
                  {aiLoading && aiAction === "conversational"
                    ? "Rewriting..."
                    : "💬 Conversational"}
                </button>

                <button
                  type="button"
                  className="ai-button"
                  onClick={() => enhanceText("summarize")}
                  disabled={aiLoading || !text.trim()}
                >
                  {aiLoading && aiAction === "summarize"
                    ? "Summarizing..."
                    : "📝 Summarize"}
                </button>

              </div>

            </div>

            {/* ===================================================
                FILE UPLOAD
            =================================================== */}

            <div className="file-upload">
              <div className="file-upload-info">
                <span className="file-icon">📄</span>
                <div>
                  <strong>Upload a document</strong>
                  <p>Extract text from TXT, PDF, or DOCX files.</p>
                </div>
              </div>

              <label
                htmlFor="file-upload"
                className="upload-button"
              >
                {uploadingFile ? "Extracting..." : "📂 Choose File"}
                <input
                  id="file-upload"
                  type="file"
                  accept=".txt,.pdf,.docx"
                  onChange={uploadFile}
                  disabled={uploadingFile}
                  hidden
                />
              </label>
            </div>

            {uploadedFileName && (
              <div className="uploaded-file">
                <span>✓ {uploadedFileName}</span>
                <button
                  type="button"
                  onClick={() => {
                    setUploadedFileName("");
                    setText("");
                  }}
                  title="Remove uploaded file"
                >
                  ✕
                </button>
              </div>
            )}

            <div className="text-meta">

              <span>
                {text.length} / 5000
                {" "}characters
              </span>

              <span>
                {wordCount} words
              </span>

            </div>

          </div>

          {/* =================================================
              SETTINGS CARD
          ================================================= */}

          <div className="card settings-card">

            <div className="card-header">

              <div>
                <h3>
                  Voice settings
                </h3>

                <p>
                  Customize your speech.
                </p>
              </div>

            </div>

            {/* LANGUAGE */}

            <div className="form-group">

              <label htmlFor="language">
                Language
              </label>

              <select
                id="language"
                value={language}
                onChange={(event) =>
                  handleLanguageChange(
                    event.target.value
                  )
                }
                disabled={
                  loadingVoices ||
                  languages.length === 0
                }
              >

                {loadingVoices ? (
                  <option>
                    Loading languages...
                  </option>
                ) : (
                  <>
                    <option value="">
                      Select language
                    </option>

                    {languages.map(
                      (item) => (
                        <option
                          key={item.code}
                          value={item.code}
                        >
                          {item.name}
                        </option>
                      )
                    )}
                  </>
                )}

              </select>

            </div>

            {/* VOICE */}

            <div className="form-group">

              <label htmlFor="voice">
                Voice
              </label>

              <select
                id="voice"
                value={voice}
                onChange={(event) =>
                  setVoice(
                    event.target.value
                  )
                }
                disabled={
                  loadingVoices ||
                  voices.length === 0
                }
              >

                {loadingVoices ? (
                  <option>
                    Loading voices...
                  </option>
                ) : (
                  <>
                    <option value="">
                      Select voice
                    </option>

                    {voices
                      .filter((item) => {
                        const itemLanguage =
                          item.language ||
                          item.code ||
                          item.id;

                        return (
                          !language ||
                          itemLanguage ===
                          language
                        );
                      })
                      .map((item) => {

                        const voiceId =
                          item.voice ||
                          item.id ||
                          item.code;

                        const voiceName =
                          item.name ||
                          item.voice_name ||
                          voiceId;

                        return (
                          <option
                            key={voiceId}
                            value={voiceId}
                          >
                            {voiceName}
                          </option>
                        );
                      })}

                  </>
                )}

              </select>

            </div>

            {/* SPEED */}

            <div className="form-group">

              <div className="speed-label-row">

                <label htmlFor="speed">
                  Speaking speed
                </label>

                <span className="speed-value">
                  {Number(speed).toFixed(1)}x
                </span>

              </div>

              <input
                id="speed"
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={speed}
                onChange={(event) =>
                  setSpeed(
                    Number(
                      event.target.value
                    )
                  )
                }
                className="speed-slider"
              />

              <div className="speed-range">

                <span>
                  0.5x
                </span>

                <span>
                  Normal
                </span>

                <span>
                  2.0x
                </span>

              </div>

            </div>

            {/* ERROR */}

            {error && (
              <div className="error-message">
                <span>⚠️</span>

                <span>
                  {error}
                </span>
              </div>
            )}

            {/* GENERATE */}

            <button
              type="button"
              className="generate-button"
              onClick={generateSpeech}
              disabled={
                generating ||
                loadingVoices ||
                !text.trim()
              }
            >

              {generating ? (
                <>
                  <span className="spinner"></span>

                  Generating Speech...
                </>
              ) : (
                <>
                  <span>
                    ✨
                  </span>

                  Generate Speech
                </>
              )}

            </button>

          </div>

        </section>

        {/* ===================================================
            GENERATED AUDIO
        =================================================== */}

        {audioUrl && (
          <section className="card output-card">

            <div className="card-header">

              <div>
                <h3>
                  Generated Audio
                </h3>

                <p>
                  Your speech is ready
                  to play.
                </p>
              </div>

              <span className="success-badge">
                ✓ Ready
              </span>

            </div>

            <div className="audio-player-wrapper">

              <audio
                controls
                src={audioUrl}
                className="audio-player"
              >
                Your browser does not
                support the audio element.
              </audio>

            </div>

            <div className="output-actions">

              <a
                href={audioUrl}
                download="voiceforge-speech.mp3"
                className="download-button"
              >
                ⬇ Download Audio
              </a>

            </div>

          </section>
        )}

        {/* ===================================================
            HISTORY
        =================================================== */}

        <section className="card history-card">

          <div className="card-header">

            <div>
              <h3>
                Speech History
              </h3>

              <p>
                Your recently generated
                speeches.
              </p>
            </div>

            {audioHistory.length > 0 && (
              <button
                type="button"
                className="clear-button"
                onClick={clearHistory}
              >
                Clear History
              </button>
            )}

          </div>

          {audioHistory.length === 0 ? (
            <div className="empty-history">

              <div className="empty-icon">
                🎧
              </div>

              <h4>
                No speech generated yet
              </h4>

              <p>
                Your generated audio will
                appear here.
              </p>

            </div>
          ) : (
            <div className="history-list">

              {audioHistory.map(
                (item) => (
                  <div
                    className="history-item"
                    key={item.id}
                  >

                    <div className="history-icon">
                      🔊
                    </div>

                    <div className="history-content">

                      <p className="history-text">
                        {item.text}
                      </p>

                      <div className="history-details">

                        <span>
                          {item.language}
                        </span>

                        <span>
                          •
                        </span>

                        <span>
                          {item.voice}
                        </span>

                        <span>
                          •
                        </span>

                        <span>
                          {item.speed}x
                        </span>

                      </div>

                    </div>

                    <div className="history-actions">

                      <audio
                        controls
                        src={item.audioUrl}
                      />

                      <a
                        href={item.audioUrl}
                        download="voiceforge-speech.mp3"
                        className="history-download"
                        title="Download audio"
                      >
                        ⬇
                      </a>

                      <button
                        type="button"
                        className="favorite-button"
                        onClick={() =>
                          toggleFavorite(item.id)
                        }
                        title={
                          favorites.some(
                            (favorite) =>
                              favorite.history_id === item.id
                          )
                            ? "Remove from favorites"
                            : "Add to favorites"
                        }
                      >
                        {favorites.some(
                          (favorite) =>
                            favorite.history_id === item.id
                        )
                          ? "★"
                          : "☆"}
                      </button>

                      <button
                        type="button"
                        className="history-delete"
                        onClick={() =>
                          deleteHistoryItem(item.id)
                        }
                        title="Delete history"
                      >
                        🗑️
                      </button>

                    </div>

                  </div>
                )
              )}

            </div>
          )}

        </section>

      </main>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="footer">

        <p>
          © {new Date().getFullYear()}
          {" "}VoiceForge. Built with
          React + FastAPI.
        </p>

      </footer>

    </div>
  );
}

export default App;