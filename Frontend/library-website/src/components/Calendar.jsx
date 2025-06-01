// src/components/Calendar.jsx
import React, { Component } from 'react';
import CalendarDays from './CalendarDays.jsx';
import "../css/calendar.css";

export default class Calendar extends Component {
  constructor() {
    super();

    this.weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    this.months = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'];

    this.today = new Date();
    this.maxDate = new Date();
    this.maxDate.setMonth(this.today.getMonth() + 3);

    this.state = {
        currentDay: new Date(),
        displayedMonth: new Date()
};

  }

  changeCurrentDay = (day) => {
    const selected = new Date(day.year, day.month, day.number);

    // Walidacja daty
    if (selected < this.today || selected > this.maxDate) return;

    this.setState({ currentDay: selected });

    // Przekazanie wybranej daty rodzicowi
    this.props.onDateSelected(selected);
  }

  goToPrevMonth = () => {
  const { displayedMonth } = this.state;
  const prev = new Date(displayedMonth);
  prev.setMonth(prev.getMonth() - 1);

  if (prev >= this.today) {
    this.setState({ displayedMonth: prev });
  }
};

goToNextMonth = () => {
  const { displayedMonth } = this.state;
  const next = new Date(displayedMonth);
  next.setMonth(next.getMonth() + 1);

  if (next <= this.maxDate) {
    this.setState({ displayedMonth: next });
  }
};


  render() {
    return (
      <div className="calendar-container">
        <div className="calendar">
          <div className="calendar-header">
  <button onClick={this.goToPrevMonth} className="calendar-nav-btn">❮</button>
  <h2>{this.months[this.state.displayedMonth.getMonth()]} {this.state.displayedMonth.getFullYear()}</h2>
  <button onClick={this.goToNextMonth} className="calendar-nav-btn">❯</button>
</div>

          <div className="calendar-body">
            <div className="table-header">
              {this.weekdays.map((weekday, index) => (
                <div className="weekday" key={index}><p>{weekday}</p></div>
              ))}
            </div>
            <CalendarDays
                day={this.state.displayedMonth}
                changeCurrentDay={this.changeCurrentDay}
                today={this.today}
                maxDate={this.maxDate}
/>
          </div>
        </div>
      </div>
    );
  }
}
