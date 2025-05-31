import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"; // ✅ Corrected import
import "../css/Auth.css";

const LoginPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errMsg, setErrMsg] = useState("");
  const errRef = useRef();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/login",
        JSON.stringify({ username, password }),
        {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        }
      );

      localStorage.setItem("access_token", response.data.access_token)

      setUsername("");
      setPassword("");
      navigate("/"); 
    } catch (err) {
      if (!err?.response) {
        setErrMsg("No Server Response");
      } else if (err.response?.status === 400) {
        setErrMsg("Missing Username or Password");
      } else if (err.response?.status === 401) {
        setErrMsg("Unauthorized");
      } else {
        setErrMsg("Login Failed");
      }
      errRef.current?.focus();
    }
  };

  return (
    <div className="auth-container">
      <h1 className="auth-title" onClick={() => navigate("/")}>
        BookNest
      </h1>
      <h2>Log in to BookNest</h2>
      <p ref={errRef} className="errmsg">
        {errMsg}
      </p>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Log in</button>
      </form>
      <p>
        Don't have an account?{" "}
        <span className="auth-link" onClick={() => navigate("/register")}>
          Register here
        </span>
      </p>
    </div>
  );
};

export default LoginPage;
