// src/pages/BookDetails.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../css/BookDetails.css";

const BookDetails = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://localhost:5000/api/books`)
      .then((res) => res.json())
      .then((data) => {
        const found = data.find(b => b.id === parseInt(id));
        if (found) {
          setBook(found);
        } else {
          navigate("/"); // Redirect if not found
        }
      });
  }, [id, navigate]);

  if (!book) return <div className="book-details-container">Loading...</div>;

  return (
    <div className="book-details-container">
      <button className="back-button" onClick={() => navigate("/")}>← Back to Home</button>
      <div className="book-info">
        <img src={`http://localhost:5000/api/books/${book.id}/cover`} alt={book.title} />
        <div className="info-text">
          <h2>{book.title}</h2>
          <p><strong>Author:</strong> {book.author}</p>
          <p><strong>Release Year:</strong> {book.release_year}</p>
          <p><strong>Description:</strong> {book.description}</p>
        </div>
      </div>
    </div>
  );
};

export default BookDetails;
