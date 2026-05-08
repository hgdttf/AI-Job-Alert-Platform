import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    localStorage.getItem("admin_token")
  );

  const [users, setUsers] = useState([]);

  const BACKEND_URL = "http://127.0.0.1:8000";


  // =========================
  // FETCH USERS
  // =========================

const fetchUsers = async () => {

  try {

    const response = await axios.get(
      `${BACKEND_URL}/admin/users`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    setUsers(response.data);

  } catch (error) {

    console.log(error);

  }

};


  // =========================
  // LOGIN
  // =========================

  const login = async () => {

    try {

      const response = await axios.post(
        `${BACKEND_URL}/admin/login`,
        {
          email,
          password
        }
      );

      const accessToken =
        response.data.access_token;

      localStorage.setItem(
        "admin_token",
        accessToken
      );

      setToken(accessToken);

    } catch (error) {

      alert("Invalid credentials");

      console.log(error);

    }

  };


  // =========================
  // DELETE USER
  // =========================

  const deleteUser = async (userId) => {

    try {

      await axios.delete(
        `${BACKEND_URL}/admin/delete-user/${userId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      fetchUsers();

    } catch (error) {

      console.log(error);

    }

  };


  // =========================
  // LOAD USERS
  // =========================

  useEffect(() => {

    if (!token) return;

    // call async loader inside effect to avoid calling setState synchronously
    const load = async () => {
      try {
        await fetchUsers();
      } catch (err) {
        console.error(err);
      }
    };

    void load();

  }, [token, fetchUsers]);


  // =========================
  // LOGIN SCREEN
  // =========================

  if (!token) {

    return (

      <div className="
        min-h-screen
        bg-slate-950
        flex
        items-center
        justify-center
      ">

        <div className="
          bg-slate-900
          p-10
          rounded-3xl
          w-[400px]
          shadow-2xl
        ">

          <h1 className="
            text-4xl
            font-bold
            text-white
            mb-8
            text-center
          ">
            Admin Login
          </h1>

          <input
            type="email"
            placeholder="Admin Email"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            className="
              w-full
              p-4
              rounded-xl
              bg-slate-800
              text-white
              mb-5
              outline-none
            "
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            className="
              w-full
              p-4
              rounded-xl
              bg-slate-800
              text-white
              mb-5
              outline-none
            "
          />

          <button
            onClick={login}
            className="
              w-full
              bg-blue-600
              hover:bg-blue-700
              transition
              text-white
              p-4
              rounded-xl
              font-semibold
            "
          >
            Login
          </button>

        </div>

      </div>

    );

  }


  // =========================
  // DASHBOARD
  // =========================

  return (

    <div className="
      min-h-screen
      bg-slate-950
      text-white
      px-6
      py-8
    ">

      {/* HEADER */}

      <div className="
        flex
        justify-between
        items-center
        mb-8
      ">

        <div>

          <h1 className="
            text-4xl
            font-bold
          ">
            JobPulse Admin
          </h1>

          <p className="
            text-slate-400
            mt-1
          ">
            Manage registered users
          </p>

        </div>

        <button
          onClick={() => {

            localStorage.removeItem(
              "admin_token"
            );

            setToken(null);

          }}
          className="
            bg-red-600
            hover:bg-red-700
            px-4
            py-2
            rounded-lg
            text-sm
            font-semibold
            transition
          "
        >
          Logout
        </button>

      </div>


      {/* STATS */}

      <div className="
        bg-slate-900
        rounded-2xl
        p-5
        mb-8
        border
        border-slate-800
      ">

        <p className="
          text-slate-400
          text-sm
        ">
          Total Registered Users
        </p>

        <h2 className="
          text-4xl
          font-bold
          mt-2
        ">
          {users.length}
        </h2>

      </div>


      {/* USERS */}

      <div className="
        grid
        gap-4
      ">

        {users.length === 0 ? (

          <div className="
            bg-slate-900
            p-8
            rounded-2xl
            text-center
            text-slate-400
          ">
            No users registered
          </div>

        ) : (

          users.map((user) => (

            <div
              key={user.id}
              className="
                bg-slate-900
                rounded-2xl
                p-5
                border
                border-slate-800
                flex
                justify-between
                items-center
              "
            >

              <div>

                <h2 className="
                  text-xl
                  font-semibold
                  mb-2
                ">
                  {user.email}
                </h2>

                <p className="
                  text-slate-400
                  text-sm
                ">
                  Time:
                  {" "}
                  {user.delivery_time}
                </p>

                <p className="
                  text-slate-400
                  text-sm
                  mt-1
                ">
                  Categories:
                  {" "}
                  {user.categories}
                </p>

              </div>

              <button
                onClick={() =>
                  deleteUser(user.id)
                }
                className="
                  bg-red-600
                  hover:bg-red-700
                  px-4
                  py-2
                  rounded-lg
                  text-sm
                  font-semibold
                  transition
                "
              >
                Delete
              </button>

            </div>

          ))

        )}

      </div>

    </div>

  );

}