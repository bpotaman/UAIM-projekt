import { render, screen, waitFor } from "@testing-library/react";
import BookDetails from "../BookDetails";
import { BrowserRouter, MemoryRouter, Route, Routes } from "react-router-dom";

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () =>
        Promise.resolve([{ id: 1, title: "Test Book", author: "Author", release_year: 2020, description: "Desc" }]),
    })
  );
});

test("renders book details correctly", async () => {
  render(
    <MemoryRouter initialEntries={["/book/1"]}>
      <Routes>
        <Route path="/book/:id" element={<BookDetails />} />
      </Routes>
    </MemoryRouter>
  );

  await waitFor(() => expect(screen.getByText("Test Book")).toBeInTheDocument());
});
