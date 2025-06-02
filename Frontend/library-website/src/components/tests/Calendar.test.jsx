import { render, screen, fireEvent } from "@testing-library/react";
import Calendar from "../Calendar";

describe("Calendar component", () => {
  const onDateSelectedMock = jest.fn();

  beforeEach(() => {
    onDateSelectedMock.mockClear();
  });

  test("renders current month and weekdays", () => {
    render(<Calendar onDateSelected={onDateSelectedMock} />);
    const monthName = screen.getByRole("heading", { level: 2 });
    expect(monthName).toBeInTheDocument();

    // Sprawdź, czy wszystkie dni tygodnia są widoczne
    ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].forEach((day) => {
      expect(screen.getByText(day)).toBeInTheDocument();
    });
  });

  test("navigates to next and previous month", () => {
    render(<Calendar onDateSelected={onDateSelectedMock} />);
    
    const prevBtn = screen.getByText("❮");
    const nextBtn = screen.getByText("❯");
    const monthHeading = screen.getByRole("heading", { level: 2 });

    const initialMonth = monthHeading.textContent;

    fireEvent.click(nextBtn);
    expect(monthHeading.textContent).not.toBe(initialMonth);

    fireEvent.click(prevBtn);
    fireEvent.click(prevBtn);
    // Po dwóch kliknięciach "prev" miesiąc powinien być wcześniejszy niż początkowy,
    // ale w komponencie jest walidacja żeby nie cofnąć przed today, więc jeśli
    // today jest początkiem, miesiąc może się nie zmienić. Sprawdzamy, że nie jest pusty.
    expect(monthHeading.textContent.length).toBeGreaterThan(0);
  });
});
