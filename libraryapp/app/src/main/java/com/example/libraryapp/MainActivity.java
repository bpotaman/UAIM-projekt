package com.example.libraryapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private static final String BOOKS_URL = "http://10.0.2.2:5000/api/books";

    private ListView lvBooks;
    private final List<Book> books = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        lvBooks = findViewById(R.id.lvBooks);

        // Kliknięcie w element listy → DetailActivity
        lvBooks.setOnItemClickListener((AdapterView<?> parent, android.view.View view, int position, long id) -> {
            Book book = books.get(position);
            Intent intent = new Intent(MainActivity.this, DetailActivity.class);
            intent.putExtra("ID", book.getId());
            intent.putExtra("TITLE", book.getTitle());
            intent.putExtra("AUTHOR", book.getAuthor());
            intent.putExtra("YEAR", book.getReleaseYear());
            intent.putExtra("IMAGE_URL", book.getImageUrl());
            startActivity(intent);
        });

        // Pobranie listy książek z API
        fetchBooks();
    }

    private void fetchBooks() {
        new Thread(() -> {
            HttpURLConnection conn = null;
            try {
                Log.d("MainActivity", "Łączenie: " + BOOKS_URL);
                URL url = new URL(BOOKS_URL);
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);

                int responseCode = conn.getResponseCode();
                Log.d("MainActivity", "HTTP code: " + responseCode);
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                reader.close();

                // Parsowanie JSON-a
                JSONArray arr = new JSONArray(sb.toString());
                for (int i = 0; i < arr.length(); i++) {
                    JSONObject obj = arr.getJSONObject(i);
                    int id          = obj.getInt("id");
                    String title    = obj.getString("title");
                    String author   = obj.getString("author");
                    int year        = obj.getInt("release_year");
                    String imageUrl = obj.getString("image");
                    books.add(new Book(id, title, author, year, imageUrl));
                }

                // Przełączamy się na wątek UI, żeby ustawić adapter
                runOnUiThread(() -> {
                    BookAdapter adapter = new BookAdapter(
                            MainActivity.this,
                            R.layout.item_book,
                            books
                    );
                    lvBooks.setAdapter(adapter);
                });
            } catch (Exception e) {
                Log.e("MainActivity", "Błąd fetchBooks", e);
                runOnUiThread(() ->
                        Toast.makeText(MainActivity.this, "Błąd: " + e.getMessage(), Toast.LENGTH_LONG).show()
                );
            } finally {
                if (conn != null) conn.disconnect();
            }
        }).start();
    }
}
