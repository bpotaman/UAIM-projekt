package com.example.libraryapp;

public class Book {
    private final int id;
    private final String title;
    private final String author;
    private final int releaseYear;

    public Book(int id, String title, String author, int releaseYear) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.releaseYear = releaseYear;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public int getReleaseYear() {
        return releaseYear;
    }
}
