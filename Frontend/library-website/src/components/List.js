import React, { useState } from "react";
import Book from "./Book";
import BorrowBook from "./BorrowBook";
import "../css/Book.css";
import axios from "axios";

function List(props) {
  const [selectedBookId, setSelectedBookId] = useState(null);
  const [showCalendar, setShowCalendar] = useState(false);

  // Pobranie user_id z tokenu
  let user_id = null;
  if (localStorage.getItem("access_token") !== null) {
    try {
      const arrayToken = localStorage.getItem("access_token").split(".");
      const tokenPayload = JSON.parse(atob(arrayToken[1]));
      user_id = tokenPayload.sub;
    } catch (e) {
      console.error("Invalid token", e);
    }
  }

  // Filtrowanie książek
  const title_match = (book) => book.title.toLowerCase().includes(props.input);
  const filteredBooks = props.books.filter(title_match);

  // Kliknięcie przycisku "Borrow"
  const handleBorrowClick = (bookId) => {
    setSelectedBookId(bookId);
    setShowCalendar(true);
  };

  // Po wybraniu daty z kalendarza
  const handleDateChosen = async (bookId, userId, due_date) => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/loans",
        JSON.stringify({ book_id: bookId, user_id: userId, due_date }),
        { headers: { "Content-Type": "application/json" } }
      );
      console.log("Loan response:", response);
    } catch (err) {
      console.error("Loan error:", err);
    } finally {
      setShowCalendar(false); // Zamknij kalendarz po złożeniu żądania
    }
  };

  return (
    <div className="searched-books">
      {filteredBooks.map((book) => (
        <Book
          key={book.id}
          img_path={`http://localhost:5000/api/books/${book.id}/cover`}
          book_title={book.title}
          book_id={book.id}
          handle={handleBorrowClick}
        />
      ))}

      {/* Modal z kalendarzem */}
      {showCalendar && selectedBookId && user_id && (
        <BorrowBook
          bookId={selectedBookId}
          userId={user_id}
          onDateChosen={handleDateChosen}
          onClose={() => setShowCalendar(false)}
        />
      )}
    </div>
  );
}

export default List;
