import { useEffect, useState } from "react";
import API from "./api";

export default function App() {

  // =========================
  // STATES
  // =========================

  const [email, setEmail] = useState("");

  const [selectedCategories, setSelectedCategories] = useState([]);

  const [hour, setHour] = useState("12");
  const [minute, setMinute] = useState("00");
  const [period, setPeriod] = useState("AM");

  const [users, setUsers] = useState([]);

  const [message, setMessage] = useState("");

  // =========================
  // CATEGORY OPTIONS
  // =========================

  const categories = [
    "BTech",
    "MTech",
    "MS Research",
    "Life Sciences",
    "Internships",
    "Remote",
    "AI/ML",
    "Cybersecurity",
    "Cloud",
    "Software",
  ];

  // =========================
  // TIME FORMAT
  // =========================

  const selectedTime = `${hour}:${minute} ${period}`;

  // =========================
  // TOGGLE CATEGORY
  // =========================

  const toggleCategory = (category) => {

    if (selectedCategories.includes(category)) {

      setSelectedCategories(
        selectedCategories.filter(
          (item) => item !== category
        )
      );

    } else {

      setSelectedCategories([
        ...selectedCategories,
        category,
      ]);

    }

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

    try {

      setMessage("");

      // VALIDATION

      if (!email) {

        setMessage("Email is required");

        return;

      }

      if (selectedCategories.length === 0) {

        setMessage("Select at least one category");

        return;

      }

      // API REQUEST

      await API.post(
        "/register",
        {
          email,
          categories:
            selectedCategories.join(","),

          delivery_time:
            selectedTime,
        }
      );

      setMessage(
        "Registration successful"
      );

      // RESET FORM

      setEmail("");

      setSelectedCategories([]);

      setHour("12");

      setMinute("00");

      setPeriod("AM");

      // REFRESH USERS

      fetchUsers();

    } catch (error) {

      console.error(error);

      setMessage("Registration failed");

    }

  };

  // =========================
  // LOAD USERS
  // =========================

  useEffect(() => {

    const loadUsers = async () => {

      await fetchUsers();

    };

    loadUsers();

  }, []);

  // =========================
  // UI
  // =========================

  return (
  <div className="min-h-screen bg-[#020617] text-white overflow-hidden">
    
    {/* Background Effects */}
    <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-blue-500/5 to-purple-500/10 blur-3xl"></div>

    {/* Navbar */}
    <nav className="relative z-10 flex items-center justify-between px-8 py-6 border-b border-white/10 backdrop-blur-md">
      <h1 className="text-2xl font-bold tracking-wide">
        JobPulse AI
      </h1>

      <div className="hidden md:flex gap-8 text-sm text-gray-300">
        <a href="#" className="hover:text-cyan-400 transition">
          Features
        </a>

        <a href="#" className="hover:text-cyan-400 transition">
          Categories
        </a>

        <a href="#" className="hover:text-cyan-400 transition">
          Alerts
        </a>
      </div>
    </nav>

    {/* Hero Section */}
    <section className="relative z-10 max-w-7xl mx-auto px-6 py-20 grid lg:grid-cols-2 gap-16 items-center">

      {/* Left Side */}
      <div>
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-300 text-sm mb-6">
          AI Powered Job Aggregation
        </div>

        <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
          Discover Fresh
          <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            {" "}Jobs Faster
          </span>
        </h1>

        <p className="text-gray-400 text-lg leading-relaxed mb-10 max-w-xl">
          Automated AI-powered alerts for internships, fresher jobs,
          research opportunities, and remote positions delivered directly
          to your inbox every day.
        </p>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-xl">
            <h2 className="text-3xl font-bold text-cyan-400">
              {users.length}
            </h2>

            <p className="text-gray-400 text-sm mt-1">
              Registered Users
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-xl">
            <h2 className="text-3xl font-bold text-cyan-400">
              24/7
            </h2>

            <p className="text-gray-400 text-sm mt-1">
              Smart Alerts
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-5 backdrop-blur-xl">
            <h2 className="text-3xl font-bold text-cyan-400">
              10+
            </h2>

            <p className="text-gray-400 text-sm mt-1">
              Categories
            </p>
          </div>
        </div>
      </div>

      {/* Right Side Form */}
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-3xl blur-2xl opacity-20"></div>

        <div className="relative bg-white/5 border border-white/10 backdrop-blur-2xl rounded-3xl p-8 shadow-2xl">

          <h2 className="text-3xl font-bold mb-2">
            Register For Alerts
          </h2>

          <p className="text-gray-400 mb-8">
            Stay updated with the latest opportunities.
          </p>

          {/* Email */}
          <div className="mb-6">
            <label className="block mb-3 text-sm text-gray-300">
              Email Address
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-[#020617] border border-white/10 rounded-xl px-4 py-4 focus:outline-none focus:border-cyan-400 transition"
            />
          </div>

          {/* Time Selector */}
          <div className="mb-8">
            <label className="block mb-3 text-sm text-gray-300">
              Delivery Time
            </label>

            <div className="flex gap-3">
              <select
                value={hour}
                onChange={(e) => setHour(e.target.value)}
                className="bg-[#020617] border border-white/10 rounded-xl px-4 py-3"
              >
                {hours.map((h) => (
                  <option key={h}>{h}</option>
                ))}
              </select>

              <select
                value={minute}
                onChange={(e) => setMinute(e.target.value)}
                className="bg-[#020617] border border-white/10 rounded-xl px-4 py-3"
              >
                {minutes.map((m) => (
                  <option key={m}>{m}</option>
                ))}
              </select>

              <select
                value={period}
                onChange={(e) => setPeriod(e.target.value)}
                className="bg-[#020617] border border-white/10 rounded-xl px-4 py-3"
              >
                <option>AM</option>
                <option>PM</option>
              </select>
            </div>
          </div>

          {/* Categories */}
          <div className="mb-8">
            <label className="block mb-4 text-sm text-gray-300">
              Categories
            </label>

            <div className="flex flex-wrap gap-3">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => toggleCategory(category)}
                  className={`px-4 py-2 rounded-xl border transition-all duration-300 ${
                    selectedCategories.includes(category)
                      ? "bg-cyan-500 text-black border-cyan-400"
                      : "bg-white/5 border-white/10 hover:border-cyan-400"
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            onClick={registerUser}
            className="w-full py-4 rounded-xl font-semibold bg-gradient-to-r from-cyan-500 to-blue-600 hover:scale-[1.02] transition-all duration-300 shadow-lg shadow-cyan-500/20"
          >
            Activate Alerts
          </button>
        </div>
      </div>
    </section>
  </div>
)}

// =========================
// STYLES
// =========================

const cardStyle = {
  background: "#0f172a",
  padding: "25px",
  borderRadius: "16px",
  width: "220px",
  textAlign: "center",
  border: "1px solid #1e293b",
};

const inputStyle = {
  width: "100%",
  padding: "14px",
  borderRadius: "12px",
  border: "1px solid #334155",
  background: "#020617",
  color: "white",
  marginTop: "10px",
};

const selectStyle = {
  padding: "12px",
  borderRadius: "10px",
  border: "1px solid #334155",
  background: "#020617",
  color: "white",
};