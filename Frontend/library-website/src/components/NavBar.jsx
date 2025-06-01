import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import "../css/NavBar.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function NavBar({ setInputText, setFilters, myBooks }) {
  const navigate = useNavigate();

  const [open, setOpen] = useState(false);
  const [filterState, setFilterState] = useState({
    author: "",
    genre: "",
    release_year: ""
  });

  const user_id = localStorage.getItem("access_token")
    ? JSON.parse(atob(localStorage.getItem("access_token").split(".")[1])).sub
    : null;

  const handleInputChange = (e) => {
    setInputText(e.target.value.toLowerCase());
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilterState({ ...filterState, [name]: value });
  };

  const applyFilters = () => {
    setFilters(filterState);
    setOpen(false);
  };

  const clearFilters = () => {
    setFilterState({ author: "", genre: "", release_year: "" });
    setFilters({ author: "", genre: "", release_year: "" });
  };

  return (
    <div className="main">
      <h1>BookNest</h1>
      <div className="nav-controls">
        <button onClick={() => myBooks(user_id)}>My books</button>
        <div className="search-filter-group">
            <TextField
              variant="outlined"
              label="Search title..."
              onChange={handleInputChange}
              size="small"
              className="search"
            />
            <Button
              variant="outlined"
              onClick={() => setOpen(true)}
              size="small"
              className="filter-button"
            >
              Filters
            </Button>
          </div>
        {localStorage.getItem("access_token") ? (
          <button onClick={() => { localStorage.clear(); window.location.reload(); }}>
            Log out
          </button>
        ) : (
          <>
            <button onClick={() => navigate("/login")}>Log in</button>
            <button onClick={() => navigate("/register")}>Sign in</button>
          </>
        )}
      </div>

      {/* Modal z filtrami */}
      <Modal open={open} onClose={() => setOpen(false)}>
        <Box className="filter-modal">
          <h2>Filter books</h2>
          <TextField
            label="Author"
            name="author"
            value={filterState.author}
            onChange={handleFilterChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Genre"
            name="genre"
            value={filterState.genre}
            onChange={handleFilterChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Release Year"
            name="release_year"
            value={filterState.release_year}
            onChange={handleFilterChange}
            fullWidth
            margin="normal"
          />
          <div className="filter-buttons">
            <Button onClick={applyFilters} variant="contained" sx={{ mr: 1 }}>
              Apply
            </Button>
            <Button onClick={clearFilters} variant="outlined" color="error">
              Clear
            </Button>
          </div>
        </Box>
      </Modal>
    </div>
  );
}

export default NavBar;
