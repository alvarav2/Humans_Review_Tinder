package com.example.foxe5.hrt_fin;

import android.content.Intent;
import android.database.Cursor;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import java.util.ArrayList;
import java.util.List;
/**
 * Created by foxe5 on 2/16/19.
 */


public class TinderReview extends AppCompatActivity{

    DatabaseHelper myDB;

    private Button btnViewData;
    private EditText editText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.tinder_profile);
        btnViewData = (Button) findViewById(R.id.post_review);
        editText = (EditText) findViewById(R.id.review_input);
        myDB = new DatabaseHelper(this);

        ListView listView = (ListView) findViewById(R.id.listView);
        myDB = new DatabaseHelper(TinderReview.this);

        ArrayList<String> theList = new ArrayList<>();
        Cursor data = myDB.getData();
        while(data.moveToNext()){
            theList.add(data.getString(1));
            ListAdapter listAdapter = new ArrayAdapter<>(this,android.R.layout.simple_list_item_1,theList);
            listView.setAdapter(listAdapter);
        }


        btnViewData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Intent intent = new Intent(TinderReview.this, ListDataActivity.class);
                //startActivity(intent);

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
        boolean insertData = myDB.addData(newEntry);

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
}
