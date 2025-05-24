import "../css/Book.css";

const Book = ({ title, image }) => {
  return (
    <div className="book-card">
      <img src={image} alt={title} />
      <h3>{title}</h3>
      <button>Borrow</button>
    </div>
  );
};

export default Book;
