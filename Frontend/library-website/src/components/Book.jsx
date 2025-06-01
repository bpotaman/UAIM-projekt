import "../css/Book.css";
import { useNavigate } from 'react-router-dom';

const Book = ({ img_path, book_title, book_id, loan_date, due_date, handle }) => {

  let user_id = null
  const navigate = useNavigate();
  
  if (localStorage.getItem("access_token") === null) {
    user_id = false
  }
  else {
    const arrayToken = localStorage.getItem("access_token").split('.')
    const tokenPayload = JSON.parse(atob(arrayToken[1]))
    user_id = tokenPayload.sub
  }
  
  return (
    <div className="book-card">
        <img src={img_path} alt={book_title} onClick={() => navigate(`/book/${book_id}`)} style={{ cursor: "pointer" }} />
        <h3 onClick={() => navigate(`/book/${book_id}`)} style={{ cursor: "pointer" }}>{book_title}</h3>
        <button onClick={() => handle(book_id, user_id, "2010-10-04")}>Borrow</button>
    </div>
  );
};

export default Book;