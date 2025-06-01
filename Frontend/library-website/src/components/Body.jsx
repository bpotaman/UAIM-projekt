import React from "react";
import List from "./List";

export default function Body(props) {
  return (
    <div>
      <List
        input={props.inputText}
        filters={props.filters}
        books={props.books}
      />
    </div>
  );
}
