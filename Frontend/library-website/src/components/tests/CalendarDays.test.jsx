// __tests__/CalendarDays.test.jsx
import { render, screen, fireEvent } from "@testing-library/react";
import CalendarDays from "../CalendarDays";

describe("CalendarDays component", () => {
  const today = new Date();
  const maxDate = new Date();
  maxDate.setMonth(today.getMonth() + 3);

  const changeCurrentDayMock = jest.fn();

  test("renders 42 days with proper classes", () => {
    render(
      <CalendarDays
        day={today}
        changeCurrentDay={changeCurrentDayMock}
        today={today}
        maxDate={maxDate}
      />
    );

    const days = screen.getAllByText(/\d+/);
    expect(days.length).toBe(42);

    // Sprawdź, że jest jakiś dzień z klasą "current"
    expect(document.querySelector(".calendar-day.current")).toBeInTheDocument();
  });

  test("calls changeCurrentDay on clicking enabled day", () => {
    render(
      <CalendarDays
        day={today}
        changeCurrentDay={changeCurrentDayMock}
        today={today}
        maxDate={maxDate}
      />
    );

    // Wybierz pierwszy nie-disabled dzień
    const enabledDay = Array.from(document.querySelectorAll(".calendar-day"))
      .find(day => !day.classList.contains("disabled"));
    
    if (enabledDay) {
      fireEvent.click(enabledDay);
      expect(changeCurrentDayMock).toHaveBeenCalled();
    }
  });

  test("does not call changeCurrentDay on clicking disabled day", () => {
    render(
      <CalendarDays
        day={today}
        changeCurrentDay={changeCurrentDayMock}
        today={today}
        maxDate={maxDate}
      />
    );

    // Wybierz pierwszy disabled dzień
    const disabledDay = Array.from(document.querySelectorAll(".calendar-day"))
      .find(day => day.classList.contains("disabled"));

    if (disabledDay) {
      fireEvent.click(disabledDay);
      expect(changeCurrentDayMock).not.toHaveBeenCalled();
    }
  });
});
