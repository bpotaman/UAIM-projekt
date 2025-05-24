import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../css/Auth.css";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    console.log("Registering with", email, password);
    navigate("/"); 
  };

  return (
    <div className="auth-container">
      <h1 className="auth-title" onClick={() => navigate("/")}>
        BookNest
      </h1>
      <h2>Create your BookNest account</h2>
      <form onSubmit={handleRegister}>
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
