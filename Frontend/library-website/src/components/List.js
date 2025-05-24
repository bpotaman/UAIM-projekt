import Book from './Book'
import "../css/Book.css"

function List(props) {

    const name_match = (book) => book.name.toLowerCase().includes(props.input)

    const filteredBooks = props.books.filter(name_match)

    return (
        <div className="searched-books">
            {filteredBooks.map(book => <Book img_path={book.image} book_name={book.name} key={book.id}/>)}
        </div>
    )
}

export default List