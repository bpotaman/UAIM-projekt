package com.example.libraryapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.*;
import com.android.volley.toolbox.*;

import org.json.JSONException;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    EditText usernameField, passwordField;
    TextView errorMsg;
    Button loginButton;


    //--------------------------------------------------------------
    //------------------------------------------------------------------
    //DO ZMIANY NA 10.0.2.2
    //--------------------------------------------------------------------
    //--------------------------------------------------------------------
    private static final String LOGIN_URL = "http://192.168.1.3:5000/api/login";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        usernameField = findViewById(R.id.usernameInput);
        passwordField = findViewById(R.id.passwordInput);
        loginButton = findViewById(R.id.loginButton);
        errorMsg = findViewById(R.id.errorText);

        loginButton.setOnClickListener(v -> handleLogin());
    }

    private void handleLogin() {
        String username = usernameField.getText().toString().trim();
        String password = passwordField.getText().toString().trim();

        if (username.isEmpty() || password.isEmpty()) {
            errorMsg.setText("Missing username or password");
            return;
        }

        JSONObject body = new JSONObject();
        try {
            body.put("username", username);
            body.put("password", password);
        } catch (JSONException e) {
            errorMsg.setText("JSON Error");
            return;
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                LOGIN_URL,
                body,
                response -> {
                    try {
                        String token = response.getString("access_token");
                        // Możesz zapisać token w SharedPreferences, jeśli chcesz
                        Toast.makeText(LoginActivity.this, "Login successful", Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        startActivity(intent);
                        finish();
                    } catch (JSONException e) {
                        errorMsg.setText("Response parsing error");
                    }
                },
                error -> {
                    if (error.networkResponse != null) {
                        int status = error.networkResponse.statusCode;
                        if (status == 400) {
                            errorMsg.setText("Missing username or password");
                        } else if (status == 401) {
                            errorMsg.setText("Unauthorized");
                        } else {
                            errorMsg.setText("Login failed (status " + status + ")");
                        }
                    } else {
                        errorMsg.setText("No server response");
                    }
                }
        );

        Volley.newRequestQueue(this).add(request);
    }
}
