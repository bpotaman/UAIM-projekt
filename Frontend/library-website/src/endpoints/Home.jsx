import React from 'react'
import books from "../data/Books.json"
import NavBar from "../components/NavBar";
import Body from "../components/Body";
import { useState } from "react";

export default function Home() {
    const [inputText, setInputText] = useState("");
    return (
        <>
            <NavBar inputText={inputText} setInputText={setInputText} />
            <Body books={books} inputText={inputText} setInputText={setInputText} />
        </>
  )
}
