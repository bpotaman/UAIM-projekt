import React, { useEffect, useState } from "react";
import axios from "axios";
import "../css/MyBooks.css";
import { useNavigate } from "react-router-dom";

const MyBooks = () => {
  const [loans, setLoans] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    const arrayToken = token.split(".");
    const tokenPayload = JSON.parse(atob(arrayToken[1]));
    const user_id = tokenPayload.sub;

    axios
      .get(`http://localhost:5000/api/loans/${user_id}`)
      .then((res) => {
        const unreturned = res.data.loans.filter(
          (loan) => loan.return_date === null
        );
        setLoans(unreturned);
      })
      .catch((err) => {
        console.error("Failed to fetch user loans:", err);
      });
  }, [navigate]);

  const handleReturn = async (loanId) => {
    try {
      await axios.put(`http://localhost:5000/api/loans/${loanId}/return`);
      setLoans((prev) => prev.filter((loan) => loan.id !== loanId));
    } catch (err) {
      console.error("Failed to return loan:", err);
    }
  };

  return (
  <div className="my-books-container">
    <button className="back-button" onClick={() => navigate("/")}>← Back to Home</button>
    <h2>My Current Loans</h2>
    {loans.length === 0 ? (
      <p>You have no unreturned books.</p>
    ) : (
      <div className="loan-list">
        {loans.map((loan) => (
          <div className="loan-card" key={loan.id}>
            <img
              src={`http://localhost:5000/api/books/${loan.book.id}/cover`}
              alt={loan.book.title}
              className="loan-cover"
            />
            <div className="loan-details">
              <h3>{loan.book.title}</h3>
              <p><strong>Author:</strong> {loan.book.author}</p>
              <p><strong>Loaned on:</strong> {loan.loan_date}</p>
              <p><strong>Due by:</strong> {loan.due_date}</p>
              <button onClick={() => handleReturn(loan.id)}>Return</button>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

};

export default MyBooks;
