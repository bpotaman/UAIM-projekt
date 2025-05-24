import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/Auth.css";

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    console.log("Logging in with", email, password);
    navigate("/"); 
  };

  return (
    <div className="auth-container">
      <h1 className="auth-title" onClick={() => navigate("/")}>
        BookNest
      </h1>
      <h2>Log in to BookNest</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
