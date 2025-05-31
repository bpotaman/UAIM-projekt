package com.example.libraryapp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private static final String BOOKS_URL =
            "http://192.168.1.3:5000/api/books";


    private ListView lvBooks;
    private final ArrayList<Book> books = new ArrayList<>();    

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        lvBooks = findViewById(R.id.lvBooks);
        lvBooks.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, android.view.View view, int position, long id) {
                Book book = books.get(position);
                Intent intent = new Intent(MainActivity.this, DetailActivity.class);
                intent.putExtra("TITLE", book.getTitle());
                intent.putExtra("AUTHOR", book.getAuthor());
                intent.putExtra("YEAR", book.getReleaseYear());
                startActivity(intent);
            }
        });

        fetchBooks();
    }

    private void fetchBooks() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL(BOOKS_URL);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    conn.setConnectTimeout(5000);
                    conn.setReadTimeout(5000);

                    if (conn.getResponseCode() == 200) {
                        BufferedReader reader = new BufferedReader(
                                new InputStreamReader(conn.getInputStream()));
                        StringBuilder sb = new StringBuilder();
                        String line;
                        while ((line = reader.readLine()) != null) {
                            sb.append(line);
                        }
                        reader.close();

                        JSONArray arr = new JSONArray(sb.toString());
                        for (int i = 0; i < arr.length(); i++) {
                            JSONObject obj = arr.getJSONObject(i);
                            books.add(new Book(
                                    obj.getInt("id"),
                                    obj.getString("title"),
                                    obj.getString("author"),
                                    obj.getInt("release_year")
                            ));
                        }

                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                ArrayList<String> titles = new ArrayList<>();
                                for (Book b : books) {
                                    titles.add(b.getTitle());
                                }
                                lvBooks.setAdapter(new ArrayAdapter<>(
                                        MainActivity.this,
                                        android.R.layout.simple_list_item_1,
                                        titles
                                ));
                            }
                        });
                    }
                    conn.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
}
