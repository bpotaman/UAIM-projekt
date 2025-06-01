import React from "react";

function CalendarDays({ day, changeCurrentDay, today, maxDate }) {
  const firstDayOfMonth = new Date(day.getFullYear(), day.getMonth(), 1);
  const weekdayOfFirstDay = firstDayOfMonth.getDay();
  const currentDays = [];

  for (let i = 0; i < 42; i++) {
    if (i === 0 && weekdayOfFirstDay === 0) {
      firstDayOfMonth.setDate(firstDayOfMonth.getDate() - 7);
    } else if (i === 0) {
      firstDayOfMonth.setDate(firstDayOfMonth.getDate() + (i - weekdayOfFirstDay));
    } else {
      firstDayOfMonth.setDate(firstDayOfMonth.getDate() + 1);
    }

    const date = new Date(firstDayOfMonth);
    const isCurrentMonth = date.getMonth() === day.getMonth();
    const isPast = date < today.setHours(0, 0, 0, 0);
    const isFuture = date > maxDate;

    currentDays.push({
      date,
      number: date.getDate(),
      month: date.getMonth(),
      year: date.getFullYear(),
      disabled: isPast || isFuture,
      currentMonth: isCurrentMonth
    });
  }

  return (
    <div className="table-content">
      {currentDays.map((day, index) => (
        <div
          className={
            "calendar-day" +
            (day.currentMonth ? " current" : "") +
            (day.disabled ? " disabled" : "")
          }
          key={index}
          onClick={() => !day.disabled && changeCurrentDay(day)}
        >
          <p>{day.number}</p>
        </div>
      ))}
    </div>
  );
}

export default CalendarDays;
