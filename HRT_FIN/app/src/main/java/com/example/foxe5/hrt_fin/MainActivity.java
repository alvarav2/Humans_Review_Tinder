package com.example.foxe5.hrt_fin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.view.Menu;
import android.view.MenuItem;
<<<<<<< HEAD
import android.widget.Toast;
=======
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
>>>>>>> bfc0a96535bc8d5dc36897f50b191bf1a7c38396


public class MainActivity extends AppCompatActivity {

<<<<<<< HEAD
    private static final String TAG = "MainActivity";

    DatabaseHelper mDatabaseHelper;
    private Button btnAdd, btnViewData;
    private EditText editText;
=======
    private EditText link;
    private Button sendToProfile;
    private RequestQueue requestQueue;
    private static final String URL = "";
    private StringRequest request;

>>>>>>> bfc0a96535bc8d5dc36897f50b191bf1a7c38396

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

<<<<<<< HEAD
        editText = (EditText) findViewById(R.id.url_input);

        btnAdd = (Button) findViewById(R.id.get_profile);
        mDatabaseHelper = new DatabaseHelper(this);

        btnAdd.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, TinderReview.class);
                startActivity(intent);

                String newEntry = editText.getText().toString();
                if (editText.length() != 0) {
                    AddData(newEntry);
                    editText.setText("");
                } else {
                    toastMessage("You must put something in the text field!");
                }
            }
=======
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
>>>>>>> bfc0a96535bc8d5dc36897f50b191bf1a7c38396


                requestQueue.add(request);
            }
        });
    }
<<<<<<< HEAD

    public void AddData(String newEntry) {
        boolean insertData = mDatabaseHelper.addData(newEntry);

        if (insertData) {
            toastMessage("Data Successfully Inserted!");
        } else {
            toastMessage("Something went wrong");
        }
    }

        /**
         * customizable toast
         * @param message
         */
        private void toastMessage(String message){
            Toast.makeText(this,message, Toast.LENGTH_SHORT).show();
        }

        /*SAVES LINK TO BUTTON*/
        /*Button goToUrl = (Button) findViewById(R.id.get_profile);
        goToUrl.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {
                Intent myWebLink = new Intent(android.content.Intent.ACTION_VIEW);
                myWebLink.setData(Uri.parse("https://go.tinder.com/LT9eWlxobCs-Malachi"));
                startActivity(myWebLink);
            }
        });*/


}
=======
}
>>>>>>> bfc0a96535bc8d5dc36897f50b191bf1a7c38396
