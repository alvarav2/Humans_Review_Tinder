package com.example.foxe5.hrt_fin;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;


public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";

    DatabaseHelper mDatabaseHelper;
    private Button btnAdd, btnViewData;
    private EditText editText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

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

        });
    }

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
