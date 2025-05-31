import Book from './Book'
import "../css/Book.css"

// komponent do wyszukiwania książek
function List(props) {

    const title_match = (book) => book.title.toLowerCase().includes(props.input)

    const filteredBooks = props.books.filter(title_match)

    return (
        <div className="searched-books">
            {filteredBooks.map(book => <Book img_path={`http://localhost:5000/api/books/${book.id}/cover`} book_title={book.title} key={book.id}/>)}
        </div>
    )
}

export default List