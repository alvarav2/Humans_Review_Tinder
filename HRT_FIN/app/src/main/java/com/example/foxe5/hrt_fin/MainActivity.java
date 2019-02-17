package com.example.foxe5.hrt_fin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.StringReader;


public class MainActivity extends AppCompatActivity {

    private EditText link;
    private Button sendToProfile;
    private RequestQueue requestQueue;
    private static final String URL = "";
    private StringRequest request;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        link = (EditText) findViewById(R.id.url_input);
        sendToProfile = (Button) findViewById(R.id.get_profile);

        requestQueue = Volley.newRequestQueue(this);

        sendToProfile.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                request = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject jsonObject = new JSONObject(response);
                            if (jsonObject.names().get(0).equals("success")) {
                                Toast.makeText(getApplicationContext(), "SUCCESS" + jsonObject.getString("success"), Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(MainActivity.this, TinderReview.class);
                                startActivity(intent);
                            } else {
                                Toast.makeText(getApplicationContext(), "Error" + jsonObject.getString("error"), Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                    }
                });


                requestQueue.add(request);
            }
        });
    }
}