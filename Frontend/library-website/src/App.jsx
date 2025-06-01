import Home from "./endpoints/Home"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./endpoints/LoginPage";
import RegisterPage from "./endpoints/RegisterPage";
import MyBooks from './endpoints/MyBooks';
import BookDetails from './components/BookDetails';

const App = () => {
    return ( 
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/my-books" element={<MyBooks />} />
                <Route path="/book/:id" element={<BookDetails />} />
            </Routes>
        </Router>
     );
}

export default App;