package com.example.libraryapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.*;
import com.android.volley.toolbox.*;

import org.json.JSONException;
import org.json.JSONObject;

public class RegisterActivity extends AppCompatActivity {

    EditText emailField, usernameField, passwordField;
    Button registerButton;
    TextView errorMsg;
//---------------------------------------------------------------------------------
    //---------------------------------------------------------
    //SPOWROTEM NA IP DLA DOCKEROW
    //-----------------------------------------------------------
    //--------------------------------------------
    private static final String REGISTER_URL = "http://10.0.2.2:5000/api/register";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        emailField = findViewById(R.id.emailInput);
        usernameField = findViewById(R.id.usernameInput);
        passwordField = findViewById(R.id.passwordInput);
        registerButton = findViewById(R.id.registerButton);
        errorMsg = findViewById(R.id.errorText);

        registerButton.setOnClickListener(v -> handleRegister());
    }

    private void handleRegister() {
        String email = emailField.getText().toString().trim();
        String username = usernameField.getText().toString().trim();
        String password = passwordField.getText().toString().trim();

        if (email.isEmpty() || username.isEmpty() || password.isEmpty()) {
            errorMsg.setText("All fields are required");
            return;
        }

        JSONObject requestBody = new JSONObject();
        try {
            requestBody.put("email", email);
            requestBody.put("username", username);
            requestBody.put("password", password);
        } catch (JSONException e) {
            errorMsg.setText("Error creating request");
            return;
        }

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.POST,
                REGISTER_URL,
                requestBody,
                response -> {
                    Log.d("REGISTER", "Success: " + response.toString());
                    Toast.makeText(RegisterActivity.this, "Registration successful", Toast.LENGTH_SHORT).show();
                    startActivity(new Intent(RegisterActivity.this, LoginActivity.class));
                    finish();
                },
                error -> {
                    if (error.networkResponse != null) {
                        int status = error.networkResponse.statusCode;
                        if (status == 400) {
                            errorMsg.setText("Missing or invalid input");
                        } else if (status == 409) {
                            errorMsg.setText("Username or email already exists");
                        } else {
                            errorMsg.setText("Registration failed with status: " + status);
                        }
                    } else {
                        errorMsg.setText("No Server Response");
                    }
                }
        );

        request.setRetryPolicy(new DefaultRetryPolicy(
                5000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

        Volley.newRequestQueue(this).add(request);
    }
}
