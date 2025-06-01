import React, { useState } from "react";
import Book from "./Book";
import BorrowBook from "./BorrowBook";
import "../css/Book.css";
import axios from "axios";

function List({ books, input, filters }) {
  const [selectedBookId, setSelectedBookId] = useState(null);
  const [showCalendar, setShowCalendar] = useState(false);

  // Pobieranie user_id z JWT
  let user_id = null;
  if (localStorage.getItem("access_token")) {
    try {
      const arrayToken = localStorage.getItem("access_token").split(".");
      const tokenPayload = JSON.parse(atob(arrayToken[1]));
      user_id = tokenPayload.sub;
    } catch (e) {
      console.error("Invalid token", e);
    }
  }

  // Filtrowanie książek: tytuł + dodatkowe filtry
  const filteredBooks = books.filter((book) => {
    const titleMatch = book.title.toLowerCase().includes(input.toLowerCase());

    const authorMatch = !filters.author ||
      book.author.toLowerCase().includes(filters.author.toLowerCase());

    const genreMatch = !filters.genre ||
      book.genre.toLowerCase().includes(filters.genre.toLowerCase());

    const yearMatch = !filters.release_year ||
      book.release_year.toString().includes(filters.release_year);

    return titleMatch && authorMatch && genreMatch && yearMatch;
  });

  // Obsługa kliknięcia "Borrow"
  const handleBorrowClick = (bookId) => {
    setSelectedBookId(bookId);
    setShowCalendar(true);
  };

  // Po wybraniu daty
  const handleDateChosen = async (bookId, userId, due_date) => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/loans",
        JSON.stringify({ book_id: bookId, user_id: userId, due_date }),
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Loan response:", response);
    } catch (err) {
      console.error("Loan error:", err);
    } finally {
      setShowCalendar(false);
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
