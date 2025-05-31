import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/Auth.css";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errMsg, setErrMsg] = useState("");
  const errRef = useRef();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/register",
        JSON.stringify({ email, username, password }),
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log("Registration successful:", response.data);
      navigate("/login");
    } catch (err) {
      if (!err?.response) {
        setErrMsg("No Server Response");
      } else if (err.response?.status === 400) {
        setErrMsg("Missing or invalid input");
      } else if (err.response?.status === 409) {
        setErrMsg("Username or email already exists");
      } else {
        setErrMsg("Registration Failed");
      }
      errRef.current?.focus();
    }
  };

  return (
    <div className="auth-container">
      <h1 className="auth-title" onClick={() => navigate("/")}>
        BookNest
      </h1>
      <h2>Create your BookNest account</h2>
      <p ref={errRef} className="errmsg">
        {errMsg}
      </p>
      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
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
        <button type="submit">Sign up</button>
      </form>
      <p>
        Already have an account?{" "}
        <span className="auth-link" onClick={() => navigate("/login")}>
          Log in
        </span>
      </p>
    </div>
  );
};

export default RegisterPage;
