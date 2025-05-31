import "../css/Book.css";

const Book = ({ img_path, book_title }) => {
  return (
    <div className="book-card">
      <img src={img_path} alt={book_title} />
      <h3>{book_title}</h3>
      <button>Borrow</button>
    </div>
  );
};

export default Book;
