package com.example.libraryapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.squareup.picasso.Picasso;

import java.util.List;

public class BookAdapter extends ArrayAdapter<Book> {

    private final Context context;
    private final int resourceId;
    private final LayoutInflater inflater;

    public BookAdapter(@NonNull Context context, int resource, @NonNull List<Book> books) {
        super(context, resource, books);
        this.context = context;
        this.resourceId = resource;
        this.inflater = LayoutInflater.from(context);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        ViewHolder holder;

        if (convertView == null) {
            convertView = inflater.inflate(resourceId, parent, false);
            holder = new ViewHolder();
            holder.ivThumbnail = convertView.findViewById(R.id.ivThumbnail);
            holder.tvTitle     = convertView.findViewById(R.id.tvTitle);
            holder.tvAuthor    = convertView.findViewById(R.id.tvAuthorDetail);
            holder.tvYear      = convertView.findViewById(R.id.tvYearDetail);
            convertView.setTag(holder);
        } else {
            holder = (ViewHolder) convertView.getTag();
        }

        Book book = getItem(position);
        if (book != null) {
            // Tytuł
            holder.tvTitle.setText(book.getTitle());

            // Autor
            holder.tvAuthor.setText(book.getAuthor());

            // Rok wydania
            holder.tvYear.setText(String.valueOf(book.getReleaseYear()));

            // Ładowanie okładki przy pomocy Picasso
            String imageUrl = book.getImageUrl();
            if (imageUrl != null && !imageUrl.isEmpty()) {
                // Jeśli aplikacja działa w emulatorze i backend jest na localhost:5000,
                // Picasso nie załaduje obrazu z "http://localhost". Używamy 10.0.2.2 zamiast localhost.
                String fixedUrl = imageUrl.replace("http://localhost:5000", "http://10.0.2.2:5000");
                Picasso.get()
                        .load(fixedUrl)
                        //.placeholder(R.drawable.placeholder) // jeśli chcesz mieć placeholder
                        //.error(R.drawable.error)             // jeśli chcesz mieć obraz błędu
                        .into(holder.ivThumbnail);
            }
        }

        return convertView;
    }

    private static class ViewHolder {
        ImageView ivThumbnail;
        TextView  tvTitle;
        TextView  tvAuthor;
        TextView  tvYear;
    }
}
