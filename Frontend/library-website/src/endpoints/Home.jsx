import React from 'react'
import NavBar from "../components/NavBar";
import Body from "../components/Body";
import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';


export default function Home() {
    const [inputText, setInputText] = useState("");

    const [books, setBooks] = useState([]);
    let navigate = useNavigate();

   useEffect(() => {
      fetch('http://localhost:5000/api/books')
         .then((res) => res.json())
         .then((data) => {
            setBooks(data);
         })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);

   const myBooks = (user_id) => {
    if (user_id === null) {
      navigate("/login")
    }
    else {
      navigate("/my-books")
    }
  }
   

    return (
        <>
            <NavBar inputText={inputText} setInputText={setInputText} myBooks={myBooks} />
            <Body books={books} inputText={inputText} setInputText={setInputText} />
        </>
  )
}
