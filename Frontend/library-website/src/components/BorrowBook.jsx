import Calendar from "./Calendar";
import "../css/calendar.css";

const BorrowBook = ({ bookId, userId, onDateChosen, onClose }) => {
  const handleDateSelected = (date) => {
  const localDateString = date.toLocaleDateString("en-CA"); // yyyy-mm-dd
  onDateChosen(bookId, userId, localDateString);
};


  return (
    <div className="calendar-overlay">
      <div className="calendar-modal">
        <button className="calendar-close-btn" onClick={onClose}>×</button>
        <p className="calendar-instruction">Select return date (max. 3 months ahead):</p>
        <Calendar onDateSelected={handleDateSelected} />
      </div>
    </div>
  );
};

export default BorrowBook;
