import { render } from "@testing-library/react";
import Body from "../Body";
import React from "react";

jest.mock("../List", () => () => <div>Mocked List</div>);

test("renders Body with mocked List", () => {
  const { getByText } = render(<Body inputText="abc" filters={{}} books={[]} />);
  expect(getByText("Mocked List")).toBeInTheDocument();
});
