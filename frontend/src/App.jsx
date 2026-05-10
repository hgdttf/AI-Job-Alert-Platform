import { useEffect, useState, useRef, useCallback } from "react";
import API from "./api";

// ─────────────────────────────────────────────
// CONSTANTS  (global — never recreated)
// ─────────────────────────────────────────────

const HOURS   = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, "0"));
const MINUTES = ["00","05","10","15","20","25","30","35","40","45","50","55"];

const CATEGORIES = [
  { label: "BTech",          icon: "🎓" },
  { label: "MTech",          icon: "📘" },
  { label: "MS Research",    icon: "🔬" },
  { label: "Life Sciences",  icon: "🧬" },
  { label: "Internships",    icon: "💼" },
  { label: "Remote",         icon: "🌐" },
  { label: "AI / ML",        icon: "🤖" },
  { label: "Cybersecurity",  icon: "🔐" },
  { label: "Cloud",          icon: "☁️" },
  { label: "Software",       icon: "💻" },
];

// 2× for seamless translateX(-50%) marquee loop
const MARQUEE_ITEMS = [...CATEGORIES, ...CATEGORIES];

// ─────────────────────────────────────────────
// APP
// ─────────────────────────────────────────────

export default function App() {
  const [email,              setEmail]              = useState("");
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [hour,               setHour]               = useState("09");
  const [minute,             setMinute]             = useState("00");
  const [period,             setPeriod]             = useState("AM");
  const [users,              setUsers]              = useState([]);
  const [message,            setMessage]            = useState({ text: "", type: "" });
  const [emailError,         setEmailError]         = useState("");
  const [loading,            setLoading]            = useState(false);
  const loadingRef = useRef(false);
  const pollRef = useRef(null);
  const cardRef = useRef(null);

  // keep loadingRef in sync with loading state for staged timers
  useEffect(() => { loadingRef.current = loading; }, [loading]);

  const selectedTime = `${hour}:${minute} ${period}`;

  // ── cursor-follow spotlight on form card ──
  useEffect(() => {
    const el = cardRef.current;
    if (!el) return;
    const onMove = (e) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", `${e.clientX - r.left}px`);
      el.style.setProperty("--my", `${e.clientY - r.top}px`);
    };
    el.addEventListener("mousemove", onMove);
    return () => el.removeEventListener("mousemove", onMove);
  }, []);

  // ── fetch users ──
  const fetchUsers = useCallback(async (retries = 2) => {
    try {
      const res = await API.get("/users");
      setUsers(Array.isArray(res.data) ? res.data : []);
    } catch (e) {
      console.error("Fetch users error:", e);
      if (retries > 0) {
        setTimeout(() => fetchUsers(retries - 1), 1500 * (3 - retries));
      }
      // preserve existing users on error — don't zero out stats
    }
  }, []);

  // ── on mount ──
  useEffect(() => {
    let mounted = true;
    (async () => { if (mounted) await fetchUsers(); })();
    return () => { mounted = false; };
  }, [fetchUsers]);

  // ── toggle category ──
  const toggleCategory = useCallback((cat) =>
    setSelectedCategories((prev) => {
      const set = new Set(prev);
      if (set.has(cat)) set.delete(cat); else set.add(cat);
      return Array.from(set);
    }), []);

  // ── robust error parser ──
  const parseApiError = (err) => {
    if (!err) return "Something went wrong. Please try again.";
    if (typeof err === "string") return err;
    // Axios / fetch-style structured errors
    const data = err.response?.data;
    if (data) {
      if (typeof data.detail === "string" && data.detail.trim()) return data.detail;
      if (Array.isArray(data.detail)) {
        return data.detail.map((d) =>
          typeof d === "string" ? d : d.msg || JSON.stringify(d)
        ).join(". ");
      }
      if (typeof data.message === "string" && data.message.trim()) return data.message;
    }
    if (err.code === "ECONNABORTED" || err.message === "Network Error")
      return "Connection failed. Please check your internet and try again.";
    if (typeof err.message === "string" && err.message.trim()) return err.message;
    return "Something went wrong. Please try again.";
  };

  // ── background polling for user count ──
  const startPollingUsers = () => {
    if (pollRef.current) clearInterval(pollRef.current);
    let attempts = 0;
    pollRef.current = setInterval(() => {
      attempts++;
      fetchUsers().catch(() => {});
      if (attempts >= 5) {          // poll 5 times over 15s then stop
        clearInterval(pollRef.current);
        pollRef.current = null;
      }
    }, 3000);
  };

  // cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  // ── register ──
  const registerUser = async () => {
    if (loading) return;                        // double-click guard

    setMessage({ text: "", type: "" });
    setEmailError("");

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      setEmailError("Please enter a valid email address.");
      return;
    }
    if (selectedCategories.length === 0) {
      setMessage({ text: "Select at least one category to continue.", type: "error" });
      return;
    }

    setLoading(true);
    setMessage({ text: "", type: "" });

    // staged loading messages — makes wait feel intentional, not broken
    const stageTimers = [];
    stageTimers.push(setTimeout(() => {
      if (loadingRef.current) setMessage({ text: "Saving your preferences...", type: "" });
    }, 1500));
    stageTimers.push(setTimeout(() => {
      if (loadingRef.current) setMessage({ text: "Preparing your first alert...", type: "" });
    }, 5000));
    stageTimers.push(setTimeout(() => {
      if (loadingRef.current) setMessage({ text: "Sending welcome email (this may take a moment)...", type: "" });
    }, 9000));

    // safety net — always unlocks UI after 12 s
    const timer = setTimeout(() => {
      console.warn("Request timeout safeguard triggered");
      setLoading(false);
      stageTimers.forEach(clearTimeout);
      setMessage({ text: "Server timeout. Please try again in a few seconds.", type: "error" });
    }, 20000);

    try {
      const response = await API.post("/register", {
        email,
        categories:    selectedCategories,
        delivery_time: selectedTime,
      });
      console.log("Register response:", response.data);

      setMessage({ text: "Alerts activated successfully.", type: "success" });
      setEmail("");
      setSelectedCategories([]);
      setHour("09"); setMinute("00"); setPeriod("AM");
      // refresh stats in background — don't block success UI
      fetchUsers().catch(() => {});

    } catch (error) {
      const detail = parseApiError(error);
      const isTimeout = detail.toLowerCase().includes("timeout") || detail.toLowerCase().includes("busy");
      const isDuplicate =
        detail.toLowerCase().includes("already") ||
        detail.toLowerCase().includes("exist")   ||
        detail.toLowerCase().includes("registered");

      if (isDuplicate) {
        setEmailError("This email is already registered.");
      } else if (isTimeout) {
        // optimistic: backend likely still processing the slow email
        setMessage({ text: "Registration accepted — check your inbox shortly.", type: "success" });
        setEmail("");
        setSelectedCategories([]);
        setHour("09"); setMinute("00"); setPeriod("AM");
        startPollingUsers();
      } else {
        setMessage({ text: detail, type: "error" });
      }
    } finally {
      if (timer) clearTimeout(timer);
      stageTimers.forEach(clearTimeout);
      setLoading(false);                        // always runs
    }
  };

  // ─────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────
  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

        /* ── reset ── */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html {
          scroll-behavior: smooth;
          scroll-padding-top: 80px;         /* offset for fixed nav */
        }

        /* ── tokens ── */
        :root {
          --bg:         #080809;
          --bg-card:    #0E0E11;
          --bg-input:   rgba(0,0,0,0.4);
          --neon:       #D2FF00;
          --neon-10:    rgba(210,255,0,0.10);
          --neon-18:    rgba(210,255,0,0.18);
          --neon-30:    rgba(210,255,0,0.30);
          --neon-glow:  rgba(210,255,0,0.22);
          --border:     rgba(255,255,255,0.07);
          --border-hi:  rgba(255,255,255,0.12);
          --text:       #F2F2F3;
          --text-2:     #A1A1AA;
          --text-3:     #52525B;
          --red:        rgba(255,80,80,0.9);
          --red-10:     rgba(255,80,80,0.10);
          --red-30:     rgba(255,80,80,0.30);
          --r-sm:       8px;
          --r-md:       12px;
          --r-lg:       16px;
          --r-xl:       20px;
          --ease:       cubic-bezier(0.22,1,0.36,1);
        }

        /* ── base ── */
        body {
          background: var(--bg);
          color: var(--text);
          font-family: 'Inter', system-ui, sans-serif;
          font-size: 15px;
          line-height: 1.6;
          overflow-x: hidden;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }

        /* ── custom scrollbar ── */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 99px; }
        ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

        /* ── dot-grid background (Linear/Raycast inspired — NOT a blob) ── */
        .dot-grid {
          position: fixed; inset: 0; z-index: 0; pointer-events: none;
          background-image: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px);
          background-size: 28px 28px;
          mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
          -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
        }

        /* ── single subtle neon vignette top-right ── */
        .vignette {
          position: fixed; z-index: 0; pointer-events: none;
          top: -200px; right: -150px;
          width: 700px; height: 700px; border-radius: 50%;
          background: radial-gradient(circle, rgba(210,255,0,0.05) 0%, transparent 65%);
          filter: blur(60px);
          will-change: transform;
        }

        /* ── NAVBAR ── */
        .nav {
          position: fixed; top: 0; left: 0; right: 0; z-index: 200;
          height: 60px;
          display: flex; align-items: center; justify-content: space-between;
          padding: 0 40px;
          background: rgba(8,8,9,0.82);
          backdrop-filter: blur(20px) saturate(160%);
          border-bottom: 1px solid var(--border);
        }

        .nav-logo {
          display: flex; align-items: center; gap: 9px;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 16px; font-weight: 700;
          color: var(--text); text-decoration: none;
          letter-spacing: -0.3px;
        }
        /* pulsing live dot — signals the service is running */
        .live-dot {
          position: relative;
          width: 8px; height: 8px; border-radius: 50%;
          background: var(--neon);
          box-shadow: 0 0 8px var(--neon);
        }
        .live-dot::after {
          content: '';
          position: absolute; inset: -3px; border-radius: 50%;
          border: 1.5px solid var(--neon);
          opacity: 0;
          animation: ripple 2.4s ease-out infinite;
        }
        @keyframes ripple {
          0%   { transform: scale(0.6); opacity: 0.7; }
          100% { transform: scale(2);   opacity: 0; }
        }

        .nav-center { display: flex; gap: 2px; list-style: none; }
        .nav-center a {
          display: block; padding: 6px 14px; border-radius: 99px;
          color: var(--text-2); text-decoration: none;
          font-size: 13.5px; font-weight: 500;
          transition: color .18s, background .18s;
        }
        .nav-center a:hover { color: var(--text); background: rgba(255,255,255,0.05); }

        .nav-cta {
          padding: 8px 18px; border-radius: 99px;
          background: var(--neon); color: #080809;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 13px; font-weight: 700; letter-spacing: 0.1px;
          border: none; cursor: pointer;
          text-decoration: none; display: inline-block;
          transition: box-shadow .25s var(--ease), transform .2s var(--ease), filter .2s;
        }
        .nav-cta:hover {
          box-shadow: 0 0 28px var(--neon-glow);
          transform: translateY(-1px);
          filter: brightness(1.07);
        }
        .nav-cta:active { transform: none; transition: none; }

        @media (max-width: 700px) {
          .nav { padding: 0 20px; }
          .nav-center { display: none; }
        }

        /* ── PAGE ── */
        .page { position: relative; z-index: 1; padding-top: 60px; }

        /* ── HERO ── */
        .hero {
          max-width: 1200px; margin: 0 auto;
          padding: 88px 40px 72px;
          display: grid;
          grid-template-columns: 1fr 448px;
          gap: 64px; align-items: center;
          min-height: calc(100vh - 60px);
        }
        @media (max-width: 1040px) {
          .hero {
            grid-template-columns: 1fr;
            min-height: auto;
            padding: 56px 20px 48px;
            gap: 48px;
          }
        }

        /* eyebrow */
        .eyebrow {
          display: inline-flex; align-items: center; gap: 8px;
          padding: 5px 13px 5px 6px; border-radius: 99px;
          border: 1px solid var(--border);
          background: rgba(255,255,255,0.025);
          font-size: 12px; color: var(--text-2);
          font-weight: 500; letter-spacing: 0.2px;
          margin-bottom: 26px;
        }
        .eyebrow-badge {
          padding: 2px 9px; border-radius: 99px;
          background: var(--neon); color: #080809;
          font-size: 10px; font-weight: 800;
          letter-spacing: 0.8px; text-transform: uppercase;
        }

        /* headline */
        h1.headline {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(44px, 5.5vw, 70px);
          font-weight: 700; line-height: 1.04;
          letter-spacing: -3px; color: var(--text);
          margin-bottom: 20px;
        }
        h1.headline .hl { color: var(--neon); display: block; }

        .hero-desc {
          color: var(--text-2); font-size: 16px; line-height: 1.75;
          max-width: 460px; margin-bottom: 40px;
          font-weight: 400;
        }

        /* stats strip */
        .stats {
          display: inline-flex;
          border: 1px solid var(--border);
          border-radius: var(--r-lg); overflow: hidden;
        }
        .stat {
          padding: 16px 28px; text-align: center; position: relative;
        }
        .stat + .stat::before {
          content: ''; position: absolute; left: 0; top: 18%; bottom: 18%;
          width: 1px; background: var(--border);
        }
        .stat-val {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 26px; font-weight: 700;
          color: var(--neon); letter-spacing: -0.8px;
          display: block; margin-bottom: 3px;
          font-variant-numeric: tabular-nums;
        }
        /* live pulse on user count */
        .stat-val.live {
          animation: count-glow 3s ease-in-out infinite alternate;
        }
        @keyframes count-glow {
          from { text-shadow: none; }
          to   { text-shadow: 0 0 16px var(--neon-30); }
        }
        .stat-lbl {
          font-size: 11px; color: var(--text-3);
          white-space: nowrap; font-weight: 500; letter-spacing: 0.4px;
          text-transform: uppercase;
        }

        /* ── FORM CARD ── */
        .fcard {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: var(--r-xl);
          padding: 32px 28px;
          position: relative; overflow: hidden;
          /* cursor spotlight vars */
          --mx: 50%; --my: 50%;
          transition: border-color .3s var(--ease);
        }
        .fcard:hover { border-color: var(--border-hi); }

        /* cursor spotlight — premium feel from Raycast/Linear cards */
        .fcard::before {
          content: ''; position: absolute; inset: 0;
          border-radius: inherit; pointer-events: none;
          background: radial-gradient(
            260px circle at var(--mx) var(--my),
            rgba(210,255,0,0.045) 0%, transparent 70%
          );
        }

        /* top specular line — Raycast-style border highlight */
        .fcard::after {
          content: ''; position: absolute;
          top: 0; left: 12%; right: 12%; height: 1px;
          background: linear-gradient(90deg, transparent, rgba(210,255,0,0.28), transparent);
          border-radius: 99px;
        }

        .f-title {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 20px; font-weight: 700;
          letter-spacing: -0.4px; margin-bottom: 4px;
        }
        .f-sub {
          font-size: 13px; color: var(--text-3);
          margin-bottom: 24px; font-weight: 400;
        }

        /* ── fields ── */
        .field { margin-bottom: 18px; }

        .f-label {
          display: flex; justify-content: space-between; align-items: center;
          font-size: 11px; font-weight: 600;
          letter-spacing: 0.8px; text-transform: uppercase;
          color: var(--text-3); margin-bottom: 8px;
        }
        .f-count {
          font-size: 11px; color: var(--neon);
          background: var(--neon-10); padding: 2px 8px;
          border-radius: 99px; font-weight: 700;
          letter-spacing: 0.2px; text-transform: none;
        }

        .inp {
          width: 100%;
          background: var(--bg-input);
          border: 1px solid var(--border);
          border-radius: var(--r-md);
          padding: 11px 14px;
          color: var(--text);
          font-family: 'Inter', sans-serif; font-size: 14px;
          outline: none;
          transition: border-color .18s, box-shadow .18s;
          /* prevent iOS zoom */
          font-size: max(14px, 1em);
        }
        .inp::placeholder { color: var(--text-3); opacity: 0.7; }
        .inp:focus {
          border-color: var(--neon-30);
          box-shadow: 0 0 0 3px rgba(210,255,0,0.07);
        }
        .inp.err { border-color: var(--red-30); }
        .inp.err:focus { box-shadow: 0 0 0 3px var(--red-10); }

        /* inline field error */
        .f-err {
          display: flex; align-items: center; gap: 7px;
          margin-top: 8px; padding: 9px 13px;
          background: var(--red-10); border: 1px solid var(--red-30);
          border-radius: var(--r-sm);
          color: #FF9F9A; font-size: 12px; font-weight: 500;
          animation: fadeUp .2s var(--ease);
        }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(-4px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        /* time selects */
        .time-row { display: flex; gap: 8px; }
        .sel {
          flex: 1;
          background: var(--bg-input);
          border: 1px solid var(--border);
          border-radius: var(--r-md);
          padding: 11px 8px;
          color: var(--text);
          font-family: 'Inter', sans-serif; font-size: 14px;
          outline: none; cursor: pointer;
          text-align: center; appearance: none;
          transition: border-color .18s;
        }
        .sel:focus { border-color: var(--neon-30); }
        .sel option { background: #0E0E11; color: var(--text); }

        /* category chips */
        .chips { display: flex; flex-wrap: wrap; gap: 7px; }
        .chip {
          display: inline-flex; align-items: center; gap: 5px;
          padding: 6px 13px; border-radius: 99px;
          border: 1px solid var(--border);
          background: transparent;
          color: var(--text-2);
          font-family: 'Inter', sans-serif;
          font-size: 12.5px; font-weight: 500;
          cursor: pointer; user-select: none;
          outline: none; -webkit-tap-highlight-color: transparent;
          transition: border-color .15s, background .15s, color .15s, transform .1s;
          letter-spacing: 0.1px;
        }
        .chip:hover {
          border-color: var(--neon-30); color: var(--text);
          background: var(--neon-10);
        }
        .chip:focus-visible {
          border-color: var(--neon); box-shadow: 0 0 0 2px rgba(210,255,0,0.14);
        }
        .chip:active { transform: scale(0.94); transition: transform .05s; }
        .chip.on { background: var(--neon-10); border-color: var(--neon-30); color: var(--neon); }
        .chip.on:hover { background: var(--neon-18); }
        .chip-icon { font-size: 13px; line-height: 1; }

        /* status banner */
        .banner {
          display: flex; align-items: center; gap: 8px;
          padding: 10px 14px; border-radius: var(--r-sm);
          font-size: 13px; font-weight: 500;
          margin-bottom: 18px;
          animation: fadeUp .2s var(--ease);
        }
        .banner.error {
          background: var(--red-10); border: 1px solid var(--red-30); color: #FFB3AF;
        }
        .banner.success {
          background: var(--neon-10); border: 1px solid var(--neon-30); color: var(--neon);
        }
        .banner-icon { font-size: 14px; flex-shrink: 0; }

        /* submit button */
        .sbtn {
          width: 100%; padding: 13px;
          margin-top: 6px; border-radius: var(--r-md);
          border: none;
          background: var(--neon); color: #080809;
          font-family: 'Space Grotesk', sans-serif;
          font-size: 14px; font-weight: 700; letter-spacing: 0.2px;
          cursor: pointer; position: relative; overflow: hidden;
          transition: box-shadow .25s var(--ease), transform .2s var(--ease), filter .2s;
          /* sheen layer */
        }
        .sbtn::before {
          content: '';
          position: absolute; inset: 0;
          background: linear-gradient(135deg, rgba(255,255,255,0.18) 0%, transparent 55%);
          opacity: 0; transition: opacity .25s;
        }
        .sbtn:hover:not(:disabled)::before { opacity: 1; }
        .sbtn:hover:not(:disabled) {
          box-shadow: 0 6px 32px var(--neon-glow);
          transform: translateY(-1px); filter: brightness(1.06);
        }
        /* instant press feedback — no transition delay */
        .sbtn:active:not(:disabled) {
          transform: scale(0.98);
          transition: transform .05s, box-shadow .05s;
          box-shadow: none;
        }
        .sbtn:disabled { opacity: 0.48; cursor: not-allowed; filter: grayscale(0.3); }

        /* loading spinner inside button */
        .spin {
          display: inline-block; width: 13px; height: 13px;
          border: 2px solid rgba(8,8,9,0.25); border-top-color: #080809;
          border-radius: 50%;
          animation: spin .65s linear infinite;
          margin-right: 8px; vertical-align: middle;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* ── MARQUEE ── */
        .mq {
          position: relative; z-index: 1;
          padding: 22px 0; overflow: hidden;
          border-top: 1px solid var(--border);
          border-bottom: 1px solid var(--border);
        }
        /* fade edges */
        .mq::before, .mq::after {
          content: ''; position: absolute; top: 0; bottom: 0; width: 160px;
          z-index: 2; pointer-events: none;
        }
        .mq::before { left: 0;  background: linear-gradient(90deg,  var(--bg), transparent); }
        .mq::after  { right: 0; background: linear-gradient(270deg, var(--bg), transparent); }

        .mq-track {
          display: flex; gap: 10px; width: max-content;
          animation: marquee 32s linear infinite;
          will-change: transform;
        }
        .mq-track:hover { animation-play-state: paused; }
        @keyframes marquee { to { transform: translateX(-50%); } }

        .mq-pill {
          display: inline-flex; align-items: center; gap: 7px;
          padding: 7px 16px; border-radius: 99px;
          border: 1px solid var(--border);
          background: rgba(255,255,255,0.02);
          font-size: 12.5px; color: var(--text-2);
          font-weight: 500; white-space: nowrap;
          transition: border-color .2s, background .2s;
        }
        .mq-pill:hover { border-color: var(--border-hi); background: rgba(255,255,255,0.04); }
        .mq-pill-icon { font-size: 13px; }

        /* ── FEATURES ── */
        .features {
          max-width: 1200px; margin: 0 auto; padding: 88px 40px;
        }
        @media (max-width: 700px) { .features { padding: 60px 20px; } }

        .sec-label {
          display: inline-flex; align-items: center; gap: 10px;
          font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
          text-transform: uppercase; color: var(--neon);
          margin-bottom: 14px;
        }
        .sec-label::before {
          content: ''; display: inline-block;
          width: 20px; height: 1.5px;
          background: var(--neon); border-radius: 2px;
        }

        .sec-title {
          font-family: 'Space Grotesk', sans-serif;
          font-size: clamp(28px, 3.5vw, 44px);
          font-weight: 700; letter-spacing: -1.8px;
          line-height: 1.12; margin-bottom: 48px; color: var(--text);
        }

        /* 3-col grid */
        .feat-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 14px;
        }
        @media (max-width: 900px) { .feat-grid { grid-template-columns: 1fr; } }

        .feat-card {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: var(--r-xl); padding: 28px 26px;
          position: relative; overflow: hidden;
          display: flex; flex-direction: column;
          transition: border-color .28s var(--ease), transform .28s var(--ease), background .28s;
          cursor: default;
        }
        /* bottom neon reveal on hover */
        .feat-card::after {
          content: ''; position: absolute; bottom: 0; left: 0; right: 0;
          height: 2px; background: var(--neon);
          transform: scaleX(0); transform-origin: left;
          transition: transform .35s var(--ease);
          border-radius: 0 0 var(--r-xl) var(--r-xl);
        }
        .feat-card:hover {
          border-color: rgba(210,255,0,0.13);
          background: rgba(210,255,0,0.018);
          transform: translateY(-3px);
        }
        .feat-card:hover::after { transform: scaleX(1); }

        .fc-num {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 10px; font-weight: 800;
          letter-spacing: 2.5px; color: var(--neon);
          opacity: 0.45; margin-bottom: 20px; display: block;
        }
        .fc-icon {
          width: 42px; height: 42px; border-radius: var(--r-md);
          background: var(--neon-10); border: 1px solid rgba(210,255,0,0.14);
          display: flex; align-items: center; justify-content: center;
          font-size: 18px; margin-bottom: 16px; flex-shrink: 0;
        }
        .fc-title {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 15.5px; font-weight: 700;
          letter-spacing: -0.3px; margin-bottom: 8px; color: var(--text);
        }
        .fc-desc { font-size: 13px; color: var(--text-2); line-height: 1.72; flex: 1; }

        /* ── FOOTER ── */
        .footer {
          position: relative; z-index: 1;
          border-top: 1px solid var(--border);
          padding: 24px 40px;
          display: flex; align-items: center; justify-content: space-between;
          max-width: 100%;
        }
        .f-logo {
          font-family: 'Space Grotesk', sans-serif;
          font-size: 14px; font-weight: 700; color: var(--text);
          display: flex; align-items: center; gap: 8px;
        }
        .f-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--neon); }
        .f-copy { font-size: 12px; color: var(--text-3); }
        @media (max-width: 560px) {
          .footer { flex-direction: column; gap: 8px; padding: 20px; text-align: center; }
        }
      `}</style>

      {/* ── background layers ── */}
      <div className="dot-grid" aria-hidden="true" />
      <div className="vignette"  aria-hidden="true" />

      {/* ── NAVBAR ── */}
      <nav className="nav" role="navigation" aria-label="Main navigation">
        <a href="#" className="nav-logo">
          <span className="live-dot" aria-hidden="true" />
          JobPulse AI
        </a>

        <ul className="nav-center" role="list">
          <li><a href="#features">Features</a></li>
          <li><a href="#categories">Categories</a></li>
          <li><a href="#register">Alerts</a></li>
        </ul>

        <a href="#register" className="nav-cta">Get Alerts →</a>
      </nav>

      <div className="page">

        {/* ── HERO ── */}
        <section className="hero" aria-labelledby="hero-title">

          {/* left — copy */}
          <div>
            <div className="eyebrow" aria-label="Platform tag">
              <span className="eyebrow-badge">New</span>
              AI-Powered Job Intelligence
            </div>

            <h1 className="headline" id="hero-title">
              Never miss<br />the right
              <span className="hl">opportunity.</span>
            </h1>

            <p className="hero-desc">
              Curated job alerts for BTech, MTech, research, internships,
              remote roles and more — filtered by AI, delivered to your
              inbox at exactly the time you choose.
            </p>

            <div className="stats" role="group" aria-label="Platform statistics">
              <div className="stat">
                <span className="stat-val live" aria-live="polite" aria-label={`${users.length} active users`}>
                  {users.length}
                </span>
                <span className="stat-lbl">Active Users</span>
              </div>
              <div className="stat">
                <span className="stat-val">24/7</span>
                <span className="stat-lbl">Monitoring</span>
              </div>
              <div className="stat">
                <span className="stat-val">10+</span>
                <span className="stat-lbl">Categories</span>
              </div>
            </div>
          </div>

          {/* right — form */}
          <div
            className="fcard"
            id="register"
            ref={cardRef}
            role="region"
            aria-label="Alert registration form"
          >
            <div className="f-title">Start getting alerts</div>
            <div className="f-sub">Free · No spam · Unsubscribe anytime</div>

            {/* status banner */}
            {message.text && (
              <div
                className={`banner ${message.type}`}
                role={message.type === "error" ? "alert" : "status"}
                aria-live={message.type === "error" ? "assertive" : "polite"}
                aria-atomic="true"
              >
                <span className="banner-icon" aria-hidden="true">
                  {message.type === "success" ? "✓" : "⚠"}
                </span>
                {message.text}
              </div>
            )}

            {/* email */}
            <div className="field">
              <div className="f-label" id="email-label">Email Address</div>
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setEmailError(""); }}
                className={`inp ${emailError ? "err" : ""}`}
                aria-labelledby="email-label"
                aria-invalid={!!emailError}
                aria-describedby={emailError ? "email-error" : undefined}
                autoComplete="email"
              />
              {emailError && (
                <div className="f-err" id="email-error" role="alert">
                  ⚠ {emailError}
                </div>
              )}
            </div>

            {/* delivery time */}
            <div className="field">
              <div className="f-label" id="time-label">Daily Delivery Time</div>
              <div className="time-row" role="group" aria-labelledby="time-label">
                <select
                  value={hour}
                  onChange={(e) => setHour(e.target.value)}
                  className="sel"
                  aria-label="Hour"
                >
                  {HOURS.map((h) => <option key={h} value={h}>{h}</option>)}
                </select>
                <select
                  value={minute}
                  onChange={(e) => setMinute(e.target.value)}
                  className="sel"
                  aria-label="Minute"
                >
                  {MINUTES.map((m) => <option key={m} value={m}>{m}</option>)}
                </select>
                <select
                  value={period}
                  onChange={(e) => setPeriod(e.target.value)}
                  className="sel"
                  aria-label="AM or PM"
                >
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>

            {/* categories */}
            <div className="field" id="categories">
              <div className="f-label">
                Job Categories
                {selectedCategories.length > 0 && (
                  <span className="f-count" aria-live="polite">
                    {selectedCategories.length} selected
                  </span>
                )}
              </div>
              <div className="chips" role="group" aria-label="Job category filters">
                {CATEGORIES.map(({ label, icon }) => {
                  const active = selectedCategories.includes(label);
                  return (
                    <button
                      key={label}
                      type="button"
                      onClick={() => toggleCategory(label)}
                      aria-pressed={active}
                      aria-label={`${label} — ${active ? "selected, tap to remove" : "tap to select"}`}
                      className={`chip ${active ? "on" : ""}`}
                    >
                      <span className="chip-icon" aria-hidden="true">{icon}</span>
                      {label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* submit */}
            <button
              type="button"
              onClick={registerUser}
              disabled={loading}
              className="sbtn"
              aria-busy={loading}
              aria-label={loading ? "Activating alerts, please wait" : "Activate my alerts"}
            >
              {loading
                ? <><span className="spin" aria-hidden="true" />Activating...</>
                : "Activate My Alerts →"
              }
            </button>
          </div>
        </section>

        {/* ── MARQUEE ── */}
        <div className="mq" aria-hidden="true">
          <div className="mq-track">
            {MARQUEE_ITEMS.map(({ label, icon }, i) => (
              <div className="mq-pill" key={`${label}-${i}`}>
                <span className="mq-pill-icon">{icon}</span>
                {label}
              </div>
            ))}
          </div>
        </div>

        {/* ── FEATURES ── */}
        <section className="features" id="features" aria-labelledby="features-title">
          <div className="sec-label" aria-hidden="true">Why JobPulse</div>
          <h2 className="sec-title" id="features-title">
            Built different.<br />Designed for you.
          </h2>

          <div className="feat-grid">
            <div className="feat-card">
              <span className="fc-num" aria-hidden="true">01</span>
              <div className="fc-icon" aria-hidden="true">🎯</div>
              <div className="fc-title">Precision Matching</div>
              <p className="fc-desc">
                AI scans thousands of postings daily and surfaces only roles that
                match your exact categories — zero noise, maximum relevance.
              </p>
            </div>

            <div className="feat-card">
              <span className="fc-num" aria-hidden="true">02</span>
              <div className="fc-icon" aria-hidden="true">⚡</div>
              <div className="fc-title">You Set the Time</div>
              <p className="fc-desc">
                Pick your exact delivery time. Morning briefing or evening review —
                alerts arrive when you actually open email.
              </p>
            </div>

            <div className="feat-card">
              <span className="fc-num" aria-hidden="true">03</span>
              <div className="fc-icon" aria-hidden="true">🔒</div>
              <div className="fc-title">Zero Spam Guarantee</div>
              <p className="fc-desc">
                One clean digest per day. No re-marketing, no upsells — just
                high-signal opportunities worth your attention.
              </p>
            </div>
          </div>
        </section>

        {/* ── FOOTER ── */}
        <footer className="footer" role="contentinfo">
          <div className="f-logo">
            <span className="f-dot" aria-hidden="true" />
            JobPulse AI
          </div>
          <span className="f-copy">
            © {new Date().getFullYear()} — Azure · Vercel
          </span>
        </footer>

      </div>
    </>
  );
}