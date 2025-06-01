import Book from './Book'
import "../css/Book.css"
import axios from "axios"
// komponent do wyszukiwania książek
function List(props) {

    const title_match = (book) => book.title.toLowerCase().includes(props.input)

    const filteredBooks = props.books.filter(title_match)

    const handle = async (book_id, user_id, due_date) => {
        console.log(JSON.stringify({ book_id, user_id, due_date}))
        try {
            const response = await axios.post(
                    "http://localhost:5000/api/loans",
                    JSON.stringify({ book_id, user_id, due_date}),
                    {
                        headers: { "Content-Type": "application/json" }}
                );
                console.log(response)
        }
            catch (err) {
        console.log(err)
    }
}
    
    return (
        <div className="searched-books">
            {filteredBooks.map(book => <Book img_path={`http://localhost:5000/api/books/${book.id}/cover`} book_title={book.title} key={book.id} book_id={book.id} due_date={props.due_date} handle={handle} />)}
        </div>
    )
}


export default List