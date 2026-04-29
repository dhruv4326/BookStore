from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel , Field
from starlette import status

app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    published_date:int
    description:str
    rating:int

    def __init__(self,id,title,author,published_date,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.published_date=published_date
        self.description=description
        self.rating=rating


class book_request(BaseModel):
    id: Optional[int] = Field(description='Id is not needed at the time of creation' , default=None)  # it makes the id optional as the new user don't know the last id of the book so it cannot recommened to fill the id by user 
    title:str = Field(min_length=3)
    author:str = Field(min_length=3)
    published_date:int = Field(gt=1999 , lt=2030)
    description:str = Field(min_length=10,max_length=100)
    rating: int =Field(gt=-1 , lt=6) #gt=greater than and lt=less than
    
class config:
    schema_extra={
        'example':{
            "title": "string",
            "author": "string",
            "published_date:int"
            "description": "stringstri",
            "rating": 5
        }
    }


BOOKS=[
     Book(1,'Title one' , 'Author one' , 2002,'Nice Book ', 3),
     Book(2,'Title two' , 'Author two' , 2001,'Nice Book ', 4),
     Book(3,'Title three' , 'Author three' ,2007, 'Nice Book ', 5),
     Book(4,'Title four' , 'Author four' , 2002,'Nice Book ', 5),
     Book(5,'Title five' , 'Author five' , 2002,'Nice Book ', 3)
]

@app.get("/books" , status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_books_with_id(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            print('No Book Found!!')
    raise HTTPException(status_code=404 , detail="Item Not Found.")        
    


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating:int = Query(gt=0,lt=6)):
    fetched_book=[]
    for book in BOOKS:
        if book.rating == book_rating:
            fetched_book.append(book)
    return fetched_book


@app.get("/books/publish/", status_code=status.HTTP_200_OK) 
async def get_book_by_year(book_year:int=Query(gt=1999,lt=2030)):
    fetched_books=[]
    for book in BOOKS:
        if book.published_date == book_year:
            fetched_books.append(book)
        
    return fetched_books    
   

@app.put("/books/updatebooks" , status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:book_request):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book
            book_changed=True
    
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found.")


    
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(bookrequest:book_request):
    new_book=Book(**bookrequest.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed=True
            break   
    if not book_changed:
        raise HTTPException(status_code=404 ,detail="Item Not found")  
             

def find_book_id(book:Book):
    # if len(BOOKS)>0:
    #     book.id=BOOKS[-1].id +1
    # else:
    #     book.id=1
    # Another Metod of if else-----------
    book.id=1 if len(BOOKS)==1 else BOOKS[-1].id+1 
    return book