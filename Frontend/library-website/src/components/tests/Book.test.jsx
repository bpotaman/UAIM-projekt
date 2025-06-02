import { render } from "@testing-library/react";
import Book from "../Book";
import { BrowserRouter } from "react-router-dom";


test("renders book title", () => {
  const { getByText } = render(
    <BrowserRouter>
      <Book book_title="Test Book" book_id={1} img_path={null} handle={() => {}} />
    </BrowserRouter>
  );

  expect(getByText("Test Book")).toBeInTheDocument();
});
