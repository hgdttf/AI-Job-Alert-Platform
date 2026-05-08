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

    <div
      style={{
        minHeight: "100vh",
        background:
          "#020617",
        color: "white",
        padding: "40px",
        fontFamily: "Arial",
      }}
    >

      {/* HERO */}

      <div
        style={{
          textAlign: "center",
          marginBottom: "40px",
        }}
      >

        <h1
          style={{
            fontSize: "52px",
            marginBottom: "10px",
          }}
        >
          AI-Powered Job Alert Platform
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "18px",
          }}
        >
          Daily fresher jobs,
          internships and
          research opportunities
          delivered automatically.
        </p>

      </div>

      {/* STATS */}

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "20px",
          marginBottom: "40px",
          flexWrap: "wrap",
        }}
      >

        <div style={cardStyle}>
          <h2>{users.length}</h2>
          <p>Registered Users</p>
        </div>

        <div style={cardStyle}>
          <h2>24/7</h2>
          <p>Live Alerts</p>
        </div>

        <div style={cardStyle}>
          <h2>10</h2>
          <p>Categories</p>
        </div>

      </div>

      {/* FORM */}

      <div
        style={{
          maxWidth: "700px",
          margin: "0 auto",
          background: "#0f172a",
          padding: "35px",
          borderRadius: "18px",
          border:
            "1px solid #1e293b",
        }}
      >

        <h2
          style={{
            marginBottom: "25px",
          }}
        >
          Register For Daily Alerts
        </h2>

        {/* EMAIL */}

        <div
          style={{
            marginBottom: "25px",
          }}
        >

          <p>Email Address</p>

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            style={inputStyle}
          />

        </div>

        {/* TIME */}

        <div
          style={{
            marginBottom: "25px",
          }}
        >

          <p>Select Delivery Time</p>

          <div
            style={{
              display: "flex",
              gap: "10px",
              alignItems: "center",
            }}
          >

            <select
              value={hour}
              onChange={(e) =>
                setHour(e.target.value)
              }
              style={selectStyle}
            >

              {Array.from(
                { length: 12 },
                (_, i) =>
                  String(i + 1).padStart(2, "0")
              ).map((h) => (
                <option
                  key={h}
                  value={h}
                >
                  {h}
                </option>
              ))}

            </select>

            <span>:</span>

            <select
              value={minute}
              onChange={(e) =>
                setMinute(e.target.value)
              }
              style={selectStyle}
            >

              {Array.from(
                { length: 60 },
                (_, i) =>
                  String(i).padStart(2, "0")
              ).map((m) => (
                <option
                  key={m}
                  value={m}
                >
                  {m}
                </option>
              ))}

            </select>

            <select
              value={period}
              onChange={(e) =>
                setPeriod(e.target.value)
              }
              style={selectStyle}
            >

              <option value="AM">
                AM
              </option>

              <option value="PM">
                PM
              </option>

            </select>

          </div>

          <p
            style={{
              color: "#38bdf8",
              marginTop: "10px",
            }}
          >
            Selected Time:
            {" "}
            {selectedTime}
          </p>

        </div>

        {/* CATEGORIES */}

        <div
          style={{
            marginBottom: "30px",
          }}
        >

          <p>Select Categories</p>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "10px",
              marginTop: "15px",
            }}
          >

            {categories.map((category) => (

              <button
                key={category}
                onClick={() =>
                  toggleCategory(category)
                }
                style={{
                  padding:
                    "10px 16px",

                  borderRadius: "12px",

                  border:
                    selectedCategories.includes(
                      category
                    )
                      ? "none"
                      : "1px solid #334155",

                  background:
                    selectedCategories.includes(
                      category
                    )
                      ? "linear-gradient(to right, #06b6d4, #3b82f6)"
                      : "#0f172a",

                  color: "white",

                  cursor: "pointer",
                }}
              >

                {category}

              </button>

            ))}

          </div>

        </div>

        {/* BUTTON */}

        <button
          onClick={registerUser}
          style={{
            width: "100%",
            padding: "16px",
            border: "none",
            borderRadius: "14px",
            background:
              "linear-gradient(to right, #06b6d4, #2563eb)",
            color: "white",
            fontWeight: "bold",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Activate Alerts
        </button>

        {/* MESSAGE */}

        {message && (

          <div
            style={{
              marginTop: "20px",
              padding: "15px",
              borderRadius: "10px",

              background:
                message.includes(
                  "successful"
                )
                  ? "#14532d"
                  : "#7f1d1d",

              textAlign: "center",
            }}
          >

            {message}

          </div>

        )}

      </div>

      {/* USERS */}

      <div
        style={{
          marginTop: "60px",
          maxWidth: "900px",
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >

        <h2
          style={{
            marginBottom: "20px",
          }}
        >
          Registered Users
        </h2>

        <div
          style={{
            display: "grid",
            gap: "20px",
          }}
        >

          {users.map((user) => (

            <div
              key={user.id}
              style={{
                background: "#0f172a",
                padding: "20px",
                borderRadius: "14px",
                border:
                  "1px solid #1e293b",
              }}
            >

              <p>
                <strong>Email:</strong>
                {" "}
                {user.email}
              </p>

              <p>
                <strong>Categories:</strong>
                {" "}
                {user.categories}
              </p>

              <p>
                <strong>Delivery Time:</strong>
                {" "}
                {user.delivery_time}
              </p>

            </div>

          ))}

        </div>

      </div>

    </div>

  );

}

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