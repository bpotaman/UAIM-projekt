import TextField from "@mui/material/TextField";
import "../css/NavBar.css";
import { useNavigate } from 'react-router-dom';

function NavBar(props) {
  let inputHandler = (e) => {
    var lowerCase = e.target.value.toLowerCase();
    props.setInputText(lowerCase);
  }

  let navigate = useNavigate();
  

  return (
    <div className="main">
      <h1>BookNest</h1>
      <div className="nav-controls">
        <button>My books</button>
        <div className="search">
          <TextField
            id="outlined-basic"
            onChange={inputHandler}
            variant="outlined"
            fullWidth
            label="Search"
          />
        </div>
        {localStorage.getItem("access_token") ?
        <button onClick={() => {localStorage.clear(); window.location.reload()}}>Log out</button> :
        <> <button onClick={() => navigate("/login")}>Log in</button>
        <button onClick={() => navigate("/register")}>Sign in</button> </>
        }
      </div>
    </div>
  );
}

export default NavBar;
