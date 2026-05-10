import { useEffect, useState, useRef, useCallback } from "react";
import API from "./api";

// =========================
// DATA
// =========================

const hours = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, "0"));
const minutes = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"];

const CATEGORIES = [
  { label: "BTech",         icon: "🎓" },
  { label: "MTech",         icon: "📘" },
  { label: "MS Research",   icon: "🔬" },
  { label: "Life Sciences", icon: "🧬" },
  { label: "Internships",   icon: "💼" },
  { label: "Remote",        icon: "🌐" },
  { label: "AI/ML",         icon: "🤖" },
  { label: "Cybersecurity", icon: "🔐" },
  { label: "Cloud",         icon: "☁️" },
  { label: "Software",      icon: "💻" },
];

const MARQUEE_ITEMS = [...CATEGORIES, ...CATEGORIES];

// =========================
// APP
// =========================

export default function App() {
  const [email, setEmail]                           = useState("");
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [hour, setHour]                             = useState("09");
  const [minute, setMinute]                         = useState("00");
  const [period, setPeriod]                         = useState("AM");
  const [users, setUsers]                           = useState([]);
  const [message, setMessage]                       = useState({ text: "", type: "" });
  const [emailError, setEmailError]                 = useState("");
  const [loading, setLoading]                       = useState(false);
  const glowRef                                     = useRef(null);

  const selectedTime = `${hour}:${minute} ${period}`;

  // Cursor-follow glow inside form card
  useEffect(() => {
    const el = glowRef.current;
    if (!el) return;
    const move = (e) => {
      const rect = el.getBoundingClientRect();
      el.style.setProperty("--gx", `${e.clientX - rect.left}px`);
      el.style.setProperty("--gy", `${e.clientY - rect.top}px`);
    };
    el.addEventListener("mousemove", move);
    return () => el.removeEventListener("mousemove", move);
  }, []);

  // ---- TOGGLE CATEGORY ----
  const toggleCategory = (category) =>
    setSelectedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((i) => i !== category)
        : [...prev, category]
    );

  // ---- FETCH USERS ----
  const fetchUsers = useCallback(async () => {
    try {
      const res = await API.get("/users");
      setUsers(Array.isArray(res.data) ? res.data : []);
    } catch (e) { console.error("Fetch users error:", e); }
  }, []);

  // ---- REGISTER ----
  const registerUser = async () => {
    if (loading) return;
    setMessage({ text: "", type: "" });
    setEmailError("");

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setEmailError("Please enter a valid email address.");
      return;
    }
    if (selectedCategories.length === 0) {
      setMessage({ text: "Select at least one category.", type: "error" });
      return;
    }

    setLoading(true);
    const timer = setTimeout(() => {
      console.warn("Request timeout safeguard triggered");
      setLoading(false);
      setMessage({ text: "Server timeout. Please try again in a few seconds.", type: "error" });
    }, 15000);

    try {
      const response = await API.post("/register", {
        email,
        categories: selectedCategories,
        delivery_time: selectedTime,
      });
      console.log("Register response:", response.data);
      setMessage({ text: "Alerts activated successfully. Check your inbox.", type: "success" });
      setEmail(""); setSelectedCategories([]);
      setHour("09"); setMinute("00"); setPeriod("AM");
      try { await fetchUsers(); } catch (_) {}
    } catch (error) {
      const detail = error.response?.data?.detail || error.message || "";
      const dup = detail.toLowerCase().includes("already") ||
                  detail.toLowerCase().includes("exist")   ||
                  detail.toLowerCase().includes("registered");
      dup
        ? setEmailError("This email is already registered.")
        : setMessage({ text: detail || "Something went wrong.", type: "error" });
    } finally {
      if (timer) { clearTimeout(timer); }
      setLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      if (mounted) { await fetchUsers(); }
    };
    load();
    return () => { mounted = false; };
  }, []);

  // =========================
  // RENDER
  // =========================
  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html {
          scroll-behavior: smooth;
          scroll-padding-top: 80px;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }
        ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

        :root {
          --bg:          #09090B;
          --bg2:         #0F0F12;
          --neon:        #D2FF00;
          --neon-dim:    rgba(210,255,0,0.09);
          --neon-glow:   rgba(210,255,0,0.25);
          --neon-border: rgba(210,255,0,0.35);
          --surf:        rgba(255,255,255,0.04);
          --surf2:       rgba(255,255,255,0.07);
          --border:      rgba(255,255,255,0.07);
          --text:        #FAFAFA;
          --muted:       #71717A;
          --muted2:      #A1A1AA;
          --red-dim:     rgba(239,68,68,0.1);
          --red-border:  rgba(239,68,68,0.3);
          --r-sm:        8px;
          --r-md:        12px;
          --r-lg:        18px;
          --r-xl:        22px;
        }

        body {
          background: var(--bg);
          color: var(--text);
          font-family: 'Inter', sans-serif;
          font-size: 15px;
          overflow-x: hidden;
          -webkit-font-smoothing: antialiased;
        }

        /* Subtle noise overlay */
        body::after {
          content: '';
          position: fixed; inset: 0;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
          pointer-events: none; z-index: 9999; opacity: 0.35;
        }

        /* Ambient orbs */
        .orb {
          position: fixed; border-radius: 50%;
          filter: blur(130px); pointer-events: none; z-index: 0;
          will-change: transform;
        }
        .orb1 {
          width: 560px; height: 560px; top: -160px; right: -120px;
          background: radial-gradient(circle, rgba(210,255,0,0.07) 0%, transparent 70%);
          animation: fl1 20s ease-in-out infinite alternate;
        }
        .orb2 {
          width: 420px; height: 420px; bottom: 5%; left: -120px;
          background: radial-gradient(circle, rgba(210,255,0,0.04) 0%, transparent 70%);
          animation: fl2 25s ease-in-out infinite alternate;
        }
        @keyframes fl1 { to { transform: translate(-80px,100px) scale(1.1); } }
        @keyframes fl2 { to { transform: translate(100px,-80px) scale(1.15); } }

        /* ======= NAVBAR ======= */
        .nav {
          position: fixed; top: 0; left: 0; right: 0; z-index: 100;
          display: flex; align-items: center; justify-content: space-between;
          height: 62px; padding: 0 48px;
          background: rgba(9,9,11,0.8);
          backdrop-filter: blur(24px) saturate(180%);
          border-bottom: 1px solid var(--border);
        }
        .logo {
          display: flex; align-items: center; gap: 8px;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 17px; font-weight: 700; color: var(--text);
          letter-spacing: -0.3px; text-decoration: none;
        }
        .logo-dot {
          width: 8px; height: 8px; border-radius: 50%;
          background: var(--neon);
          box-shadow: 0 0 12px var(--neon);
          animation: pulse 2.5s ease-in-out infinite;
          flex-shrink: 0;
        }
        @keyframes pulse {
          0%,100% { opacity:1; transform: scale(1); }
          50%      { opacity:0.5; transform: scale(0.85); }
        }
        .nav-links { display: flex; gap: 2px; list-style: none; }
        .nav-links a {
          display: block; padding: 6px 15px; border-radius: 99px;
          color: var(--muted); text-decoration: none; font-size: 14px;
          transition: color .2s, background .2s;
        }
        .nav-links a:hover { color: var(--text); background: var(--surf2); }
        .nav-btn {
          padding: 8px 20px; border-radius: 99px;
          background: var(--neon); color: #09090B;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 13px; font-weight: 700;
          border: none; cursor: pointer; text-decoration: none;
          display: inline-block; letter-spacing: 0.2px;
          transition: box-shadow .2s, transform .2s;
        }
        .nav-btn:hover {
          box-shadow: 0 0 24px var(--neon-glow);
          transform: translateY(-1px);
        }
        @media (max-width: 768px) {
          .nav { padding: 0 20px; }
          .nav-links { display: none; }
        }

        /* ======= PAGE ======= */
        .page { position: relative; z-index: 1; padding-top: 62px; }

        /* ======= HERO ======= */
        .hero {
          max-width: 1280px; margin: 0 auto;
          padding: 90px 48px 70px;
          display: grid;
          grid-template-columns: 1fr 460px;
          gap: 72px; align-items: center;
          min-height: calc(100vh - 62px);
        }
        @media (max-width: 1100px) {
          .hero { grid-template-columns: 1fr; min-height: auto; padding: 48px 20px 40px; gap: 48px; }
        }

        .eyebrow {
          display: inline-flex; align-items: center; gap: 9px;
          padding: 5px 14px 5px 7px; border-radius: 99px;
          border: 1px solid var(--border); background: var(--surf);
          font-size: 12px; color: var(--muted2);
          font-weight: 400; letter-spacing: 0.2px; margin-bottom: 30px;
        }
        .eyebrow-tag {
          padding: 3px 9px; border-radius: 99px;
          background: var(--neon); color: #09090B;
          font-size: 10px; font-weight: 700;
          letter-spacing: 0.6px; text-transform: uppercase;
        }

        h1.ht {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(46px, 5.5vw, 74px);
          font-weight: 700; line-height: 1.03;
          letter-spacing: -3px; color: var(--text); margin-bottom: 22px;
        }
        h1.ht .neon { color: var(--neon); display: block; }

        .hdesc {
          color: var(--muted); font-size: 16px; line-height: 1.75;
          max-width: 500px; margin-bottom: 48px; font-weight: 300;
        }

        .stats {
          display: inline-flex;
          border: 1px solid var(--border);
          border-radius: var(--r-lg); overflow: hidden;
        }
        .si {
          padding: 18px 30px; text-align: center; position: relative;
        }
        .si + .si::before {
          content:''; position: absolute; left:0; top:18%; bottom:18%;
          width:1px; background: var(--border);
        }
        .sv {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 30px; font-weight: 700;
          color: var(--neon); letter-spacing: -1px;
          display: block; margin-bottom: 3px;
        }
        .sl { font-size: 11px; color: var(--muted); white-space: nowrap; font-weight: 400; }

        /* ======= FORM CARD ======= */
        .fcard {
          background: var(--bg2);
          border: 1px solid var(--border);
          border-radius: var(--r-xl);
          padding: 34px 30px;
          position: relative; overflow: hidden;
          --gx: 50%; --gy: 50%;
        }
        /* cursor spotlight */
        .fcard::before {
          content:''; position: absolute; inset:0; pointer-events: none;
          background: radial-gradient(280px circle at var(--gx) var(--gy), rgba(210,255,0,0.055) 0%, transparent 70%);
          border-radius: inherit;
        }
        /* top shimmer */
        .fcard::after {
          content:''; position: absolute; top:0; left:8%; right:8%; height:1px;
          background: linear-gradient(90deg, transparent, var(--neon-border), transparent);
        }

        .ftitle {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 21px; font-weight: 700;
          letter-spacing: -0.4px; margin-bottom: 4px;
        }
        .fsub { font-size: 13px; color: var(--muted); margin-bottom: 26px; font-weight: 300; }

        /* Fields */
        .field { margin-bottom: 18px; }
        .flbl {
          display: flex; justify-content: space-between; align-items: center;
          font-size: 11px; font-weight: 600; letter-spacing: 0.7px;
          text-transform: uppercase; color: var(--muted); margin-bottom: 8px;
        }
        .flbl-count {
          font-size: 11px; color: var(--neon);
          background: var(--neon-dim); padding: 2px 8px;
          border-radius: 99px; font-weight: 600;
          letter-spacing: 0.2px; text-transform: none;
        }

        .inp {
          width: 100%; background: rgba(0,0,0,0.35);
          border: 1px solid var(--border); border-radius: var(--r-md);
          padding: 11px 15px; color: var(--text);
          font-family: 'Inter', sans-serif; font-size: 14px;
          outline: none; transition: border-color .2s, box-shadow .2s;
        }
        .inp::placeholder { color: rgba(113,113,122,0.45); }
        .inp:focus {
          border-color: var(--neon-border);
          box-shadow: 0 0 0 3px rgba(210,255,0,0.07);
        }
        .inp.err { border-color: rgba(239,68,68,0.5); }
        .inp.err:focus { box-shadow: 0 0 0 3px var(--red-dim); }

        .ferr {
          display: flex; align-items: center; gap: 6px;
          margin-top: 7px; padding: 8px 12px;
          background: var(--red-dim); border: 1px solid var(--red-border);
          border-radius: var(--r-sm); color: #FCA5A5; font-size: 12px;
          animation: sd .2s ease;
        }
        @keyframes sd { from { opacity:0; transform:translateY(-5px); } to { opacity:1; transform:translateY(0); } }

        .trow { display: flex; gap: 8px; }
        .sel {
          flex: 1; background: rgba(0,0,0,0.35);
          border: 1px solid var(--border); border-radius: var(--r-md);
          padding: 11px 8px; color: var(--text);
          font-family: 'Inter', sans-serif; font-size: 14px;
          outline: none; cursor: pointer; text-align: center;
          appearance: none; transition: border-color .2s;
        }
        .sel:focus { border-color: var(--neon-border); }
        .sel option { background: #0F0F12; }

        .chips { display: flex; flex-wrap: wrap; gap: 6px; }
        .chip {
          display: inline-flex; align-items: center; gap: 5px;
          padding: 6px 13px; border-radius: 99px;
          border: 1px solid var(--border); background: transparent;
          color: var(--muted2); font-family: 'Inter', sans-serif;
          font-size: 12px; font-weight: 500; cursor: pointer;
          transition: border-color .15s, background .15s, color .15s, transform .1s;
          user-select: none; outline: none;
          -webkit-tap-highlight-color: transparent; letter-spacing: 0.1px;
        }
        .chip:hover { border-color: rgba(210,255,0,0.3); color: var(--text); background: var(--neon-dim); }
        .chip:focus-visible { border-color: var(--neon); box-shadow: 0 0 0 2px rgba(210,255,0,0.15); }
        .chip:active { transform: scale(0.94); }
        .chip.on { background: var(--neon-dim); border-color: var(--neon-border); color: var(--neon); }
        .chip.on:hover { background: rgba(210,255,0,0.14); }
        .ci { font-size: 13px; line-height: 1; }

        .banner {
          padding: 10px 13px; border-radius: var(--r-sm);
          font-size: 13px; font-weight: 500;
          margin-bottom: 16px; animation: sd .2s ease;
        }
        .banner.error { background: var(--red-dim); border: 1px solid var(--red-border); color: #FCA5A5; }
        .banner.success { background: var(--neon-dim); border: 1px solid var(--neon-border); color: var(--neon); }

        .sbtn {
          width: 100%; padding: 13px; margin-top: 6px;
          border-radius: var(--r-md); border: none;
          background: var(--neon); color: #09090B;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 14px; font-weight: 700; letter-spacing: 0.3px;
          cursor: pointer; position: relative; overflow: hidden;
          transition: box-shadow .2s, transform .2s, opacity .2s;
        }
        .sbtn::after {
          content:''; position: absolute; inset:0;
          background: linear-gradient(135deg,rgba(255,255,255,0.15),transparent);
          opacity:0; transition: opacity .2s;
        }
        .sbtn:hover:not(:disabled)::after { opacity:1; }
        .sbtn:hover:not(:disabled) { box-shadow: 0 6px 32px var(--neon-glow); transform: translateY(-1px); }
        .sbtn:active:not(:disabled) { transform: translateY(0); }
        .sbtn:disabled { opacity: 0.52; cursor: not-allowed; }

        .spin {
          display: inline-block; width: 13px; height: 13px;
          border: 2px solid rgba(9,9,11,0.3); border-top-color: #09090B;
          border-radius: 50%; animation: sp .7s linear infinite;
          margin-right: 8px; vertical-align: middle;
        }
        @keyframes sp { to { transform: rotate(360deg); } }

        /* ======= MARQUEE ======= */
        .mq {
          position: relative; z-index: 1;
          border-top: 1px solid var(--border);
          border-bottom: 1px solid var(--border);
          padding: 22px 0; overflow: hidden;
          background: linear-gradient(180deg, transparent, rgba(210,255,0,0.015), transparent);
        }
        .mq::before, .mq::after {
          content:''; position: absolute; top:0; bottom:0; width:180px; z-index:2; pointer-events:none;
        }
        .mq::before { left:0; background: linear-gradient(90deg, var(--bg), transparent); }
        .mq::after  { right:0; background: linear-gradient(270deg, var(--bg), transparent); }
        .mq-track {
          display: flex; gap: 10px; width: max-content;
          animation: mq 30s linear infinite;
          will-change: transform;
        }
        .mq-track:hover { animation-play-state: paused; }
        @keyframes mq { to { transform: translateX(-50%); } }
        .mq-pill {
          display: inline-flex; align-items: center; gap: 7px;
          padding: 7px 16px; border-radius: 99px;
          border: 1px solid var(--border); background: var(--surf);
          font-size: 12px; color: var(--muted2); font-weight: 500; white-space: nowrap;
        }
        .mq-pill span { font-size: 13px; }

        /* ======= FEATURES ======= */
        .fsec {
          max-width: 1280px; margin: 0 auto; padding: 88px 48px;
        }
        @media (max-width: 768px) { .fsec { padding: 52px 20px; } }

        .sec-eye {
          display: inline-flex; align-items: center; gap: 10px;
          font-size: 11px; font-weight: 700; letter-spacing: 1.2px;
          text-transform: uppercase; color: var(--neon); margin-bottom: 14px;
        }
        .sec-eye::before {
          content:''; display: inline-block;
          width: 22px; height: 2px; background: var(--neon); border-radius: 2px;
        }
        .sec-title {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(28px, 3.5vw, 44px); font-weight: 700;
          letter-spacing: -1.8px; line-height: 1.12;
          margin-bottom: 52px; color: var(--text);
        }

        .fgrid {
          display: grid; grid-template-columns: repeat(3,1fr); gap: 14px;
        }
        @media (max-width: 900px) { .fgrid { grid-template-columns: 1fr; } }

        .fc {
          background: var(--bg2); border: 1px solid var(--border);
          border-radius: var(--r-xl); padding: 30px 28px;
          position: relative; overflow: hidden;
          transition: border-color .25s, background .25s, transform .25s;
        }
        .fc::after {
          content:''; position: absolute; bottom:0; left:0; right:0; height:2px;
          background: var(--neon); transform: scaleX(0); transform-origin: left;
          transition: transform .3s ease; border-radius: 0 0 var(--r-xl) var(--r-xl);
        }
        .fc:hover { border-color: rgba(210,255,0,0.15); background: rgba(210,255,0,0.02); transform: translateY(-3px); }
        .fc:hover::after { transform: scaleX(1); }

        .fc-num {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 10px; font-weight: 700;
          letter-spacing: 2px; color: var(--neon);
          opacity: 0.55; margin-bottom: 18px; display: block;
        }
        .fc-ico { font-size: 30px; display: block; margin-bottom: 14px; line-height: 1; }
        .fc-title {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 16px; font-weight: 700;
          letter-spacing: -0.3px; margin-bottom: 9px; color: var(--text);
        }
        .fc-desc { font-size: 13px; color: var(--muted); line-height: 1.7; font-weight: 300; }

        /* ======= FOOTER ======= */
        .footer {
          position: relative; z-index: 1;
          border-top: 1px solid var(--border);
          padding: 26px 48px;
          display: flex; align-items: center; justify-content: space-between;
        }
        .flogo {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 14px; font-weight: 700; color: var(--text);
          display: flex; align-items: center; gap: 7px;
        }
        .fdot { width: 6px; height: 6px; border-radius: 50%; background: var(--neon); }
        .fcopy { font-size: 12px; color: var(--muted); }
        @media (max-width: 600px) {
          .footer { flex-direction: column; gap: 8px; padding: 20px; text-align: center; }
        }
      `}</style>

      {/* Ambient */}
      <div className="orb orb1" />
      <div className="orb orb2" />

      {/* ===== NAVBAR ===== */}
      <nav className="nav">
        <a href="#" className="logo">
          <span className="logo-dot" />
          JobPulse AI
        </a>
        <ul className="nav-links">
          <li><a href="#features">Features</a></li>
          <li><a href="#categories">Categories</a></li>
          <li><a href="#register">Alerts</a></li>
        </ul>
        <a href="#register" className="nav-btn">Get Alerts →</a>
      </nav>

      <div className="page">

        {/* ===== HERO ===== */}
        <section className="hero">

          {/* Left */}
          <div>
            <div className="eyebrow">
              <span className="eyebrow-tag">New</span>
              AI-Powered Job Intelligence Platform
            </div>

            <h1 className="ht">
              Never Miss<br />The Right
              <span className="neon">Opportunity.</span>
            </h1>

            <p className="hdesc">
              Curated job alerts for BTech, MTech, research, internships,
              remote roles and more — filtered by AI, delivered to your
              inbox at exactly the time you choose.
            </p>

            <div className="stats">
              <div className="si">
                <span className="sv">{users.length}</span>
                <span className="sl">Active Users</span>
              </div>
              <div className="si">
                <span className="sv">24/7</span>
                <span className="sl">Monitoring</span>
              </div>
              <div className="si">
                <span className="sv">10+</span>
                <span className="sl">Categories</span>
              </div>
            </div>
          </div>

          {/* Right — form */}
          <div className="fcard" id="register" ref={glowRef}>

            <div className="ftitle">Start Getting Alerts</div>
            <div className="fsub">Free · No spam · Unsubscribe anytime</div>

            {/* Banner */}
            {message.text && (
              <div
                className={`banner ${message.type}`}
                role={message.type === "error" ? "alert" : "status"}
                aria-live={message.type === "error" ? "assertive" : "polite"}
              >
                {message.text}
              </div>
            )}

            {/* Email */}
            <div className="field">
              <div className="flbl">Email Address</div>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setEmailError(""); }}
                className={`inp ${emailError ? "err" : ""}`}
              />
              {emailError && <div className="ferr">⚠ {emailError}</div>}
            </div>

            {/* Delivery Time */}
            <div className="field">
              <div className="flbl">Daily Delivery Time</div>
              <div className="trow">
                <select value={hour} onChange={(e) => setHour(e.target.value)} className="sel">
                  {hours.map((h) => <option key={h} value={h}>{h}</option>)}
                </select>
                <select value={minute} onChange={(e) => setMinute(e.target.value)} className="sel">
                  {minutes.map((m) => <option key={m} value={m}>{m}</option>)}
                </select>
                <select value={period} onChange={(e) => setPeriod(e.target.value)} className="sel">
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>

            {/* Categories */}
            <div className="field" id="categories">
              <div className="flbl">
                Job Categories
                {selectedCategories.length > 0 && (
                  <span className="flbl-count">{selectedCategories.length} selected</span>
                )}
              </div>
              <div className="chips">
                {CATEGORIES.map(({ label, icon }) => {
                  const on = selectedCategories.includes(label);
                  return (
                    <button
                      key={label}
                      type="button"
                      onClick={() => toggleCategory(label)}
                      aria-pressed={on}
                      aria-label={`${label} — ${on ? "selected, click to remove" : "click to select"}`}
                      className={`chip ${on ? "on" : ""}`}
                    >
                      <span className="ci" aria-hidden="true">{icon}</span>
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Submit */}
            <button type="button" onClick={registerUser} disabled={loading} className="sbtn">
              {loading
                ? <><span className="spin" />Activating...</>
                : "Activate My Alerts →"
              }
            </button>

          </div>
        </section>

        {/* ===== MARQUEE ===== */}
        <div className="mq">
          <div className="mq-track">
            {MARQUEE_ITEMS.map(({ label, icon }, i) => (
              <div className="mq-pill" key={`${label}-${i}`}>
                <span>{icon}</span>{label}
              </div>
            ))}
          </div>
        </div>

        {/* ===== FEATURES ===== */}
        <section className="fsec" id="features">
          <div className="sec-eye">Why JobPulse</div>
          <h2 className="sec-title">
            Built different.<br />Designed for you.
          </h2>
          <div className="fgrid">
            <div className="fc">
              <span className="fc-num">01</span>
              <span className="fc-ico">🎯</span>
              <div className="fc-title">Precision Matching</div>
              <p className="fc-desc">AI scans thousands of postings daily and surfaces only roles that match your exact categories — zero noise.</p>
            </div>
            <div className="fc">
              <span className="fc-num">02</span>
              <span className="fc-ico">⚡</span>
              <div className="fc-title">You Set the Time</div>
              <p className="fc-desc">Pick your exact delivery time. Morning briefing or evening review — alerts arrive when you actually check email.</p>
            </div>
            <div className="fc">
              <span className="fc-num">03</span>
              <span className="fc-ico">🔒</span>
              <div className="fc-title">Zero Spam Guarantee</div>
              <p className="fc-desc">One clean digest per day. No re-marketing, no upsells — just high-signal opportunities worth your attention.</p>
            </div>
          </div>
        </section>

        {/* ===== FOOTER ===== */}
        <footer className="footer">
          <div className="flogo">
            <span className="fdot" />
            JobPulse AI
          </div>
          <span className="fcopy">
            © {new Date().getFullYear()} — Azure · Vercel
          </span>
        </footer>

      </div>
    </>
  );
}