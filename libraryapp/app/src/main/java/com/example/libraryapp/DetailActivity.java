package com.example.libraryapp;

import android.os.Bundle;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class DetailActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_detail);

        TextView tvTitle = findViewById(R.id.tvTitleDetail);
        TextView tvAuthor = findViewById(R.id.tvAuthorDetail);
        TextView tvYear   = findViewById(R.id.tvYearDetail);

        String title  = getIntent().getStringExtra("TITLE");
        String author = getIntent().getStringExtra("AUTHOR");
        int year      = getIntent().getIntExtra("YEAR", -1);

        tvTitle.setText(title);
        tvAuthor.setText("Autor: " + author);
        tvYear.setText("Rok wydania: " + year);
    }
}
