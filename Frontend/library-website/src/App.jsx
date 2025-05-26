import Home from "./endpoints/Home"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./endpoints/LoginPage";
import RegisterPage from "./endpoints/RegisterPage";

const App = () => {
    return ( 
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
            </Routes>
        </Router>
     );
}

export default App;