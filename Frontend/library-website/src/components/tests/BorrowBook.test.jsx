import { render, fireEvent } from "@testing-library/react";
import BorrowBook from "../BorrowBook";

test("calls onClose when X button is clicked", () => {
  const onClose = jest.fn();
  const { getByText } = render(
    <BorrowBook bookId={1} userId={1} onDateChosen={() => {}} onClose={onClose} />
  );
  fireEvent.click(getByText("×"));
  expect(onClose).toHaveBeenCalled();
});
