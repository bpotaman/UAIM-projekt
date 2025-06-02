package com.example.libraryapp;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.util.Log;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.navigation.NavigationView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
//----------------------------------------------
    //-----------------------------------------
    //SPOWROTEM IP DLA DOCKERÓW
    //-------------------------------------------------------
    //-----------------------------------------------
    private static final String BOOKS_URL = "http://192.168.1.3:5000/api/books";

    private ListView lvBooks;
    private final List<Book> books = new ArrayList<>();
    private DrawerLayout drawerLayout;
    private NavigationView navigationView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this::onNavigationItemSelected);
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

        DrawerLayout drawerLayout = findViewById(R.id.drawer_layout);
        FloatingActionButton fab = findViewById(R.id.fabMenu);
        fab.setOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.END));

        // Pobranie listy książek z API
        fetchBooks();
    }

    private boolean onNavigationItemSelected(@NonNull MenuItem item) {
        int id1 = item.getItemId();
        if (id1 == R.id.nav_login) {
            startActivity(new Intent(MainActivity.this, LoginActivity.class));
        }

        if (id1 == R.id.nav_register) {
            startActivity(new Intent(MainActivity.this, RegisterActivity.class));
        }

        drawerLayout.closeDrawers();
        return true;
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
