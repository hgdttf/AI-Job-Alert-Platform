import { useEffect, useState, useCallback } from "react";
import API from "./api";

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(() => {
  return localStorage.getItem("admin_token");
});

  const [users, setUsers] = useState([]);

  const [error, setError] = useState("");

  // =========================
  // FETCH USERS
  // =========================

  const fetchUsers = useCallback(async () => {
    try {
      const response = await API.get("/admin/users", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setUsers(response.data);

    } catch (error) {
      console.error(error);
      setError("Failed to fetch users");
    }
  }, [token]);

  // =========================
  // LOGIN
  // =========================

  const login = async () => {
    try {
      setError("");

      const response = await API.post(
        "/admin/login",
        {
          email,
          password,
        }
      );

      const accessToken = response.data.access_token;

      localStorage.setItem(
        "admin_token",
        accessToken
      );

      setToken(accessToken);

    } catch (error) {
      console.error(error);
      setError("Invalid credentials");
    }
  };

  // =========================
  // DELETE USER
  // =========================

  const deleteUser = async (userId) => {
    try {
      await API.delete(
        `/admin/delete-user/${userId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      await fetchUsers();

    } catch (error) {
      console.error(error);
      setError("Failed to delete user");
    }
  };

  // =========================
  // LOAD USERS AFTER LOGIN
  // =========================

  useEffect(() => {

  const loadUsers = async () => {

    if (token) {
      await fetchUsers();
    }

  };

  loadUsers();

}, [token, fetchUsers]);
  // =========================
  // LOGIN SCREEN
  // =========================

  if (!token) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "#0f172a",
          color: "white",
        }}
      >
        <div
          style={{
            width: "350px",
            padding: "30px",
            borderRadius: "12px",
            background: "#1e293b",
          }}
        >
          <h1
            style={{
              marginBottom: "20px",
              textAlign: "center",
            }}
          >
            Admin Login
          </h1>

          <input
            type="email"
            placeholder="Admin Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
              borderRadius: "8px",
              border: "none",
            }}
          />

          <input
            type="password"
            placeholder="Admin Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "15px",
              borderRadius: "8px",
              border: "none",
            }}
          />

          <button
            onClick={login}
            style={{
              width: "100%",
              padding: "12px",
              border: "none",
              borderRadius: "8px",
              background: "#2563eb",
              color: "white",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Login
          </button>

          {error && (
            <p
              style={{
                color: "red",
                marginTop: "15px",
                textAlign: "center",
              }}
            >
              {error}
            </p>
          )}
        </div>
      </div>
    );
  }

  // =========================
  // ADMIN DASHBOARD
  // =========================

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "30px",
        background: "#0f172a",
        color: "white",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "30px",
        }}
      >
        <h1>Admin Dashboard</h1>

        <button
          onClick={() => {
            localStorage.removeItem(
              "admin_token"
            );

            setToken("");
          }}
          style={{
            padding: "10px 20px",
            border: "none",
            borderRadius: "8px",
            background: "red",
            color: "white",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>

      {error && (
        <p
          style={{
            color: "red",
            marginBottom: "20px",
          }}
        >
          {error}
        </p>
      )}

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
              background: "#1e293b",
              padding: "20px",
              borderRadius: "12px",
            }}
          >
            <p>
              <strong>Email:</strong>{" "}
              {user.email}
            </p>

            <p>
              <strong>Categories:</strong>{" "}
              {user.categories}
            </p>

            <p>
              <strong>Delivery Time:</strong>{" "}
              {user.delivery_time}
            </p>

            <button
              onClick={() =>
                deleteUser(user.id)
              }
              style={{
                marginTop: "15px",
                padding: "10px 15px",
                border: "none",
                borderRadius: "8px",
                background: "red",
                color: "white",
                cursor: "pointer",
              }}
            >
              Delete User
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}