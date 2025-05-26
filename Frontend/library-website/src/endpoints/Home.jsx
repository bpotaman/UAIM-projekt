import React from 'react'
import NavBar from "../components/NavBar";
import Body from "../components/Body";
import { useState, useEffect } from "react";

export default function Home() {
    const [inputText, setInputText] = useState("");

    const [books, setBooks] = useState([]);

   useEffect(() => {
      fetch('http://127.0.0.1:5000/api/books')
         .then((res) => res.json())
         .then((data) => {
            console.log(data);
            setBooks(data);
         })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);
   console.log(books)

    return (
        <>
            <NavBar inputText={inputText} setInputText={setInputText} />
            <Body books={books} inputText={inputText} setInputText={setInputText} />
        </>
  )
}
