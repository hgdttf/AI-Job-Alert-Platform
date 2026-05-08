import { useEffect, useState } from "react";

import axios from "axios";

import {
  FaRocket,
  FaBell,
  FaUsers,
  FaClock,
  FaEnvelope,
} from "react-icons/fa";

import { motion } from "framer-motion";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [email, setEmail] = useState("");

  const [hour, setHour] = useState("12");

  const [minute, setMinute] = useState("00");

  const [mode, setMode] = useState("AM");

  const [users, setUsers] = useState([]);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [messageType, setMessageType] = useState("");

  const [selectedCategories, setSelectedCategories] = useState([]);

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

  const hours = Array.from({ length: 12 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  );

  const minutes = Array.from({ length: 60 }, (_, i) =>
    String(i).padStart(2, "0")
  );

  const toggleCategory = (category) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(
        selectedCategories.filter((c) => c !== category)
      );
    } else {
      setSelectedCategories([...selectedCategories, category]);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_URL}/users`);

      setUsers(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");

    if (!email.trim()) {
      setMessage("Please enter email");
      setMessageType("error");
      return;
    }

    if (selectedCategories.length === 0) {
      setMessage("Please select at least one category");
      setMessageType("error");
      return;
    }

    try {
      setLoading(true);

      const deliveryTime = `${hour}:${minute} ${mode}`;

      const payload = {
        email: email.trim(),
        categories: selectedCategories,
        delivery_time: deliveryTime,
      };

      const response = await axios.post(
        `${API_URL}/register`,
        payload
      );

      setMessage(response.data.message);

      setMessageType("success");

      setEmail("");

      setSelectedCategories([]);

      fetchUsers();
    } catch (error) {
      console.error(error);

      setMessage("Registration failed");

      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] text-white overflow-x-hidden">

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(59,130,246,0.18),transparent_40%)]"></div>

      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px)",
          backgroundSize: "40px 40px",
        }}
      />

      <div className="relative z-10 px-6 py-12">

        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="text-center mb-14"
        >

          <div className="inline-flex items-center gap-3 bg-blue-500/10 border border-blue-500/20 px-5 py-2 rounded-full mb-6">
            <FaRocket className="text-cyan-400" />

            <span className="text-cyan-300 font-medium">
              Smart AI Automation
            </span>
          </div>

          <h1 className="text-5xl md:text-7xl font-black leading-tight mb-6">
            AI-Powered{" "}

            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              Job Alert
            </span>{" "}

            Platform
          </h1>

          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Daily fresher jobs, internships and research opportunities delivered automatically.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 max-w-7xl mx-auto mb-12">

          <div className="bg-[#07122b] border border-white/10 rounded-3xl p-8 text-center">
            <FaUsers className="mx-auto text-cyan-400 text-3xl mb-4" />

            <h2 className="text-5xl font-bold mb-2">
              {users.length}
            </h2>

            <p className="text-gray-400">
              Registered Users
            </p>
          </div>

          <div className="bg-[#07122b] border border-white/10 rounded-3xl p-8 text-center">
            <FaBell className="mx-auto text-cyan-400 text-3xl mb-4" />

            <h2 className="text-5xl font-bold mb-2">
              24/7
            </h2>

            <p className="text-gray-400">
              Live Alerts
            </p>
          </div>

          <div className="bg-[#07122b] border border-white/10 rounded-3xl p-8 text-center">
            <FaClock className="mx-auto text-cyan-400 text-3xl mb-4" />

            <h2 className="text-5xl font-bold mb-2">
              {categories.length}
            </h2>

            <p className="text-gray-400">
              Categories
            </p>
          </div>
        </div>

        <div className="max-w-3xl mx-auto bg-[#07122b]/90 border border-white/10 rounded-[32px] p-8 md:p-10">

          <div className="flex items-center gap-4 mb-8">
            <FaEnvelope className="text-4xl text-cyan-400" />

            <h2 className="text-4xl font-bold">
              Register For Daily Alerts
            </h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">

            <div>
              <label className="block text-gray-300 mb-3 text-lg">
                Email Address
              </label>

              <input
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-[#020817] border border-white/10 rounded-2xl px-5 py-4 text-lg outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-gray-300 mb-4 text-lg">
                Select Delivery Time
              </label>

              <div className="flex flex-wrap items-center gap-4">

                <select
                  value={hour}
                  onChange={(e) => setHour(e.target.value)}
                  className="bg-[#020817] border border-white/10 rounded-2xl px-5 py-4 text-xl font-bold"
                >
                  {hours.map((h) => (
                    <option key={h}>{h}</option>
                  ))}
                </select>

                <span className="text-3xl font-bold text-cyan-400">
                  :
                </span>

                <select
                  value={minute}
                  onChange={(e) => setMinute(e.target.value)}
                  className="bg-[#020817] border border-white/10 rounded-2xl px-5 py-4 text-xl font-bold"
                >
                  {minutes.map((m) => (
                    <option key={m}>{m}</option>
                  ))}
                </select>

                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="bg-[#020817] border border-white/10 rounded-2xl px-5 py-4 text-xl font-bold"
                >
                  <option>AM</option>
                  <option>PM</option>
                </select>
              </div>

              <p className="mt-4 text-cyan-400 font-semibold">
                Selected Time: {hour}:{minute} {mode}
              </p>
            </div>

            <div>
              <label className="block text-gray-300 mb-4 text-lg">
                Select Categories
              </label>

              <div className="flex flex-wrap gap-4">
                {categories.map((category) => (
                  <button
                    type="button"
                    key={category}
                    onClick={() => toggleCategory(category)}
                    className={`px-5 py-3 rounded-2xl transition font-medium border ${
                      selectedCategories.includes(category)
                        ? "bg-gradient-to-r from-cyan-500 to-blue-600 border-transparent"
                        : "bg-[#111c36] border-white/10"
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-5 rounded-2xl text-xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600"
            >
              {loading ? "Activating..." : "Activate Alerts"}
            </button>
          </form>

          {message && (
            <div
              className={`mt-8 p-4 rounded-2xl text-center font-semibold ${
                messageType === "success"
                  ? "bg-green-500/20 text-green-300"
                  : "bg-red-500/20 text-red-300"
              }`}
            >
              {message}
            </div>
          )}
        </div>

        <div className="max-w-5xl mx-auto mt-16">

          <h2 className="text-4xl font-bold mb-8">
            Registered Users
          </h2>

          <div className="grid gap-6">

            {users.map((user, index) => (
              <div
                key={index}
                className="bg-[#07122b] border border-white/10 rounded-3xl p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4"
              >
                <div>
                  <h3 className="text-2xl font-bold">
                    {user.email}
                  </h3>

                  <p className="text-gray-400 mt-2">
                    {user.categories}
                  </p>
                </div>

                <div className="text-cyan-400 text-xl font-bold">
                  {user.delivery_time}
                </div>
              </div>
            ))}

          </div>
        </div>
      </div>
    </div>
  );
}