from fastapi import FastAPI, HTTPException
import books_service
from pydantic import BaseModel

app = FastAPI()

@app.get("/book/{book_id}")
def get_book(book_id: str):
    book_data = books_service.get_book_basic_data(book_id)
    book_data["more data"] = "http://localhost:8000/book/details/" + book_id
    return book_data


@app.get("/book/details/{book_id}")
def get_book(book_id: str):
    book_details = books_service.get_a_book_details(book_id)
    print(book_details)
    book_data = {"isbn": book_id}
    book_data["details"] = book_details
    return book_data


class BookReviewModel(BaseModel):
    isbn: str
    review: str



@app.post("/book/review", status_code=202)
def add_book_review(book_review: BookReviewModel):
    review_temporary_id = books_service.add_book_review_to_validation(book_review.isbn, book_review.review)
    response_content = {
        "review_id": review_temporary_id,
        "status": "http://localhost:8000/book/review/" + str(review_temporary_id) + "/status"
    }
    return response_content
@app.get("/book/review/{review_id}/status", status_code=303)
def get_book_review_status(review_id: str):
    # if review is validated...
    return {
        "review_id": review_id,
        "status": "http://localhost:8000/book/review/" + review_id
    }


@app.get("/book/review/{review_id}")
def get_book_review(review_id: str):
    review = books_service.review_by_id(review_id)
    return {
        "review_id": review_id,
        "review": review
    }