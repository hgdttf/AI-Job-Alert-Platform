import { useEffect, useState } from "react";
import API from "./api";

// =========================
// HOUR / MINUTE OPTIONS
// =========================

const hours = Array.from({ length: 12 }, (_, i) =>
  String(i + 1).padStart(2, "0")
);

const minutes = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"];

// =========================
// CATEGORY LIST
// =========================

const CATEGORIES = [
  { label: "BTech", icon: "🎓" },
  { label: "MTech", icon: "📘" },
  { label: "MS Research", icon: "🔬" },
  { label: "Life Sciences", icon: "🧬" },
  { label: "Internships", icon: "💼" },
  { label: "Remote", icon: "🌐" },
  { label: "AI/ML", icon: "🤖" },
  { label: "Cybersecurity", icon: "🔐" },
  { label: "Cloud", icon: "☁️" },
  { label: "Software", icon: "💻" },
];

// =========================
// MAIN APP
// =========================

export default function App() {
  const [email, setEmail] = useState("");
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [hour, setHour] = useState("09");
  const [minute, setMinute] = useState("00");
  const [period, setPeriod] = useState("AM");
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState({ text: "", type: "" });
  const [loading, setLoading] = useState(false);

  const selectedTime = `${hour}:${minute} ${period}`;

  // =========================
  // TOGGLE CATEGORY
  // =========================

  const toggleCategory = (category) => {
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((item) => item !== category)
        : [...prev, category]
    );
  };

  // =========================
  // FETCH USERS
  // =========================

  const fetchUsers = async () => {
    try {
      const response = await API.get("/users");
      setUsers(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  // =========================
  // REGISTER USER
  // =========================

  const registerUser = async () => {
    setMessage({ text: "", type: "" });

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setMessage({ text: "Please enter a valid email address.", type: "error" });
      return;
    }

    if (selectedCategories.length === 0) {
      setMessage({ text: "Select at least one category.", type: "error" });
      return;
    }

    setLoading(true);
    try {
      await API.post("/register", {
        email,
        categories: selectedCategories,
        delivery_time: selectedTime,
      });

      setMessage({ text: "🎉 You're all set! Alerts activated.", type: "success" });
      setEmail("");
      setSelectedCategories([]);
      setHour("09");
      setMinute("00");
      setPeriod("AM");
      fetchUsers();
    } catch (error) {
      setMessage({ text: error.message || "Registration failed. Try again.", type: "error" });
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // LOAD USERS ON MOUNT
  // =========================

  useEffect(() => {
    fetchUsers();
  }, []);

  // =========================
  // RENDER
  // =========================

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
          --bg: #020917;
          --surface: rgba(255,255,255,0.03);
          --surface-hover: rgba(255,255,255,0.06);
          --border: rgba(255,255,255,0.08);
          --border-focus: rgba(34,211,238,0.5);
          --cyan: #22d3ee;
          --cyan-dim: rgba(34,211,238,0.15);
          --blue: #3b82f6;
          --text: #f0f6ff;
          --muted: #8b9ab3;
          --radius-sm: 10px;
          --radius-md: 14px;
          --radius-lg: 20px;
        }

        body { background: var(--bg); }

        .app {
          min-height: 100vh;
          background: var(--bg);
          color: var(--text);
          font-family: 'DM Sans', sans-serif;
          font-size: 15px;
          overflow-x: hidden;
          position: relative;
        }

        /* Grid background */
        .app::before {
          content: '';
          position: fixed;
          inset: 0;
          background-image:
            linear-gradient(rgba(34,211,238,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(34,211,238,0.03) 1px, transparent 1px);
          background-size: 48px 48px;
          pointer-events: none;
          z-index: 0;
        }

        /* Radial glow */
        .app::after {
          content: '';
          position: fixed;
          top: -20%;
          right: -10%;
          width: 60vw;
          height: 60vw;
          background: radial-gradient(ellipse, rgba(34,211,238,0.06) 0%, transparent 70%);
          pointer-events: none;
          z-index: 0;
        }

        /* NAVBAR */
        .navbar {
          position: relative;
          z-index: 10;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 20px 48px;
          border-bottom: 1px solid var(--border);
          background: rgba(2,9,23,0.8);
          backdrop-filter: blur(20px);
        }

        .logo {
          font-family: 'Syne', sans-serif;
          font-size: 20px;
          font-weight: 800;
          letter-spacing: -0.5px;
          background: linear-gradient(135deg, #22d3ee, #3b82f6);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .nav-links {
          display: flex;
          gap: 32px;
          list-style: none;
        }

        .nav-links a {
          color: var(--muted);
          text-decoration: none;
          font-size: 14px;
          font-weight: 400;
          transition: color 0.2s;
        }

        .nav-links a:hover { color: var(--cyan); }

        .nav-badge {
          font-size: 12px;
          padding: 5px 14px;
          border-radius: 99px;
          border: 1px solid var(--border-focus);
          color: var(--cyan);
          background: var(--cyan-dim);
          font-weight: 500;
        }

        /* HERO */
        .hero {
          position: relative;
          z-index: 10;
          max-width: 1200px;
          margin: 0 auto;
          padding: 80px 48px 60px;
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 80px;
          align-items: center;
        }

        @media (max-width: 900px) {
          .hero { grid-template-columns: 1fr; padding: 40px 20px; gap: 40px; }
          .navbar { padding: 16px 20px; }
          .nav-links { display: none; }
        }

        /* LEFT SIDE */
        .tag-pill {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 16px;
          border-radius: 99px;
          border: 1px solid rgba(34,211,238,0.25);
          background: rgba(34,211,238,0.08);
          color: var(--cyan);
          font-size: 13px;
          margin-bottom: 28px;
        }

        .tag-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: var(--cyan);
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.5; transform: scale(0.8); }
        }

        h1.hero-title {
          font-family: 'Syne', sans-serif;
          font-size: clamp(38px, 5vw, 58px);
          font-weight: 800;
          line-height: 1.1;
          letter-spacing: -1.5px;
          color: var(--text);
          margin-bottom: 20px;
        }

        h1.hero-title .accent {
          background: linear-gradient(135deg, #22d3ee 0%, #3b82f6 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .hero-desc {
          color: var(--muted);
          font-size: 16px;
          line-height: 1.7;
          max-width: 440px;
          margin-bottom: 40px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 12px;
        }

        .stat-card {
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 18px 16px;
          transition: border-color 0.2s, background 0.2s;
        }

        .stat-card:hover {
          border-color: rgba(34,211,238,0.2);
          background: var(--surface-hover);
        }

        .stat-value {
          font-family: 'Syne', sans-serif;
          font-size: 28px;
          font-weight: 700;
          color: var(--cyan);
          line-height: 1;
          margin-bottom: 6px;
        }

        .stat-label {
          font-size: 12px;
          color: var(--muted);
          font-weight: 400;
        }

        /* RIGHT FORM CARD */
        .form-card {
          background: rgba(255,255,255,0.025);
          border: 1px solid var(--border);
          border-radius: var(--radius-lg);
          padding: 36px;
          backdrop-filter: blur(24px);
          position: relative;
          overflow: hidden;
        }

        .form-card::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 1px;
          background: linear-gradient(90deg, transparent, rgba(34,211,238,0.4), transparent);
        }

        .form-title {
          font-family: 'Syne', sans-serif;
          font-size: 26px;
          font-weight: 700;
          margin-bottom: 6px;
          letter-spacing: -0.5px;
        }

        .form-subtitle {
          color: var(--muted);
          font-size: 14px;
          margin-bottom: 28px;
        }

        .field-group {
          margin-bottom: 22px;
        }

        .field-label {
          display: block;
          font-size: 12px;
          font-weight: 500;
          letter-spacing: 0.5px;
          text-transform: uppercase;
          color: var(--muted);
          margin-bottom: 10px;
        }

        .text-input {
          width: 100%;
          background: rgba(0,0,0,0.3);
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          padding: 13px 16px;
          color: var(--text);
          font-family: 'DM Sans', sans-serif;
          font-size: 15px;
          outline: none;
          transition: border-color 0.2s, box-shadow 0.2s;
        }

        .text-input::placeholder { color: rgba(139,154,179,0.5); }

        .text-input:focus {
          border-color: var(--border-focus);
          box-shadow: 0 0 0 3px rgba(34,211,238,0.08);
        }

        /* TIME SELECTOR */
        .time-row {
          display: flex;
          gap: 10px;
        }

        .time-select {
          flex: 1;
          background: rgba(0,0,0,0.3);
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          padding: 12px 14px;
          color: var(--text);
          font-family: 'DM Sans', sans-serif;
          font-size: 14px;
          outline: none;
          cursor: pointer;
          transition: border-color 0.2s;
          appearance: none;
          text-align: center;
        }

        .time-select:focus { border-color: var(--border-focus); }

        .time-select option {
          background: #0f172a;
          color: var(--text);
        }

        /* CATEGORY CHIPS */
        .chips-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .chip {
          display: inline-flex;
          align-items: center;
          gap: 5px;
          padding: 8px 14px;
          border-radius: var(--radius-sm);
          border: 1px solid var(--border);
          background: var(--surface);
          color: var(--muted);
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          transition: border-color 0.18s ease, background 0.18s ease,
                      color 0.18s ease, transform 0.1s ease,
                      box-shadow 0.18s ease;
          user-select: none;
          outline: none;
          -webkit-tap-highlight-color: transparent;
        }

        .chip:hover {
          border-color: rgba(34,211,238,0.3);
          color: var(--text);
          background: var(--surface-hover);
        }

        .chip:focus-visible {
          border-color: var(--cyan);
          box-shadow: 0 0 0 3px rgba(34,211,238,0.2);
          color: var(--text);
        }

        .chip:active {
          transform: scale(0.95);
        }

        .chip.active {
          background: rgba(34,211,238,0.12);
          border-color: var(--cyan);
          color: var(--cyan);
        }

        .chip.active:hover {
          background: rgba(34,211,238,0.18);
        }

        .chip.active:focus-visible {
          box-shadow: 0 0 0 3px rgba(34,211,238,0.3);
        }

        .chip-icon { font-size: 14px; line-height: 1; }

        /* SUBMIT BUTTON */
        .submit-btn {
          width: 100%;
          padding: 15px;
          border-radius: var(--radius-sm);
          border: none;
          background: linear-gradient(135deg, #22d3ee, #3b82f6);
          color: #020917;
          font-family: 'Syne', sans-serif;
          font-size: 15px;
          font-weight: 700;
          letter-spacing: 0.3px;
          cursor: pointer;
          transition: all 0.2s;
          margin-top: 8px;
          position: relative;
          overflow: hidden;
        }

        .submit-btn:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 8px 24px rgba(34,211,238,0.25);
        }

        .submit-btn:active:not(:disabled) {
          transform: translateY(0);
        }

        .submit-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        /* MESSAGE BANNER */
        .message-banner {
          padding: 11px 16px;
          border-radius: var(--radius-sm);
          font-size: 14px;
          margin-bottom: 16px;
          font-weight: 500;
        }

        .message-banner.error {
          background: rgba(239,68,68,0.1);
          border: 1px solid rgba(239,68,68,0.3);
          color: #fca5a5;
        }

        .message-banner.success {
          background: rgba(34,211,238,0.08);
          border: 1px solid rgba(34,211,238,0.3);
          color: var(--cyan);
        }

        /* FEATURES STRIP */
        .features-strip {
          position: relative;
          z-index: 10;
          max-width: 1200px;
          margin: 0 auto 80px;
          padding: 0 48px;
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 20px;
        }

        @media (max-width: 700px) {
          .features-strip { grid-template-columns: 1fr; padding: 0 20px; }
        }

        .feature-card {
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 24px;
          transition: border-color 0.2s;
        }

        .feature-card:hover {
          border-color: rgba(34,211,238,0.2);
        }

        .feature-icon {
          font-size: 28px;
          margin-bottom: 14px;
        }

        .feature-title {
          font-family: 'Syne', sans-serif;
          font-size: 16px;
          font-weight: 700;
          margin-bottom: 8px;
          color: var(--text);
        }

        .feature-desc {
          font-size: 13px;
          color: var(--muted);
          line-height: 1.6;
        }

        /* DIVIDER */
        .divider {
          border: none;
          border-top: 1px solid var(--border);
          margin: 0 48px;
          position: relative;
          z-index: 10;
        }

        /* FOOTER */
        .footer {
          position: relative;
          z-index: 10;
          text-align: center;
          padding: 28px 48px;
          color: var(--muted);
          font-size: 13px;
        }
      `}</style>

      <div className="app">
        {/* Navbar */}
        <nav className="navbar">
          <span className="logo">JobPulse AI</span>
          <ul className="nav-links">
            <li><a href="#">Features</a></li>
            <li><a href="#">Categories</a></li>
            <li><a href="#">Alerts</a></li>
          </ul>
          <span className="nav-badge">✦ AI Powered</span>
        </nav>

        {/* Hero */}
        <section className="hero">

          {/* Left */}
          <div>
            <div className="tag-pill">
              <span className="tag-dot"></span>
              Automated Job Aggregation
            </div>

            <h1 className="hero-title">
              Discover Fresh<br />
              <span className="accent">Jobs Faster</span>
            </h1>

            <p className="hero-desc">
              AI-powered email alerts for internships, fresher jobs, research
              opportunities, and remote positions — curated daily and delivered
              straight to your inbox.
            </p>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{users.length}</div>
                <div className="stat-label">Registered Users</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">24/7</div>
                <div className="stat-label">Smart Alerts</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">10+</div>
                <div className="stat-label">Categories</div>
              </div>
            </div>
          </div>

          {/* Right — Form */}
          <div className="form-card">
            <h2 className="form-title">Register for Alerts</h2>
            <p className="form-subtitle">Stay updated with the latest opportunities.</p>

            {/* Message */}
            {message.text && (
              <div className={`message-banner ${message.type}`}>
                {message.text}
              </div>
            )}

            {/* Email */}
            <div className="field-group">
              <label className="field-label">Email Address</label>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="text-input"
              />
            </div>

            {/* Delivery Time */}
            <div className="field-group">
              <label className="field-label">Delivery Time</label>
              <div className="time-row">
                <select
                  value={hour}
                  onChange={(e) => setHour(e.target.value)}
                  className="time-select"
                >
                  {hours.map((h) => (
                    <option key={h} value={h}>{h}</option>
                  ))}
                </select>
                <select
                  value={minute}
                  onChange={(e) => setMinute(e.target.value)}
                  className="time-select"
                >
                  {minutes.map((m) => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                </select>
                <select
                  value={period}
                  onChange={(e) => setPeriod(e.target.value)}
                  className="time-select"
                >
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>

            {/* Categories */}
            <div className="field-group">
              <label className="field-label">
                Categories ({selectedCategories.length} selected)
              </label>
              <div className="chips-grid">
                {CATEGORIES.map(({ label, icon }) => {
                  const isActive = selectedCategories.includes(label);
                  return (
                    <button
                      key={label}
                      type="button"
                      onClick={() => toggleCategory(label)}
                      aria-pressed={isActive}
                      aria-label={`${label} — ${isActive ? "selected, click to remove" : "click to select"}`}
                      className={`chip ${isActive ? "active" : ""}`}
                    >
                      <span className="chip-icon" aria-hidden="true">{icon}</span>
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Submit */}
            <button
              type="button"
              onClick={registerUser}
              disabled={loading}
              className="submit-btn"
            >
              {loading ? "Activating..." : "Activate Alerts →"}
            </button>
          </div>
        </section>

        {/* Features */}
        <div className="features-strip">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <div className="feature-title">Precision Matching</div>
            <div className="feature-desc">
              Our AI filters thousands of postings daily and surfaces only the
              roles that match your exact preferences.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <div className="feature-title">Real-Time Alerts</div>
            <div className="feature-desc">
              Never miss a deadline. Get notified the moment a matching role
              goes live, at the exact time you choose.
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <div className="feature-title">Zero Spam</div>
            <div className="feature-desc">
              One clean digest per day. No re-marketing, no noise — just
              high-signal opportunities worth your attention.
            </div>
          </div>
        </div>

        <hr className="divider" />

        <footer className="footer">
          © {new Date().getFullYear()} JobPulse AI — Built with React &amp; deployed on Vercel
        </footer>
      </div>
    </>
  );
}