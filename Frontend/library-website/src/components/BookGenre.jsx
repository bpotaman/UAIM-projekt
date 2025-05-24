import React from 'react'
import Book from './Book'

function filterBooksByGenre(books_arr, someGenre) {
        books_arr.filter(book => {
        if (book.genre === someGenre) {
            return book
        }
    })
    }

export default function BookGenre(props) {
    
    const booksArr = filterBooksByGenre(props.booksArr, props.genre)

  return (
    <div className='book-genre-comp'>
        <h3> {props.genre} </h3>
        <div className="books-by-genre">
            {booksArr.map(book => <Book img_path={book.image} book_name={book.name} />)}
        </div>
        
        </div>
  )
}
