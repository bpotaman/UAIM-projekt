package com.example.libraryapp;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.squareup.picasso.Picasso;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

public class DetailActivity extends AppCompatActivity {

    private static final String PREFS_NAME = "BorrowPrefs";
    private static final String KEY_PREFIX = "borrowed_";

    private int bookId;
    private TextView tvTitleDetail;
    private TextView tvAuthorDetail;
    private TextView tvYearDetail;
    private ImageView ivImageDetail;
    private Button btnBorrow;
    private Button btnReturn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        // 1) Pobieramy wszystkie widoki
        tvTitleDetail  = findViewById(R.id.tvTitleDetail);
        tvAuthorDetail = findViewById(R.id.tvAuthorDetail);
        tvYearDetail   = findViewById(R.id.tvYearDetail);
        ivImageDetail  = findViewById(R.id.ivImageDetail);
        btnBorrow      = findViewById(R.id.btnBorrow);
        btnReturn       = findViewById(R.id.btnReturn);

        // 2) Odczytujemy dane z Intentu
        if (getIntent() != null) {
            bookId = getIntent().getIntExtra("ID", -1);
            String title  = getIntent().getStringExtra("TITLE");
            String author = getIntent().getStringExtra("AUTHOR");
            int year      = getIntent().getIntExtra("YEAR", -1);
            String imageUrl = getIntent().getStringExtra("IMAGE_URL");

            if (title != null) {
                tvTitleDetail.setText(title);
            }
            if (author != null) {
                tvAuthorDetail.setText(author);
            }
            if (year != -1) {
                tvYearDetail.setText(String.valueOf(year));
            }

            if (imageUrl != null && !imageUrl.isEmpty()) {
                // backend zwraca "http://localhost:5000...", więc na emulatorze zamieniamy na 10.0.2.2
//                String fixedUrl = imageUrl.replace("http://localhost:5000", "http://10.0.2.2:5000");
                String coverUrl = "http://10.0.2.2:5000/api/books/" + bookId + "/cover";
                Picasso.get()
                        .load(coverUrl)
                        .into(ivImageDetail);
            }
        }

        // 3) Sprawdzamy w SharedPreferences, czy książka jest już wypożyczona
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        long borrowedUntil = prefs.getLong(KEY_PREFIX + bookId, -1);
        long nowMillis     = System.currentTimeMillis();

        if (borrowedUntil > nowMillis) {
            // Książka jest nadal wypożyczona – blokujemy przycisk i pokazujemy datę zwrotu
            btnBorrow.setEnabled(false);
            String dateStr = formatDate(borrowedUntil);
            btnBorrow.setText("Wypożyczono do " + dateStr);

            // Aktywacja przycisku do zwrotu książki
            btnReturn.setVisibility(View.VISIBLE);
            btnReturn.setEnabled(true);
            btnReturn.setText("Zwróć książkę");

        } else {
            btnBorrow.setEnabled(true);
            btnBorrow.setText("Wypożycz książkę");

            btnReturn.setVisibility(View.GONE);
        }
//        if () {
//
//        }
            // Książka nie jest wypożyczona – ustawiamy listener
            btnBorrow.setOnClickListener(v -> {
                // Obliczamy "teraz + 2 miesiące"
                Calendar cal = Calendar.getInstance();
                cal.add(Calendar.MONTH, 2);
                long expireMillis = cal.getTimeInMillis();

                // Zapisujemy w SharedPreferences: klucz borrowed_{bookId} -> expireMillis
                prefs.edit()
                        .putLong(KEY_PREFIX + bookId, expireMillis)
                        .apply();

                // Blokujemy przycisk i ustawiamy tekst z datą zwrotu
                String dateStr = formatDate(expireMillis);
                btnBorrow.setEnabled(false);
                btnBorrow.setText("Wypożyczono do " + dateStr);

                // Pokazujemy potwierdzenie
                Toast.makeText(
                        DetailActivity.this,
                        "Wypożyczono do " + dateStr,
                        Toast.LENGTH_LONG
                ).show();
            });

        btnReturn.setOnClickListener(v -> {
            // 6a) Usuwamy wpis z SharedPreferences
            prefs.edit()
                    .remove(KEY_PREFIX + bookId)
                    .apply();

            // 6b) Przywracamy stan „nie wypożyczona”
            btnBorrow.setEnabled(true);
            btnBorrow.setText("Wypożycz książkę");

            // 6c) Ukrywamy przycisk Zwróć
            btnReturn.setVisibility(View.GONE);

            // 6d) Potwierdzenie zwrotu
            Toast.makeText(
                    DetailActivity.this,
                    "Zwrócono książkę",
                    Toast.LENGTH_SHORT
            ).show();
        });

    }

    private String formatDate(long millis) {
        Date d = new Date(millis);
        SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy", Locale.getDefault());
        return sdf.format(d);
    }
}
